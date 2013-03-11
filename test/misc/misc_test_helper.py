#!/usr/bin/python
# -*- coding: utf8 -*-

# Añade a la variable de entorno PYTHONPATH la ruta
# hacia la carpeta raíz del proyecto
import sys
import os
dirname, filename = os.path.split(os.path.abspath(__file__))
sys.path.append(os.path.join(dirname, '../../'))

from helpers.config_helper import setConfig
setConfig(test_mode=True)
