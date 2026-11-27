"""Pruebas funcionales de los endpoints de la API."""
from fastapi.testclient import TestClient
from app.main import app
from app.engine_eco import clasificar_con_eco

cliente = TestClient(app)


def test_root_responde_ok():
    r = cliente.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_health_responde_healthy():
    r = cliente.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_clasificar_eco_devuelve_clasificacion():
    r = cliente.post("/clasificar", json={"mensaje": "fix: corrige el error de login", "motor": "eco"})
    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["clasificacion"] == "bugfix"
    assert cuerpo["motor"] == "eco"
    assert cuerpo["guardado_en_db"] is True


def test_reglas_del_motor_eco():
    assert clasificar_con_eco("feat: agrega endpoint")["clasificacion"] == "feature"
    assert clasificar_con_eco("docs: actualiza el readme")["clasificacion"] == "documentation"
    assert clasificar_con_eco("limpia variables")["clasificacion"] == "refactor/other"
def test_clasificar_rechaza_motor_invalido():
    r = cliente.post("/clasificar", json={"mensaje": "hola", "motor": "inventado"})
    assert r.status_code == 400


def test_inferencias_devuelve_lista():
    r = cliente.get("/inferencias?limite=5")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
