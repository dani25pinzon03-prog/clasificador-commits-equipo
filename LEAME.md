# Sistema Inteligente de Clasificación de Commits (ADSO - SENA)

Repositorio oficial para el desarrollo del proyecto de integración de modelos de lenguaje locales con un backend en FastAPI y base de datos relacional.

## 👥 Información del Proyecto
- **Programa:** Análisis y Desarrollo de Software (ADSO - Ficha 3492142)
- **Aprendiz:** Daniel Stiven Pinzón Martínez
- **Aprendiz:** Juan Esteban Moncada Gomez
- **Aprendiz:** David Jose Gonzalez Noguera
- **Aprendiz:** Joel Santiago Herrera Vergara
- **Institución:** SENA Regional Tolima

---

## 🛠️ Stack Tecnológico
- **Entorno de ejecución:** WSL2 (Ubuntu 24.04)
- **Lenguaje:** Python 3.12+
- **Base de Datos:** PostgreSQL 16 (en contenedor Docker)
- **Inferencia Local:** Ollama con el modelo `qwen2.5-coder:1.5b`
- **Framework Web:** FastAPI & Uvicorn

---

## 📂 Estructura del Repositorio
```text
clasificador-commits-equipo/
├── app/                  # Código fuente de la API (FastAPI)
├── db/                   # Scripts de inicialización de PostgreSQL
├── docs/                 # Informes técnicos y caracterización del modelo
├── tests/                # Pruebas automatizadas
├── .env                  # Variables de entorno (confidencial)
├── requirements.txt      # Dependencias del proyecto
└── LÉAME.md              # Documentación principal
