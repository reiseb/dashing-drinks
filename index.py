#!/usr/bin/env python3
"""Main dashboard program. Execute this file to start the server."""
from . import callbacks  # noqa (ignore the "unused" import)
from . import app

if __name__ == '__main__':
    app.dashapp.run_server(debug=True, host='localhost', port=8050)
