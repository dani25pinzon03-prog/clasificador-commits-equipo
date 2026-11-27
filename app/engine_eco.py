def clasificar_con_eco(mensaje: str) -> dict:
    mensaje_lower = mensaje.lower()

    if "fix" in mensaje_lower or "bug" in mensaje_lower:
        tipo = "bugfix"
    elif "feat" in mensaje_lower or "add" in mensaje_lower:
        tipo = "feature"
    elif "docs" in mensaje_lower:
        tipo = "documentation"
    else:
        tipo = "refactor/other"

    return {
        "motor": "eco",
        "mensaje_original": mensaje,
        "clasificacion": tipo
    }
