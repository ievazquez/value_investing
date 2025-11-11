#!/bin/bash
# Wrapper script para ejecutar el CLI de Value Investing Analyzer

# Detectar el directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/backend"

# Ejecutar CLI con todos los argumentos pasados
python3 cli.py "$@"
