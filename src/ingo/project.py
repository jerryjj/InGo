import ingo
import ingo.plugin
import ingo.log
from ingo import config
from ingo.configuration import Configuration, ConfigurationNotFound

import os, sys
from pkg_resources import resource_filename

from unipath import Path

class Project(object):
    """docstring for Project"""
    _configurations = []
    def __init__(self):
        super(Project, self).__init__()
        ingo.register_project(self)
        
        self._ingo_root = self.resolvePathForName(__name__)
        self._default_config_path = Path(self._ingo_root)
        self.base_path = Path(sys.path[0])
        self._config_path = self.base_path.child('config')
        
        self._config_loader = Configuration(implementation="yml")
        
        self._loadInitialConfiguration()
        self._loadInitialUserConfiguration()
        
        config['project']['paths']['config'] = self._config_path
        config['project']['paths']['root'] = self.base_path
        
        self._prepareLoggers()
        
        ingo.features.load()
        # print ingo.features
        # print "has web app feature", ingo.features.has('web', 'application')
        # print "has web error controller", ingo.features.has('web', 'controller.error')
        
        self._preparePlugins()
    
    def initialize(self):
        pass
    
    @classmethod
    def resolvePathForName(cls, name, path='/'):
        return resource_filename(name, path)
    
    def _loadInitialConfiguration(self):
        self._config_loader.load("default", self._default_config_path)
        
        for name in self._configurations:
            conf_name = name
            conf_path = self._default_config_path
            if type(name) is list:
                conf_name = name[0]
                conf_path = name[1]
            self._config_loader.load(conf_name, conf_path)
    
    def _loadInitialUserConfiguration(self):
        if not self._config_path:
            return

        try:
            self._config_loader.load("default", self._config_path)
        except ConfigurationNotFound, e:
            pass
        
        for name in self._configurations:
            conf_name = name
            if type(name) is list:
                conf_name = name[0]
                
            try:
                self._config_loader.load(conf_name, self._config_path)
            except ConfigurationNotFound, e:
                pass
    
    def _prepareLoggers(self):
        ingo.log.loadFromConfig(config.get("logging"))
        
        self.log = ingo.log.getLogger('ingo')
        
    def _preparePlugins(self):
        """docstring for _preparePlugins"""
        load_all = config.get('plugins.load_all', False)
        
        if load_all:
            ingo.plugin.loader.loadAll()
        
        if not load_all and not config.get('plugins.enabled', None):
            return
        
        for name, activate in config.get('plugins.enabled').iteritems():
            ingo.plugin.loader.load(name)
            if activate:
                ingo.plugin.loader.activate(name)
        