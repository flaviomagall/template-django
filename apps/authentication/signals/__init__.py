# apps/authentication/signals/__init__.py

import os
import importlib

signals_dir = os.path.dirname(__file__)

for filename in os.listdir(signals_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f"apps.authentication.signals.{filename[:-3]}"
        importlib.import_module(module_name)
