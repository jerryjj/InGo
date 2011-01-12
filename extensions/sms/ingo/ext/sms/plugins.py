from ingo.plugin import Loader

loader = None

class SMSPluginLoader(Loader):
    def __init__(self):
        super(SMSPluginLoader, self).__init__()
        
        self._plugin_ep_group = "ingo.ext.sms.plugins"
loader = SMSPluginLoader()

class SenderPlugin(object):
    """docstring for SenderPlugin"""
    def __init__(self, config):
        super(SenderPlugin, self).__init__()
        self.config = self.defaults
        self.config.update(config.copy())
        
        self.initialize()
    
    def generateUri(self):
        uri = 'http'
        
        conf = self.config.get('connection')
        
        if conf.get('secure', False):
            uri += 's'
        uri += '://' + conf.get('host')
        
        if conf.has_key('port'):
            uri += ':' + str(conf.get('port'))

        if conf.has_key('path'):
            uri += conf.get('path')
        
        return uri
        