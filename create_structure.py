import os
from pathlib import Path

PROJECT_NAME = "ATLAS-Enterprise-AI"  # change if you like

# Folders (empty ones get a .gitkeep so Git tracks them)
DIRS = [
    "app/templates",
    "app/static",
    "worker",
    "infra",
    "scripts",
    "docs",
    "test",
    ".github/workflows",
    ".vscode",
]

# Files (created empty, or with starter content where given)
FILES = {
    # app/
    "app/__init__.py": "",
    "app/main.py": "# FastAPI routes and UI serving\n",
    "app/graph.py": "# LangGraph workflow\n",
    "app/rag.py": "# RAG integration\n",
    "app/vector.py": "# Pinecone operations\n",
    "app/aws.py": "# AWS clients\n",
    "app/db.py": "# PostgreSQL access and audit\n",
    "app/memory.py": "# Conversation persistence\n",
    "app/guardrails.py": "# Input/output safety checks\n",
    "app/observability.py": "# Rius initialization\n",
    "app/config.py": "# Runtime configuration\n",
    "app/templates/index.html": "",
    "app/static/style.css": "",
    "app/static/app.js": "",

    # worker/
    "worker/__init__.py": "",
    "worker/ingest.py": "# File processing and indexing\n",

    # infra/ and scripts/
    "infra/schema.sql": "-- Database schema\n",
    "scripts/init_db.py": "# Database initialization\n",

    # docs/
    "docs/SETUP.md": "# Setup\n",
    "docs/HITL_GUARDRAILS.md": "# HITL and Guardrails\n",
    "docs/RIUS_OBSERVABILITY.md": "# Rius Observability\n",
    "docs/APPROVALS_TROUBLESHOOTING.md": "# Approvals Troubleshooting\n",

    # CI/CD
    ".github/workflows/deploy.yml": "# GitHub Actions pipeline\n",

    # root files
    "requirements.txt": (
        "fastapi\nuvicorn\nlanggraph\nboto3\npinecone\n"
        "psycopg2-binary\npython-dotenv\n"
    ),
    "Dockerfile": "",
    ".env.example": (
        "AWS_REGION=us-east-1\n"
        "S3_BUCKET=your-private-document-bucket\n"
        "BEDROCK_EMBED_MODEL=amazon.titan-embed-text-v2:0\n"
        "BEDROCK_CHAT_MODEL=amazon.nova-lite-v1:0\n"
        "EMBED_DIM=1024\n\n"
        "PINECONE_API_KEY=your-pinecone-key\n"
        "PINECONE_INDEX_NAME=atlas-rag-index\n"
        "PINECONE_CLOUD=aws\n"
        "PINECONE_REGION=us-east-1\n\n"
        "DATABASE_URL=postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require\n\n"
        "HITL_ENABLED=true\n"
        "MEMORY_TURNS=6\n\n"
        "RIUS_API_KEY=\n"
        "RIUS_SERVICE_NAME=atlas-enterprise-ai\n"
        "RIUS_DISABLED=false\n"
        "RIUS_CAPTURE_CONTENT=false\n"
    ),
    ".gitignore": ".env\n.venv/\n__pycache__/\n*.pyc\n.DS_Store\n",
    "README.md": f"# {PROJECT_NAME}\n",
}


def create_structure(root: str) -> None:
    root_path = Path(root)

    for d in DIRS:
        (root_path / d).mkdir(parents=True, exist_ok=True)

    for rel_path, content in FILES.items():
        file_path = root_path / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if file_path.exists():
            print(f"skipped (exists): {rel_path}")
            continue
        file_path.write_text(content, encoding="utf-8")
        print(f"created: {rel_path}")

    # keep truly empty folders in Git
    for d in ["test", ".vscode"]:
        keep = root_path / d / ".gitkeep"
        if not any((root_path / d).iterdir()):
            keep.touch()

    print(f"\nDone. Project created at: {root_path.resolve()}")


if __name__ == "__main__":
    create_structure(PROJECT_NAME)