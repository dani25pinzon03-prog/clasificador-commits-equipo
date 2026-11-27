# Informe Técnico — Plan de Pruebas de Despliegue (AA4)

**Proyecto:** Clasificador de Commits con IA Local y Reglas  
**Programa:** Tecnólogo en Análisis y Desarrollo de Software (ADSO) — Ficha 3492142  
**Fecha:** 27 de noviembre de 2026  

---

## 1. Arquitectura y Entorno de Despliegue

El sistema está compuesto por tres componentes principales:
- **API Backend (`fastapi_commits_app`):** Aplicación Python 3.12 con FastAPI ejecutándose en contenedor Docker (`puerto 8000`), conectada a PostgreSQL bajo el rol de privilegios mínimos `app_ia` y al servidor local de Ollama (`qwen2.5-coder:1.5b`).
- **Base de Datos (`postgres_db_commits`):** PostgreSQL 15 Alpine en contenedor Docker (`puerto 5432`) con volumen persistente `postgres_data` e inicialización automatizada mediante `db/init.sql`.
- **Integración Continua (GitHub Actions):** Pipeline automatizado en `.github/workflows/ci.yml` que ejecuta análisis estático (`ruff`), construcción de imagen Docker (`docker build`) y pruebas automatizadas (`pytest`).

---

## 2. Matriz de Resultados de Pruebas (P-01 a P-09)

| ID | Categoría | Descripción de la Prueba | Resultado Obtenido | Estado |
| :--- | :--- | :--- | :--- | :---: |
| **P-01** | Funcional | Disponibilidad de endpoints `GET /` y `GET /health` | Respuesta HTTP `200 OK` con estado `healthy` y confirmación de modelo `qwen2.5-coder:1.5b` | **APROBADO** |
| **P-02** | Funcional | Clasificación con motor `eco` y validación de reglas (`feat`, `fix`, `docs`, `refactor`, `test`) | Respuesta HTTP `200 OK`, clasificación exacta según prefijo y persistencia en BD (`guardado_en_db: true`) | **APROBADO** |
| **P-03** | Funcional / Negativa | Rechazo de motor inválido en `POST /clasificar` y consulta en `GET /inferencias` | Código HTTP `400 Bad Request` ante motor inexistente; `GET /inferencias` retorna lista JSON ordenada | **APROBADO** |
| **P-04** | Seguridad / Acceso | Verificación de privilegios mínimos con el rol PostgreSQL `app_ia` | `SELECT` permitido; `DELETE` bloqueado (`permission denied`) y `DROP TABLE` bloqueado (`must be owner`) | **APROBADO** |
| **P-05** | Conectividad | Resolución DNS interna entre contenedor `api` y contenedor `db` | El contenedor `api` resuelve el host `db` en la subred privada de Docker (`172.18.0.2`) | **APROBADO** |
| **P-06** | Alta Disponibilidad | Recuperación del servicio tras reinicio controlado de PostgreSQL (`docker compose restart db`) | La API recupera conexión automáticamente y `/health` responde `200 OK` | **APROBADO** |
| **P-07** | Persistencia | Conservación de inferencias tras recrear contenedores (`docker compose down` y `up -d`) | El volumen `postgres_data` conserva íntegros los registros almacenados previamente en `historial_commits` | **APROBADO** |
| **P-08** | Carga (k6) | Prueba de carga de 2 minutos escalando hasta 10 usuarios virtuales (VUs) sobre `/clasificar` (`eco`) | **657 peticiones** (`5.08 req/s`), **0.00% errores**, promedio **10.43 ms**, **`p(95)` = 13.5 ms** (umbral `< 800 ms`) | **APROBADO** |
| **P-09** | Rendimiento IA | Caracterización secuencial de 10 peticiones al motor `ollama` (`qwen2.5-coder:1.5b`) | **10/10 exitosas (100%)**; mín. **53.8 ms**, promedio **4193.7 ms**, máx. **41028.8 ms** (arranque en frío) | **APROBADO** |

---

## 3. Análisis Técnico y Conclusiones

1. **Rendimiento del motor híbrido:** El motor determinista (`eco`) soporta concurrencia sostenida con latencia `p(95)` de `13.5 ms` y `0%` de fallos, ideal para clasificación inmediata de alto volumen. Por su parte, el modelo local `qwen2.5-coder:1.5b` en CPU presenta una latencia inicial de `41.0 s` en la primera petición debido a la carga del modelo en memoria RAM, estabilizándose entre `53.8 ms` y `166.5 ms` en las siguientes peticiones secuenciales.
2. **Seguridad y resiliencia:** La separación de roles en PostgreSQL (`postgres` como propietario y `app_ia` limitado a `SELECT` e `INSERT`) mitiga el riesgo de pérdida accidental o maliciosa de datos desde la capa de aplicación, mientras que los volúmenes nombrados en Docker garantizan la persistencia ante reinicios de infraestructura.
