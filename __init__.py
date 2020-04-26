import importlib
from . import settings
from .client import client

for module in settings.MODULES:
    _ = importlib.import_module(f'.modules.{module}', package=__name__)
