try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

import os

def findExtensions():
    ext_dir = os.path.dirname(os.path.realpath(__file__))
    ext_dirs = [x for x in os.listdir(ext_dir) if not x.count(".")]
    return ext_dirs

def getExtensionModule(name):
    return __name__ + "." + name