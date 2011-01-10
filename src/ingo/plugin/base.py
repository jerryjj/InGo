from ingo.plugin.interfaces import IPlugin
from zope.interface import implements

class Plugin(object):
    implements(IPlugin)
    __name__ = __name__
    
    def __init__(self, config=None):
        self.override_config = config
        self.config = dict()
        
        self._activated = False
        
        self.initialize()
        
    def load(self):
        pass

    def unload(self):
        pass

    def activate(self):
        self._activated = True

    def deactivate(self):
        self._activated = False

    def isActive(self):
        return self._activated