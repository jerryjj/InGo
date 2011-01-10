_registered_extensions = {}

def register(name, module):
    global _registered_extensions
    
    if not _registered_extensions.has_key(module):
        _registered_extensions[module] = []
    
    if not name in _registered_extensions[module]:
        _registered_extensions[module].append(name)