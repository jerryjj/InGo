from zope.interface import Interface

class IPlugin(Interface):
    """ Plugin interface
    """

    def __init__(self, config=None):
        """ Init
        """
    
    def initialize(self):
        """ Initialize plugin. This will be called from __init__
        """

    def load(self):
        """ Load
        """
        
    def unload(self):
        """ Load
        """

    def activate(self):
        """ Activate
        """
        
    def deactivate(self):
        """ Deactivate
        """
        
    def isActivate(self):
        """ Is activate
        """