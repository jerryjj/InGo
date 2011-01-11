import cherrypy

from ingo import config
from ingo.configuration import Configuration, ConfigurationNotFound
from ingo.web.utils.url import url

import logging
log = logging.getLogger('web')

import os, sys
from unipath import Path

import gettext

def list_features():
    return [
        'ext.cherrypy',
        'utils.url',
        'utils.url.redirect',
        'utils.request',
        'controller.base',
    ]

def getDefaultConfigPath():
    return Path(__file__).absolute().ancestor(4)

class InGoMultilangApp(cherrypy.Application):
    def __init__(self, lang, localedir, script_name="", app_config=None):
        self.lang = lang
        self.locale_dir = localedir
        self.domain = 'default'
        self.domains = []
        self.translations = {}
        
        self.default_dict = dict(
            app = self
        )
        
        self.registerTranslationDomain(self.domain, languages=[lang])
        
        if config.get('web.templating.enabled', False):
            self._prepareTemplating()
        
        cherrypy.Application.__init__(self, None, script_name, app_config)
    
    @property
    def tpl_context(self):
        d = self.default_dict.copy()
        d.update(dict(
            url = url
        ))
        return d
    
    def registerTranslationDomain(self, domain, locale_dir=None, languages=None):
        if not locale_dir:
            locale_dir = self.locale_dir
        if not languages:
            languages = [self.lang]
        
        if not domain in self.domains:
            self.domains.append(domain)
        self.translations[domain] = gettext.translation(domain, locale_dir, languages=languages, fallback=True)
    
    def activeTranslationDomain(self, domain=None):
        if not domain:
            return self.domain
        if self.domain in self.domains:
            self.domain = domain
        else:
            raise AttributeError("Domain %s not registered" % domain)
    
    def _prepareTemplating(self):
        try:
            #from ingo.ext.templating import findExtensions as tpl_findExtensions, getExtensionModule as tpl_getExtensionModule
            from ingo.ext.templating import engine
        except ImportError, e:
            raise ImportError("InGo templating is not installed! (%s)" % e)
        
        self.tpl = engine.get_instance(self)
    
    def __call__(self, environ, start_response):
        if environ['PATH_INFO'] == '':
            environ['PATH_INFO'] = '/'
        
        self.translations[self.domain].install()
        return self.wsgiapp(environ, start_response)

