export $(grep -v '^#' .env.development | xargs)
uv run gunicorn app:app