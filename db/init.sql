CREATE TABLE IF NOT EXISTS historial_commits (
    id SERIAL PRIMARY KEY,
    mensaje TEXT NOT NULL,
    motor VARCHAR(20) NOT NULL,
    clasificacion VARCHAR(50) NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT NOW()
);

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'app_ia') THEN
        CREATE ROLE app_ia WITH LOGIN PASSWORD 'password';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE clasificador_db TO app_ia;
GRANT USAGE ON SCHEMA public TO app_ia;
GRANT SELECT, INSERT ON historial_commits TO app_ia;
GRANT USAGE, SELECT ON SEQUENCE historial_commits_id_seq TO app_ia;
