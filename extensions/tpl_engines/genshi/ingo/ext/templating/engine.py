from ingo import config
from ingo.web.utils import request, thread_data

from genshi.core import Stream
from genshi.output import encode, get_serializer
from genshi.template import TemplateLoader, Context

import copy

_instance = None

def list_features():
    return [
        'ext.genshi',
        'engine',
        'engine.output',
        'engine.render'
    ]

def get_instance(app):
    global _instance
    if not _instance: _instance = Engine(app, config.get('web.templating.genshi_config', {}))
    return _instance

class Engine(object):
    """docstring for Engine"""
    defaults = {
        'auto_reload': False,
        'search_paths': ['./templates']        
    }
    
    def __init__(self, app, conf=None):
        super(Engine, self).__init__()
        self.app = app
        self.config = conf or {}
        self.config.update(copy.deepcopy(Engine.defaults))
        
        paths = self.config.get('search_paths')
        for i,p in enumerate(paths):
            if p.find('./') == 0:
                paths[i] = p.replace('./', config['project']['paths']['root']+'/')
        self._loader = TemplateLoader(paths, auto_reload=True)
        
        self.method = "xhtml"
        self.doctype = "xhtml-transitional"
    
    def add_search_path(self, path):
        """Adds a directory to the template loader search path.
        You can specify templates by base name as long as the directories
        in which they reside are in the search path.
        """
        if path not in self._loader.search_path:
            self._loader.search_path.append(path)
    
    def load(self, filename):
        return self._loader.load(filename)
    
    def page(self, tpl, data):
        """Loads a Genshi template and returns its output as
        an XHTML page, taking care of some details.

        - tpl is a path, relative to the app directory.
        - data is a dictionary to populate the template instance.
        """
        if isinstance(data, basestring):
            return data
        t = self._loader.load(tpl)
        return t.generate(**self.app.todict(**data)).render(method=self.method, doctype=self.doctype, encoding="utf-8")
    
    def render(self, *args, **kwargs):
        """Function to render the given data to the template specified via the
        ``@output`` decorator.
        """
        if args:
            assert len(args) == 1, \
                'Expected exactly one argument, but got %r' % (args,)
            template = self._loader.load(args[0])
        else:
            template = thread_data.template
        ctxt = Context(**self.app.tpl_context)
        ctxt.push(kwargs)
        return template.generate(ctxt)

def render(*args, **kwargs):
    return request.app.tpl.render(*args, **kwargs)

def output(filename, method='html', encoding='utf-8', **options):
    """Decorator for exposed methods to specify what template they should use
    for rendering, and which serialization method and options should be
    applied.
    """
    def decorate(func):
        def wrapper(*args, **kwargs):
            thread_data.template = request.app.tpl.load(filename)
            opt = options.copy()
            if method == 'html':
                opt.setdefault('doctype', 'html')
            serializer = get_serializer(method, **opt)
            stream = func(*args, **kwargs)
            if not isinstance(stream, Stream):
                return stream
            return encode(serializer(stream), method=serializer,
                          encoding=encoding)
        return wrapper
    return decorate