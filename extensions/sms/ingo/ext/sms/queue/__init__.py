from ingo import config
from .storage import createStorage

class MessageQueue(object):
    """docstring for MessageQueue"""
    def __init__(self):
        super(MessageQueue, self).__init__()
        
        self._storage = createStorage(config.get('sms.queue.storage.handler', None))
    
    def load(self):
        pass
        
    def items(self):
        return []
    
    def add(self, item):
        pass
        
    def push(self, items):
        pass
    
    def clear(self):
        pass

class ExternalQueue(MessageQueue):
    """docstring for ExternalQueue"""
    def __init__(self):
        super(ExternalQueue, self).__init__()

class LocalQueue(MessageQueue):
    """docstring for LocalQueue"""
    def __init__(self):
        super(LocalQueue, self).__init__()
        self._items = []
        
    def load(self):
        self._items = self._storage.load()

    def add(self, item):
        self._items.append(item)
        self._storage.store(self._items)
    
    def push(self, items):
        self._items += list(items)
        self._storage.store(self._items)        

    def items(self):
        return self._items

    def clear(self):
        self._items = []
        self._storage.clear()

def createQueue(name):
    if name.count("."):
        module = ".".join(name.split(".")[:-1])
        try:
    	    exec "import %s" % module
    	except ImportError, e:
    	    log.error("Failed to import queue module %s. Ignored!" % module)
    	    raise e
    
    return eval(name)()
        
__all__ = ['createQueue', 'ExternalQueue', 'LocalQueue']