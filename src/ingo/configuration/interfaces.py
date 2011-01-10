from zope.interface import Interface

class IConfigurationImpl(Interface):
    """ Configuration implementation interface
    """

    def prepareSource(self, name, path=None):
        """ Method prepare config source so it can be passed to load
        """
    
    def exists(self, source):
        """ Method to check if given config source is found
        """
    
    def load(self, source):
        """ Method to load and unserialize given config to dict
        """
    
    def dump(self, config, target=None):
        """ Method to serialize given config
        """