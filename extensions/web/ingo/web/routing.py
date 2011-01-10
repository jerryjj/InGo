from routes import Mapper
map = Mapper()

def createFromConfig(config):
    global map
    for id, conf in config.iteritems():
        kwargs = {}
        if not id:
            id = None
        
        if conf.has_key('controller'):
            kwargs['controller'] = conf.get('controller')
        if conf.has_key('action'):
            kwargs['action'] = conf.get('action')
        if conf.has_key('requirements'):                    
            kwargs['requirements'] = cong.get('requirements')
        
        map.connect(id, path, **kwargs)

__all__ = ["map"]
