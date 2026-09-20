#!/bin/bash
uv run python manage.py qcluster &
uv run daphne -b 0.0.0.0 -p "$PORT" website.asgi:application