import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "qwen2.5-coder:1.5b"

def clasificar_con_ollama(mensaje: str) -> dict:
    prompt = f"Clasifica el siguiente mensaje de commit en una categoría (ej. bugfix, feature, docs, refactor) respondiendo brevemente: '{mensaje}'"

    payload = {
        "model": MODELO,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=10)
        if response.status_code == 200:
            resultado = response.json().get("response", "Sin respuesta")
            return {
                "motor": "ollama",
                "modelo": MODELO,
                "mensaje_original": mensaje,
                "clasificacion": resultado.strip()
            }
        else:
            return {"error": "Error al conectar con el servidor de Ollama"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Ollama no está disponible: {e!s}"}
