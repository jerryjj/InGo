from ingo.plugin import Loader
from ingo.utils import dottedKeyFromDict 

loader = None

class SMSPluginLoader(Loader):
    def __init__(self):
        super(SMSPluginLoader, self).__init__()
        
        self._plugin_ep_group = "ingo.ext.sms.plugins"
loader = SMSPluginLoader()

class SenderPlugin(object):
    """docstring for SenderPlugin"""
    default = {}
    
    message_properties = [
    ]
    message_keys = {
    }
    message_map = {
    }

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
        
    def _prepareMessage(self, props):        
        prepared = {}
                
        for mk, rk in self.message_map.iteritems():            
            if mk.find('.') > 0: v = dottedKeyFromDict(mk, props)
            else: v = props[mk]
            if v != None:
                prepared[rk] = v

        for k, v in props.iteritems():            
            if self.message_keys.has_key(k):
                prepared[k] = v

        for k, default in self.message_keys.iteritems():
            if not prepared.has_key(k) and default != None:
                prepared[k] = default

        return prepared
        