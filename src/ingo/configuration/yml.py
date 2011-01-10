from yaml import load as yaml_load, dump as yaml_dump
try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import os

from ingo.configuration.interfaces import IConfigurationImpl
from zope.interface import implements

class Implementation(object):
    implements(IConfigurationImpl)
    
    def exists(self, source):
        if not os.path.exists(source):
            return False
        return True
        
    def prepareSource(self, name, path=None):
        fullname = name + ".yml"
        source = os.path.join(path, fullname)
        return source

    def load(self, source):
        results = yaml_load(file(source, 'r'), Loader=Loader)
        if not results:
            return dict()
        return results

    def dump(self, config, target=None):
        if target:
            target = file(target, 'r')
        return yaml_dump(config, target, Dumper=Dumper)