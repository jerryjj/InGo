import sys
import logging

LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

_config = {}
_defaults = {}

_handlers = {}
_formatters = {}

class LogError(Exception): pass

import ingo.log.formatters

def getLogger(name):
    return logging.getLogger(name)

def loadFromConfig(config):
    if sys.version_info[1] > 6:
        logging.dictConfig(config)
        return

    global _defaults, _config
    
    if not config:
        return False
    
    _config = config
    
    _defaults['level'] = config.get('default_level', 'info')
    _defaults['logger'] = config.get('default_logger', 'root')
    _defaults['handler'] = config.get('default_handler', 'console')
    _defaults['formatter'] = config.get('default_formatter', 'generic')    
    
    root_logger = logging.getLogger('root')
    
    root_conf = config.get('root')
    
    level = LEVELS[_defaults['level']]
    if root_conf.has_key('level'):
        level = LEVELS[root_conf.get('level')]
    
    root_logger.setLevel(level)
    if root_conf.has_key('handlers'):
        for hname in root_conf.get('handlers'):
            root_logger.addHandler(_getHandler(hname, _getHandlerConfig(hname, config)))
    else:
        root_logger.addHandler(_getHandler(_defaults['handler'], _getHandlerConfig(_defaults['handler'], config)))
    
    for name, conf in config.get('loggers').iteritems():
        level = LEVELS[_defaults['level']]
        override_level = None
        if conf.has_key('level'):
            level = LEVELS[conf.get('level')]
            override_level = level
        
        logger = logging.getLogger(name)        
        logger.setLevel(level)
        
        if conf.has_key('handlers'):
            for hname in conf.get('handlers'):
                logger.addHandler(_getHandler(hname, _getHandlerConfig(hname, config), override_level))
        else:
            logger.addHandler(_getHandler(_defaults['handler'], _getHandlerConfig(_defaults['handler'], config)))
        
def _getHandlerConfig(name, config):
    handlers = config.get('handlers')
    if not handlers.has_key(name):
        raise LogError("No handler %s defined in config" % name)
    return handlers.get(name)
    
def _getFormatterConfig(name, config):
    formatters = config.get('formatters')
    if not formatters.has_key(name):
        raise LogError("No formatter %s defined in config" % name)
    return formatters.get(name)

def _getHandler(name, config, override_level=None):
    global _handlers
    
    if _handlers.has_key(name):
        if override_level:
            oh = _handlers[name]
            oh.setLevel(override_level)            
            _handlers[name + "_%s" % override_level] = oh
            return oh
        return _handlers[name]
    
    handler = eval(config.get('class'))(*eval(config.get('args', [])))
    
    level = LEVELS[_defaults['level']]
    if config.has_key('level'):
        level = LEVELS[config.get('level')]
    
    handler.setLevel(level)
    
    fname = config.get('formatter', _defaults['formatter'])    
    formatter = _getFormatter(fname, _getFormatterConfig(fname, _config))    
    handler.setFormatter(formatter)
    
    _handlers[name] = handler
    
    return _handlers[name]
    
def _getFormatter(name, config):
    global _formatters
    
    if _formatters.has_key(name):
        return _formatters[name]
    
    formatter = eval(config.get('class'))
    _formatters[name] = formatter(config.get('format'), config.get('datefmt', None))
    
    return _formatters[name]