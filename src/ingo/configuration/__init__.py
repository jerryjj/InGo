import copy
from paste.config import DispatchingConfig
config = DispatchingConfig()

class InGoConfig(dict):
    defaults = {
        'debug': {
            'enabled': False
        },
        'project': {
            'package': None,
            'paths': {
                'root': None,
                'config': None,
                'controllers': [],
                'templates': [],
                'static_files': []
            }
        }
    }
    
    def get(self, name, default=None):
        if name.find('.') > -1:
            parts = name.split('.')
            cnt = len(parts)
            for i, k in enumerate(parts):
                if i == 0:
                    try:
                        v = super(InGoConfig, self).get(k, {})
                    except AttributeError:
                        raise AttributeError('%s is not set in path (%s)' % (k, name))
                    continue
                try: v = v.get(k)
                except AttributeError, e:
                    if i == cnt-1:
                        if default: return default
                    raise AttributeError('%s is not set in path (%s)' % (parts[i-1], name))
            return v
        return super(InGoConfig, self).get(name, default)
    
ingo_config = InGoConfig()

ingo_config.update(copy.deepcopy(InGoConfig.defaults))
config.push_process_config(ingo_config)

class ConfigurationException(Exception): pass
class ConfigurationImplementationError(ConfigurationException): pass
class ConfigurationNotFound(ConfigurationException): pass

class Configuration(object):
    """docstring for Configuration"""
    def __init__(self, implementation="yml"):
        super(Configuration, self).__init__()
        
        self._impl_name = implementation
        self._impl = None
        
        self._config = dict()
        self._config_parts = dict()
        
        self._prepareImplementation()
    
    def loadExtension(self, name, path):
        try:
            self.load("default", path, local=False)
        except ConfigurationNotFound:
            pass
        
        self.load(name, path, local=False)
        
    def load(self, name, path=None, update_global=False, local=True):        
        source = self._impl.prepareSource(name, path)
        
        if not self._impl.exists(source):
            raise ConfigurationNotFound("No config source %s found" % source)
        
        content = self._impl.load(source)
        
        self._config_parts[name] = {
            'path': path,
            'source': source
        }
        
        is_local = False
        if name.count(".local"):
            name = name.split(".local")[0]
            is_local = True
        
        if name == 'default':
            conf = self.merge(config.copy(), content)
            config.update(conf)
        else:            
            if not config.has_key(name):
                config[name] = {}
            conf = self.merge(config[name].copy(), content)
            config[name].update(conf)
            
            if update_global:
                conf = self.merge(config.copy(), content)
                config.update(conf)
        
        if local and not is_local:
            local_content = self.load(name+".local", path, update_global, local)
            content = self.merge(local_content.copy(), content)
        
        return content
    
    def dump(self, target=None):
        pass
        
    def dumpPart(self, name, path=None, target=None):
        source = self._impl.prepareSource(name, path)
    
    def update(self, new_config, section=None):
        if not section:
            self._config = self.merge(self._config, new_config)
        else:
            self._config[section] = self.merge(self._config[section], new_config)
    
    def merge(self, original, override):
        if not isinstance(original, dict):
            original = dict()

        if not isinstance(override, dict):
            return override

        for key, value in override.iteritems():
            if isinstance(value, dict):
                original[key] = self.merge(original.get(key, dict()), value)
            else:
                original[key] = value

        return original
    
    def _prepareImplementation(self):
        impl_classpath = "ingo.configuration.%s" % self._impl_name
        try:
    	    exec "import %s" % impl_classpath
    	except ImportError, e:
    	    raise ConfigurationImplementationError("Could not load implementation module %s" % impl_classpath)
    	
    	try:
    	    self._impl = eval(impl_classpath).Implementation()
    	except Exception, e:
    	    raise ConfigurationImplementation(str(e))
                
    def get(self, name, default=None):
        return self._config.get(name, default)
    
    def has_key(self, name):
        return self._config.has_key(name)
    
    def __str__(self):
        return str(self._config)
