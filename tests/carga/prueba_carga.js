import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [
    { duration: "30s", target: 5 },
    { duration: "1m", target: 10 },
    { duration: "30s", target: 0 },
  ],
  thresholds: {
    http_req_duration: ["p(95)<800"],
    http_req_failed: ["rate<0.05"],
  },
};

const MENSAJES = [
  "feat: agrega el endpoint de historial",
  "fix: corrige el error de conexion",
  "docs: actualiza el manual de instalacion",
  "test: agrega pruebas del clasificador",
];

export default function () {
  const texto = MENSAJES[Math.floor(Math.random() * MENSAJES.length)];
  const carga = JSON.stringify({ mensaje: texto, motor: "eco" });
  const cab = { headers: { "Content-Type": "application/json" } };
  const r = http.post("http://localhost:8000/clasificar", carga, cab);
  check(r, {
    "codigo 200": (res) => res.status === 200,
    "devuelve clasificacion": (res) => res.json("clasificacion") !== undefined,
  });
  sleep(1);
}
