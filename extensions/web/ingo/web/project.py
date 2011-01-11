import ingo.project

import logging
log = logging.getLogger('web')

from ingo import config
from ingo.ext.web import findExtensions as web_findExtensions, getExtensionModule as web_getExtensionModule

import os
PROJ_PATH = os.path.realpath(os.path.dirname(__file__)+'/../')

class NoExtensionsAvailable(Exception): pass

class Project(ingo.project.Project):
    """docstring for Application"""
    _configurations = [["web", PROJ_PATH]]
    routes = {}
    
    def __init__(self):
        super(Application, self).__init__()
        self._available_extensions = web_findExtensions()
        if len(self._available_extensions) == 0:
            raise NoExtensionsAvailable()
        
        self.web_config = config.get('web', {})
        
        self._ext_name = self.web_config.get('preferred_extension', 'cherry')
        
        if self.web_config.has_key('use_extension'):
            self._ext_name = self.web_config.get('use_extension')
        
        if not self._ext_name in self._available_extensions:
            raise NoExtensionsAvailable("Selected extension %s not available" % self._ext_name)
        
        self._loadExtension(self._ext_name)
        
        self.initialize()
    
    def run(self):
        return self._ext.run()

    @property
    def env(self):
        return self._ext.env
        
    @property
    def request(self):
        return self._ext.request
    
    @property
    def dispatcher(self):
        return self._ext.dispatcher
        
    @property
    def map(self):
        return self._ext.map
        
    def connect(self, *args, **kwargs):
        return self._ext.connect(*args, **kwargs)
    
    def _loadExtension(self, name):
        classpath = web_getExtensionModule(name)
        exec "import %s" % classpath
        
        self._ext = eval(classpath).make(self, self.web_config.get("ext_%s" % name, {}))
