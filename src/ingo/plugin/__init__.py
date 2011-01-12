import os
from pkg_resources import iter_entry_points, resource_string, resource_filename

loader = None

class PluginNotLoaded(Exception): pass
class PluginNotActive(Exception): pass

class Loader(object):
    """docstring for Loader"""
    def __init__(self):
        super(Loader, self).__init__()
        
        self._plugin_ep_group = "ingo.plugin"
        self._plugin_ep_name = None
        self._plugins = {}
        
    def loadAll(self):
        """docstring for loadAll"""
        
        for entry_point in iter_entry_points(group=self._plugin_ep_group, name=self._plugin_ep_name):
            if not self._plugins.has_key(entry_point.name):
                self._loadByEntryPoint(entry_point)
    
    def loadByName(self, name):
        if self._plugins.has_key(name):
            return True
        
        entry_point = self._findEntryPointByName(name)
        if entry_point:
            return self._loadByEntryPoint(entry_point)
        
        return False
    
    def unloadByName(self, name):
        if not self._plugins.has_key(name):
            return True
        
        self._plugins[name].unload()
        del self._plugins[name]
        
        return True
    
    def getByName(self, name):
        if not self._plugins.has_key(name):
            raise PluginNotLoaded("Plugin %s has not been loaded" % name)
        if not self._plugins[name].isActive():
            raise PluginNotActive("Plugin is %s not active" % name)
        return self._plugins[name]
    
    def activateByName(self, name):
        if not self._plugins.has_key(name):
            return False
        self._plugins[name].activate()
        return True
        
    def deactivateByName(self, name):
        if not self._plugins.has_key(name):
            return False
        self._plugins[name].deactivate()
        return True
        
    def isActiveByName(self, name):
        if not self._plugins.has_key(name):
            return False
        return self._plugins[name].isActive()
        
    def isLoadedByName(self, name):
        if not self._plugins.has_key(name):
            return False
        return True
    
    def _findEntryPointByName(self, name):
        for entry_point in iter_entry_points(group=self._plugin_ep_group, name=self._plugin_ep_name):
            if entry_point.name == name:
                return entry_point
        return None
    
    def _loadByEntryPoint(self, entry_point):
        print "Loading plugin: %s" % entry_point.name
        
        cls = entry_point.load()

        # override_config = None    
        # override_config_path = os.path.join(os.path.abspath(_project_root + '/config/'), entry_point.name + ".yml")
        # 
        # if os.path.exists(override_config_path):
        #     override_config = load_config(override_config_path)

        #instance = cls(config=override_config)
        instance = cls()       
        
        instance.load()
        
        self._plugins[entry_point.name] = instance
        return True
    
    def get(self, name):
        return self.getByName(name)

    def activate(self, name):    
        return self.activateByName(name)

    def deactivate(self, name):
        return self.deactivateByName(name)

    def isActive(self, name):
        return self.isActiveByName(name)

    def isLoaded(self, name):
        return self.isLoadedByName(name)

    def load(self, name):
        return self.loadByName(name)

    def unload(self, name):
        return self.unloadByName(name)
loader = Loader()