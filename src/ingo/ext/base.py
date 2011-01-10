from ingo.core.ext import register
from ingo.ext.interfaces import IExtension
from zope.interface import implements

class ExtensionMeta(type):
    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls, *args, **kwargs)
        obj.__init__(*args, **kwargs)
        
        register(cls.__name__, cls.__module__)
        
        return obj

class Extension(object):
    implements(IExtension)    
    __metaclass__ = ExtensionMeta