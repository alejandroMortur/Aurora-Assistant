import sys
import os

sys.path.append("../testCore")

import pytest

# Añade la ruta a la carpeta src para importar Main
sys.path.append(os.path.abspath('../../src'))

# Importa la función main desde Main.py
from virtual_assistant.Main import main

def test_main(capsys):
    # Ejecuta la función main y captura la salida estándar
    main()

    # Obtiene la salida estándar capturada
    captured = capsys.readouterr()

    # Verifica que la salida coincida con lo esperado
    assert captured.out.strip() == "¡Hola, mundo!"
