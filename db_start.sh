#!/bin/sh

sqlite3 src/urls.db -cmd ".tables" ".quit"

alembic upgrade head
