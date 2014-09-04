# from https://github.com/dgreisen/django-traversal/blob/master/appring.py
# Apache 2.0 licensed

try:
    from django.db.models.loading import AppCache
    apps = AppCache()
except:
    from django.apps import apps
from django.conf import settings
from importlib import import_module
from types import ModuleType

class Apps(object):
    """
    Return a ModuleWrapper-wrapped instance of the app module. The ModuleWrapper
    makes it easy to get to nested submodules through a dot notation. No need to
    do further importing.
    """
    def __init__(self):
        self.app_paths = {x.split('.')[-1]: x for x in settings.INSTALLED_APPS}

    def __getattr__(self, name):
        """
        If the package doesn't exist, then locate it, attach it and return it
        """
        try:
            packageString = self.app_paths[name]
            package = import_module(packageString)
            package = ModuleWrapper(package, packageString)
            setattr(self, name, package)
            return package
        except:
            raise ImportError("No app named '{}'".format(name))

class ModuleWrapper(object):
    def __init__(self, module, path):
        self.module = module
        self.path = path
        self.modules = {}

    def __getattribute__(self, val):
        modules = super(ModuleWrapper, self).__getattribute__("modules")
        module = super(ModuleWrapper, self).__getattribute__("module")
        path = super(ModuleWrapper, self).__getattribute__("path")
        if val in modules:
            return modules[val]
        try:
            out = getattr(module, val)
            if isinstance(out, ModuleType):
                return ModuleWrapper(out, path + '.' + val)
            else:
                return out
        except AttributeError as e:
            try:
                moduleString = path + '.' + val
                module = import_module(moduleString)
                module = ModuleWrapper(module, moduleString)
                modules[val] = module
                return module
            except:
                raise e

    def __repr__(self):
        module = super(ModuleWrapper, self).__getattribute__("module")
        return repr(module)


apps = Apps()