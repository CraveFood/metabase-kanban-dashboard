import os

POSTGRES_DATABASE_URL = os.getenv(
    "KANBANDASH_DATABASE_URL", "postgresql://postgres@postgres/kanban_metrics"
)
