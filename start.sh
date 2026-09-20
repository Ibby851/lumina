#!/bin/bash
uv run manage.py qcluster
uv run daphne -b 0.0.0.0 -p "$PORT" website.asgi:application