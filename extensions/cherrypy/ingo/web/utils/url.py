import routes
import cherrypy

def redirect(*args, **kwargs):
    _url = kwargs.pop('url', None)
    internal = kwargs.pop('internal', True)
    
    if not _url:
        _url = routes.url_for(*args, **kwargs)
    
    # """Raise InternalRedirect or HTTPRedirect to the given url."""
    if internal:
        raise cherrypy.InternalRedirect(_url)
    else:
        raise cherrypy.HTTPRedirect(_url)
    #cherrypy.tools.redirect(url=url, internal=internal)

def url(*args, **kwargs):
    return routes.url_for(*args, **kwargs)
    # if len(args) == 1 and len(kwargs) == 0 and type(args[0]) in (str, unicode):
    #     return cherrypy.url(args[0])
    # else:
    #     return cherrypy.url(routes.url_for(*args, **kwargs))
