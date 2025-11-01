from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .store import store

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
