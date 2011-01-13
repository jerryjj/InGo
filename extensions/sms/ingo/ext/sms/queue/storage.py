import ingo
from ingo import config
from unipath import Path

import logging
log = logging.getLogger('sms')

class QueueStorage(object):
    """docstring for QueueStorage"""
    def __init__(self):
        super(QueueStorage, self).__init__()
        
        self.config = config.get('sms.queue.storage.handler_config', {})
        
        self._plugin_name = config.get('sms.queue.storage.plugin', None)
        self._plugin = None
        self._preparePlugin()

    def _preparePlugin(self):
        pass
    
    def load(self):
        return []
    
    def store(self, items):
        return False
    
    def clear(self):
        pass

try:
    import cPickle as pickle
except ImportError:
    import pickle

class PickleStorage(QueueStorage):
    """docstring for PickleStorage"""
    def __init__(self):
        super(PickleStorage, self).__init__()
        
        self._prepareStorage()
    
    def _prepareStorage(self):
        default = Path(ingo.active_project.base_path, '/queue')
        self._storage_path = Path(self.config.get('path', default))
        self._storage_name = 'items.pckl'        
        
        if not self._storage_path.exists():
            raise Exception("PickleStorage storage path (%s) doesn't exist!" % self._storage_path)
        
    def load(self):
        storage_file = open(Path(self._storage_path, self._storage_name), 'rb')
        results = pickle.load(storage_file)
        storage_file.close()
        
        return results

    def store(self, items):
        storage_file = open(Path(self._storage_path, self._storage_name), 'wb')
        results = pickle.dump(items, storage_file)
        storage_file.close()
        
        return results

    def clear(self):
        self.store([])

class DBStorage(QueueStorage):
    """docstring for DBStorage"""
    def __init__(self):
        super(DBStorage, self).__init__()

    def _preparePlugin(self):
        if not self._plugin_name:
            raise Exception("No storage plugin have been defined for Queue Database Storage")
        ingo.ext.sms.plugins.loader.load(self._plugin_name)
        ingo.ext.sms.plugins.loader.activate(self._plugin_name)
        self._plugin = ingo.ext.sms.plugins.loader.get(self._plugin_name)

def createStorage(name):
    if name.count("."):
        module = ".".join(name.split(".")[:-1])
        try:
    	    exec "import %s" % module
    	except ImportError, e:
    	    log.error("Failed to import queue storage module %s. Ignored!" % module)
    	    raise e
    
    return eval(name)()

__all__ = ['createStorage', 'PickleStorage', 'DBStorage']