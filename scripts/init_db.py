# Database initialization
"""Initialize Atlas tables in Render PostgreSQL from infra/schema.sql.

Usage (from project root): python scripts/init_db.py
Safe to rerun: the supplied schema uses CREATE ... IF NOT EXISTS.
"""
import os
import sys
from pathlib import Path

try:
    import psycopg
except ImportError:  # pragma: no cover - dependency is optional until install
    psycopg = None

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - fallback when dependency is not installed
    def load_dotenv(*_args, **_kwargs):
        return False

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env')
SCHEMA = ROOT / 'infra' / 'schema.sql'
REQUIRED = ('documents', 'feedback', 'audit_events', 'approvals', 'chat_messages')


def _connect(url: str):
    if psycopg is not None:
        return psycopg.connect(url, connect_timeout=15)

    try:
        import psycopg2
    except ImportError as exc:  # pragma: no cover - covered by runtime environment
        raise RuntimeError(
            'No supported PostgreSQL driver is installed. Install "psycopg" or "psycopg2-binary".'
        ) from exc

    return psycopg2.connect(dsn=url, connect_timeout=15)


def _execute_schema(conn, schema_sql: str) -> None:
    if psycopg is not None:
        with conn.transaction():
            conn.execute(schema_sql)
        return

    with conn:
        with conn.cursor() as cur:
            cur.execute(schema_sql)


def main():
    url = os.getenv('DATABASE_URL', '').strip()
    if not url or 'YOUR_' in url or 'USERNAME:' in url:
        print('ERROR: Set a real DATABASE_URL in the project .env file.')
        return 1
    if not SCHEMA.is_file():
        print(f'ERROR: Schema not found: {SCHEMA}')
        return 1
    print('Connecting to Render PostgreSQL (credentials hidden)...')
    try:
        with _connect(url) as conn:
            _execute_schema(conn, 'CREATE EXTENSION IF NOT EXISTS pgcrypto;')
            _execute_schema(conn, SCHEMA.read_text(encoding='utf-8'))
            with conn.cursor() as cur:
                cur.execute('SELECT current_database()')
                dbname = cur.fetchone()[0]
                for table in REQUIRED:
                    cur.execute('SELECT to_regclass(%s)', (f'public.{table}',))
                    if cur.fetchone()[0] is None:
                        raise RuntimeError(f'Missing table: {table}')
        print(f'SUCCESS: Database {dbname!r} initialized; verified {len(REQUIRED)} tables.')
        print('You can safely rerun this script. Existing rows are preserved.')
        return 0
    except Exception as exc:
        print(f'ERROR: Database initialization failed: {type(exc).__name__}: {exc}')
        return 1


if __name__ == '__main__':
    sys.exit(main())