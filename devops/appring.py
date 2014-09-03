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

class Models(object):
    def __init__(self):
        self.cache = apps

    def __getattr__(self, name):
        """
        If the package doesn't exist, then locate it, attach it and return it
        """
        try:
            package = ModelPackage(self.cache.get_app(name), name, self)
            setattr(self, name, package)
            return package
        except:
            raise AttributeError("object 'Models' has no attribute '{}'".format(name))

    def _get_models(self, pkg):
        """
        get the models for a given package. used by Package children
        """
        return self.cache.get_models(pkg)


class ModelPackage(object):
    def __init__(self, package, name, parent):
        self.parent = parent
        self.package = package
        self.name = name

    def __getattr__(self, name):
        try:
            if not hasattr(self, 'models'):
                models = self.parent._get_models(self.package)
                self.models = {x.__name__: x for x in models}
            return self.models[name]
        except:
            raise AttributeError("module '{}' has no attribute {}".format(self.name, name))


class Apps(object):
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


models = Models()
apps = Apps()