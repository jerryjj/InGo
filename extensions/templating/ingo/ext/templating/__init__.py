# See http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

import os, sys
from ingo import config

def getExtensionModule(name):
    return __name__ + ".engines." + name + "_engine"