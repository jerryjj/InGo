class QueueStorage(object):
    """docstring for QueueStorage"""
    def __init__(self):
        super(QueueStorage, self).__init__()
        
class PickleStorage(QueueStorage):
    """docstring for PickleStorage"""
    def __init__(self):
        super(PickleStorage, self).__init__()


class DBStorage(QueueStorage):
    """docstring for DBStorage"""
    def __init__(self):
        super(DBStorage, self).__init__()
        
__all__ = ['PickleStorage', 'DBStorage']