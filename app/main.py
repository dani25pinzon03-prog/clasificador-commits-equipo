from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database import guardar_historial, obtener_historial
from app.engine_eco import clasificar_con_eco
from app.engine_ollama import clasificar_con_ollama

app = FastAPI(
    title="Clasificador de Commits - API",
    version="1.0.0",
    description="Backend para la clasificación de commits con reglas y Ollama."
)


class CommitRequest(BaseModel):
    mensaje: str
    motor: str = "eco"


@app.get("/")
def read_root():
    return {"status": "ok", "message": "API del Clasificador de Commits funcionando correctamente"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ollama_model": "qwen2.5-coder:1.5b"
    }


@app.post("/clasificar")
def clasificar_commit(request: CommitRequest):
    if request.motor == "ollama":
        resultado = clasificar_con_ollama(request.mensaje)
    elif request.motor == "eco":
        resultado = clasificar_con_eco(request.mensaje)
    else:
        raise HTTPException(status_code=400, detail="motor debe ser eco u ollama")

    if "error" not in resultado:
        guardar_historial(
            mensaje=request.mensaje,
            motor=resultado.get("motor"),
            clasificacion=resultado.get("clasificacion")
        )
        resultado["guardado_en_db"] = True
    else:
        resultado["guardado_en_db"] = False

    return resultado


@app.get("/inferencias")
def listar_inferencias(limite: int = 20):
    return obtener_historial(limite)
