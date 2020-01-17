#!/usr/bin/env python3
"""Main dashboard program. Execute this file to start the server."""
import callbacks  # noqa (this tells flake8 to ignore the "unused" import)
from app import app

if __name__ == '__main__':
    app.run_server(debug=True, host='localhost', port=8050)
