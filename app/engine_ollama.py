import os


import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
OLLAMA_URL = f"{OLLAMA_HOST}/api/generate"
MODELO = "qwen2.5-coder:1.5b"


def clasificar_con_ollama(mensaje: str) -> dict:
    prompt = (
        "Clasifica el siguiente mensaje de commit en una categoría "
        f"(ej. bugfix, feature, docs, refactor) respondiendo brevemente: '{mensaje}'"
    )

    payload = {
        "model": MODELO,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        if response.status_code == 200:
            resultado = response.json().get("response", "Sin respuesta")
            return {
                "motor": "ollama",
                "modelo": MODELO,
                "mensaje_original": mensaje,
                "clasificacion": resultado.strip(),
            }
        return {"error": "Error al conectar con el servidor de Ollama"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Ollama no está disponible: {e!s}"}
