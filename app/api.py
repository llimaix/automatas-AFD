from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .store import store
import os
import tempfile

app = FastAPI(title="AFD Recognizer", version="1.0")

# Configuración CORS - permitir todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los headers
)

class LoadRequest(BaseModel):
    path: str  # ruta en el contenedor, p.ej. /app/data/automatas.txt

class CheckRequest(BaseModel):
    automata: str
    word: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Sube un archivo de autómatas y lo carga directamente"""
    try:
        # Verificar que es un archivo de texto
        if not file.filename.endswith('.txt'):
            raise HTTPException(status_code=400, detail="Solo se permiten archivos .txt")
        
        # Leer el contenido del archivo
        content = await file.read()
        
        # Crear un archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
            tmp_file.write(content.decode('utf-8'))
            tmp_path = tmp_file.name
        
        try:
            # Cargar los autómatas desde el archivo temporal
            loaded = store.load_from_file(tmp_path)
            return {
                "message": f"Archivo '{file.filename}' subido y cargado exitosamente",
                "loaded": loaded,
                "filename": file.filename
            }
        finally:
            # Limpiar archivo temporal
            os.unlink(tmp_path)
            
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="El archivo debe estar en formato UTF-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error procesando archivo: {str(e)}")

@app.post("/load")
def load(req: LoadRequest):
    try:
        loaded = store.load_from_file(req.path)
        return {"loaded": loaded}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/automata")
def list_automata():
    return {"automata": store.list()}

@app.post("/check")
def check(req: CheckRequest):
    try:
        return store.check(req.automata, req.word)
    except KeyError as ke:
        raise HTTPException(status_code=404, detail=str(ke))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