class CherryPyWebExt(object):
    """docstring for CherryPyWebExt"""
    def __init__(self, parent, override_config=None):
        super(CherryPyWebExt, self).__init__()
        log.debug("CherryPyWebExt::__init__")
        self.parent = parent
        self.dispatcher = None
        
        self._loadConfiguration()
        
        if override_config:
            config['cherrypy'].update(override_config.copy())
        
        cherrypy.config.update(config.get('cherrypy.global', {}))            

        if not cherrypy.tools.staticdir.root:
            cherrypy.config.update({
                'tools.staticdir.root': self.parent.base_path
            })
        
        route_mounts = config.get('cherrypy.mounts')
        self._route_config = {}
        
        for base_path, routes in self.parent.routes.iteritems():
            if not self._route_config.has_key(base_path):
                self._route_config[base_path] = {}
            self._route_config[base_path].update({
                'request.dispatch': self._setup_routes(routes)
            })
        
        for point, conf in route_mounts.iteritems():
            if not self._route_config.has_key(point):
                self._route_config[point] = {}
            self._route_config[point].update(conf)
        
        multilang_config = config.get('cherrypy.multilang')
        localedir = os.path.join(self.parent.base_path, 'i18n')
        
        if multilang_config.get('enabled'):
            for key, conf in multilang_config.get('map').iteritems():                
                cherrypy.tree.apps['/'+key] = InGoMultilangApp(conf.get('lang'), localedir, conf.get('path'), self._route_config)
                if multilang_config.get('default') == key:
                    cherrypy.tree.apps[''] = InGoMultilangApp(conf.get('lang'), localedir, config.get('cherrypy.root_path'), self._route_config)
        else:
            cherrypy.tree.apps[''] = InGoMultilangApp(multilang_config.get('default'), localedir, config.get('cherrypy.root_path'), self._route_config)
            #cherrypy.tree.mount(None, script_name=self.config.get('root_path'), config=self._route_config)
        
        self._env = {
            'app': cherrypy.request.app,
            'ingo_app': self.parent,
            'basedir': self.parent.base_path
        }
    
    @property
    def env(self):
        return self._env

    @property
    def request(self):
        return cherrypy.request
        
    @property
    def map(self):
        return self.dispatcher.mapper
        
    def run(self):
        cherrypy.quickstart()
    
    def _loadConfiguration(self):
        self._config_loader = Configuration(implementation="yml")
        self._config_loader.load("cherrypy", getDefaultConfigPath()) #self.parent.resolvePathForName(__name__)

        try:
            self._config_loader.load("cherrypy", self.parent._config_path)
        except ConfigurationNotFound, e:
            log.error(e)
    
    def _setup_routes(self, routes):
        self.dispatcher = cherrypy.dispatch.RoutesDispatcher()

        self.dispatcher.mapper.minimization = config.get('route_mapper_minimization', True)
        self.dispatcher.mapper.explicit = config.get('route_mapper_explicit', False)

        self._set_error_controller()
        
        controllers = {}
        
        for route in routes:
            module = None
            controller_name = None
            if route.has_key('controller'):
                controller_name = route.get('controller')
                
            if controller_name and controller_name.count("."):
                module = ".".join(controller_name.split(".")[:-1])
                try:
            	    exec "import %s" % module
            	except ImportError, e:
            	    log.error("Failed to import route module %s. Ignored!" % module)
            	    continue

            is_resource = False
            if route.has_key('collection_name'):
                is_resource = True
            
            kwargs = {}
            if controller_name:
                if not controllers.has_key(controller_name):
                    controllers[controller_name] = eval(controller_name)()
                
                if is_resource:
                    self.dispatcher.controllers[route.get('collection_name', None)] = controllers[controller_name]
                else:
                    kwargs['controller'] = controllers[controller_name]
            
            kw_keys = ['action', 'conditions', 'requirements']
            if is_resource:
                kw_keys += ['collection', 'member', 'new', 'path_prefix', 'name_prefix', 'parent_resource']
            
            for kwk in kw_keys:
                if route.has_key(kwk):
                    kwargs[kwk] = route.get(kwk)
            
            if is_resource:                                    
                self.dispatcher.mapper.resource(route.get('name', None), route.get('collection_name', ''), **kwargs)
            else:
                self.dispatcher.connect(route.get('name', None), route.get('url', ''), **kwargs)
            
        if config.get('append_default_routes', True):
            self.dispatcher.mapper.connect('_default', '/:controller/:action')
            self.dispatcher.mapper.connect('_default_with_id', '/:controller/:action/:id')
        
        self._log_routing_table()
        
        return self.dispatcher
    
    def _set_error_controller(self):
        from ingo.web.controllers import ErrorController
        
        error_controller = ErrorController()
        
        if config.has_key('web.error_controller'):
            error_controller_name = config.get('web.error_controller')
            
            if error_controller_name.count("."):
                module = ".".join(error_controller_name.split(".")[:-1])
                try:
            	    exec "import %s" % module
            	except ImportError, e:
            	    log.error("Failed to import error module %s. Ignored!" % module)
            error_controller = eval(error_controller_name)()
        
        self.dispatcher.connect('error', '/error/:action', controller=error_controller)
        self.dispatcher.connect('error_id', '/error/:action/:id', controller=error_controller)        
    
    def connect(self, *args, **kwargs):
        self.dispatcher.connect(*args, **kwargs)
        self._log_routing_table()
        
    # def extend_map(self, routes, prefix):
    #     self.dispatcher.mapper.extend(routes, prefix)
    #     self._log_routing_table()
        
    def _log_routing_table(self):
        log.debug("Current routes table:")
        log.debug(self.dispatcher.mapper)

def make(parent, config=None):
    ext = CherryPyWebExt(parent, config)
    
    return ext
    