import os
import pkgutil

__all__ = []
PATH = [os.path.dirname(__file__)]
for loader, module_name, is_pkg in pkgutil.walk_packages(PATH):
    __all__.append(module_name)
    spec = loader.find_spec(module_name)
    if spec and spec.loader:
        _module = spec.loader.load_module(module_name)
    globals()[module_name] = _module
