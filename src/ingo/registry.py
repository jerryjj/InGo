from pkg_resources import iter_entry_points

class Features(object):
    """docstring for Features"""
    def __init__(self):
        super(Features, self).__init__()
        self._registered = {}
        
    def load(self):        
        for entry_point in iter_entry_points(group='ingo.features', name=None):
            func = entry_point.load()
            self.register(entry_point.name, func())
            
    def register(self, major, minors):
        if not self._registered.has_key(major):
            self._registered[major] = []
        self._registered[major] += (minors)
    
    def has(self, major, minor):
        if self.major(major):
            return self.minor(minor)
        return False
    
    def major(self, name):
        return self._registered.has_key(name)
        
    def minor(self, name):
        for major, minors in self._registered.iteritems():
            if name in minors: return True
        
        return False
    
    @property
    def registred(self):
        return self._registered
    
    def __repr__(self):
        return "<Features %s>" % self._registered

features = Features()