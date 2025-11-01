from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from .store import store
import os
import tempfile
import logging
import time
from typing import Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AFD Recognizer", version="1.0")

# Configuración CORS - permitir todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los headers
)

# Límites de seguridad
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_WORD_LENGTH = 10000
MAX_AUTOMATA_NAME_LENGTH = 100

@app.on_event("startup")
async def startup_event():
    """Inicializa el store al arrancar la aplicación"""
    logger.info("🚀 Iniciando AFD Recognizer API...")
    store.initialize()
    logger.info("✅ Store inicializado correctamente")

class LoadRequest(BaseModel):
    path: str  # ruta en el contenedor, p.ej. /app/data/automatas.txt
    
    @validator('path')
    def validate_path(cls, v):
        if not v or len(v) > 500:
            raise ValueError('Path debe tener entre 1 y 500 caracteres')
        # Validación básica de path traversal
        if '..' in v or v.startswith('/etc') or v.startswith('/proc'):
            raise ValueError('Path no permitido por seguridad')
        return v

class CheckRequest(BaseModel):
    automata: str
    word: str
    max_length: Optional[int] = MAX_WORD_LENGTH
    
    @validator('automata')
    def validate_automata_name(cls, v):
        if not v or len(v) > MAX_AUTOMATA_NAME_LENGTH:
            raise ValueError(f'Nombre de autómata debe tener entre 1 y {MAX_AUTOMATA_NAME_LENGTH} caracteres')
        # Solo caracteres seguros
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Nombre de autómata solo puede contener letras, números, _ y -')
        return v
    
    @validator('word')
    def validate_word(cls, v):
        if len(v) > MAX_WORD_LENGTH:
            raise ValueError(f'Palabra demasiado larga (máximo {MAX_WORD_LENGTH} caracteres)')
        return v
    
    @validator('max_length')
    def validate_max_length(cls, v):
        if v is not None and (v < 1 or v > MAX_WORD_LENGTH):
            raise ValueError(f'max_length debe estar entre 1 y {MAX_WORD_LENGTH}')
        return v

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    return response

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Sube un archivo de autómatas y lo carga directamente"""
    try:
        # Validaciones de seguridad
        if not file.filename:
            raise HTTPException(status_code=400, detail="Nombre de archivo requerido")
        
        if len(file.filename) > 255:
            raise HTTPException(status_code=400, detail="Nombre de archivo demasiado largo")
            
        if not file.filename.endswith('.txt'):
            raise HTTPException(status_code=400, detail="Solo se permiten archivos .txt")
        
        # Verificar tamaño del archivo
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413, 
                detail=f"Archivo demasiado grande. Máximo: {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Archivo vacío")
        
        # Crear un archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
            try:
                content_str = content.decode('utf-8')
            except UnicodeDecodeError:
                raise HTTPException(status_code=400, detail="El archivo debe estar en formato UTF-8")
            
            tmp_file.write(content_str)
            tmp_path = tmp_file.name
        
        try:
            # Cargar los autómatas desde el archivo temporal
            logger.info(f"Cargando archivo: {file.filename}")
            loaded = store.load_from_file(tmp_path)
            logger.info(f"Autómatas cargados exitosamente: {loaded}")
            
            return {
                "message": f"Archivo '{file.filename}' subido y cargado exitosamente",
                "loaded": loaded,
                "count": len(loaded),
                "filename": file.filename
            }
        except ValueError as e:
            logger.error(f"Error de validación cargando {file.filename}: {e}")
            raise HTTPException(status_code=400, detail=f"Error de validación: {str(e)}")
        except Exception as e:
            logger.error(f"Error procesando {file.filename}: {e}")
            raise HTTPException(status_code=500, detail=f"Error interno procesando archivo")
        finally:
            # Limpiar archivo temporal
            try:
                os.unlink(tmp_path)
            except:
                pass
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado en upload: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.post("/load")
def load(req: LoadRequest):
    try:
        logger.info(f"Cargando desde path: {req.path}")
        loaded = store.load_from_file(req.path)
        logger.info(f"Autómatas cargados: {loaded}")
        return {
            "loaded": loaded,
            "count": len(loaded),
            "path": req.path
        }
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado: {req.path}")
        raise HTTPException(status_code=404, detail=f"Archivo no encontrado: {req.path}")
    except PermissionError:
        logger.error(f"Sin permisos para leer: {req.path}")
        raise HTTPException(status_code=403, detail="Sin permisos para leer el archivo")
    except ValueError as e:
        logger.error(f"Error de validación: {e}")
        raise HTTPException(status_code=400, detail=f"Error de validación: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado cargando {req.path}: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/automata")
def list_automata():
    try:
        automata_list = store.list()
        return {
            "automata": automata_list,
            "count": len(automata_list)
        }
    except Exception as e:
        logger.error(f"Error listando autómatas: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.post("/check")
def check(req: CheckRequest):
    try:
        logger.info(f"Verificando '{req.word}' en autómata '{req.automata}'")
        
        # Usar el límite especificado en la request
        max_length = req.max_length or MAX_WORD_LENGTH
        
        result = store.check(req.automata, req.word, max_length=max_length)
        
        # Agregar información adicional útil
        result.update({
            "word_length": len(req.word),
            "max_length_used": max_length,
            "path_length": len(result.get("path", []))
        })
        
        logger.info(f"Resultado: {result['accepted']}, path length: {result['path_length']}")
        return result
        
    except KeyError as ke:
        logger.error(f"Autómata no encontrado: {ke}")
        raise HTTPException(status_code=404, detail=f"Autómata no encontrado: {str(ke)}")
    except ValueError as e:
        logger.error(f"Error de validación: {e}")
        raise HTTPException(status_code=400, detail=f"Error de validación: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado en check: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/automata/{name}/info")
def get_automata_info(name: str):
    """Obtiene información detallada de un autómata específico"""
    try:
        if len(name) > MAX_AUTOMATA_NAME_LENGTH:
            raise HTTPException(status_code=400, detail="Nombre de autómata demasiado largo")
        
        dfa = store.get(name)
        return {
            "name": dfa.name,
            "states": sorted(list(dfa.states)),
            "alphabet": sorted(list(dfa.alphabet)),
            "start": dfa.start,
            "finals": sorted(list(dfa.finals)),
            "transitions": [
                {"from": s, "symbol": a, "to": t}
                for (s, a), t in sorted(dfa.delta.items())
            ],
            "is_complete": dfa.is_complete(),
            "state_count": len(dfa.states),
            "alphabet_size": len(dfa.alphabet),
            "transition_count": len(dfa.delta)
        }
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Autómata '{name}' no encontrado")
    except Exception as e:
        logger.error(f"Error obteniendo info de {name}: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.post("/admin/clear")
def clear_all_automatas():
    """Limpia todos los autómatas de la memoria (admin)"""
    try:
        store.clear_all()
        return {"message": "Todos los autómatas han sido eliminados de memoria", "success": True}
    except Exception as e:
        logger.error(f"Error limpiando autómatas: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.post("/admin/reset")
def reset_to_defaults():
    """Resetea a los autómatas por defecto (admin)"""
    try:
        store.reset_to_defaults()
        return {
            "message": "Store reseteado a autómatas por defecto",
            "automata": store.list(),
            "count": len(store.list()),
            "success": True
        }
    except Exception as e:
        logger.error(f"Error reseteando a defaults: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/admin/status")
def get_store_status():
    """Obtiene el estado actual del store (admin)"""
    try:
        automata_list = store.list()
        return {
            "automata_count": len(automata_list),
            "automata": automata_list,
            "storage_type": "memory_only",
            "default_file_exists": os.path.exists("/app/data/automatas.txt"),
            "note": "Los autómatas se mantienen solo en memoria durante la sesión del servidor"
        }
    except Exception as e:
        logger.error(f"Error obteniendo status: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
