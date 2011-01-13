from unipath import Path

import ingo
from ingo import config
from ingo.configuration import Configuration, ConfigurationNotFound
from ingo.utils import dottedKeyFromDict, updateDictByDottedKey

import ingo.ext.sms.plugins

from ingo.ext.sms.queue import createQueue

import logging
log = logging.getLogger('sms')

def list_features():
    return [
        "sender",
        "receiver"
        "message"
    ]

def getDefaultConfigPath():
    return Path(__file__).absolute().ancestor(3)

class _SMSBase(object):
    def __init__(self):
        self._loadConfiguration()
        
        self.sender_plugin_name = config.get('sms.sender.plugin', None)
        self.receiver_plugin_name = config.get('sms.receiver.plugin', None)
        self._plugin = None
        
        self._preparePlugin()
    
    def _preparePlugin(self):
        pass
    
    def _loadConfiguration(self):
        self._config_loader = Configuration(implementation="yml")
        self._config_loader.load("sms", getDefaultConfigPath())
        
        try:
            self._config_loader.load("sms", ingo.active_project._config_path)
        except ConfigurationNotFound, e:
            log.error(e)
        

class MessageSender(_SMSBase):
    """docstring for MessageSender"""
    def __init__(self):
        super(MessageSender, self).__init__()        
        
        self._prepareQueue()
        
    def quickSend(self, messages):
        if not type(messages) is list and not isinstance(messages, MessageCollection):
            messages = [messages]
        
        self.queue.push(messages)
        
        status = False
        
        for msg in self.queue.items():
            status = self._plugin.process(msg)
        
        self.queue.clear()
        
        return status
    
    def _prepareQueue(self):
        self.queue = createQueue(config.get('sms.queue.handler', 'LocalQueue'))
        
    def _preparePlugin(self):
        if not self.sender_plugin_name:
            raise Exception("No sender plugin have been defined for SMS")
        ingo.ext.sms.plugins.loader.load(self.sender_plugin_name)
        ingo.ext.sms.plugins.loader.activate(self.sender_plugin_name)
        self._plugin = ingo.ext.sms.plugins.loader.get(self.sender_plugin_name).sender
        
class MessageReceiver(_SMSBase):
    """docstring for MessageReceiver"""
    def __init__(self):
        super(MessageReceiver, self).__init__()

    def _preparePlugin(self):
        if not self.receiver_plugin_name:
            raise Exception("No receiver plugin have been defined for SMS")
        ingo.ext.sms.plugins.loader.load(self.receiver_plugin_name)
        ingo.ext.sms.plugins.loader.activate(self.receiver_plugin_name)
        self._plugin = ingo.ext.sms.plugins.loader.get(self.receiver_plugin_name).receiver

class Message(object):
    """docstring for Message"""
    def __init__(self, **kwargs):
        super(Message, self).__init__()

        self._properties = {
            'sender': Contact(None, None),
            'receiver': Contact(None, None),
            'content': ''
        }
        self._bindProperties(**kwargs)
        
        self.storage_plugin_name = config.get('sms.message.storage.plugin', None)
        self._storage_plugin = None
        self._preparePlugins()
    
    @property
    def properties(self):
        """docstring for properties"""
        return self._properties
    
    def validate(self, required, optionals=None):
        """docstring for validate"""
        for key in required:
            if not self._properties.has_key(key):
                raise AttributeError("Message is missing required property '%s'" % key)
    
    def get(self, key):
        if key.find('.') > 0: return dottedKeyFromDict(key, self._properties)
        return self._properties.get(key)
    
    def set(self, key, value):
        if key.find('.') > 0:
            v = updateDictByDottedKey(key, value, self._properties)
        else:
            self._properties[key] = value
    
    def _preparePlugins(self):
        if self.storage_plugin_name:
            ingo.ext.sms.plugins.loader.load(self.storage_plugin_name)
            ingo.ext.sms.plugins.loader.activate(self.storage_plugin_name)
            self._storage_plugin = ingo.ext.sms.plugins.loader.get(self.storage_plugin_name)

    def _bindProperties(self, **kwargs):
        for key, value in kwargs.iteritems():
            if key in ['sender', 'receiver'] and not isinstance(value, Contact):
                value = Contact(None, value)
            self._properties[key] = value

    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['_storage_plugin']
        return odict

    def __setstate__(self, dict):
        self.__dict__.update(dict)
        self._storage_plugin = None
        self._preparePlugins()
    
    def __repr__(self):
        rep = "Message("
        for k, v in self._properties.iteritems():
            rep += "%s=%s, " % (k, v)
        rep = rep[0:-2] + ")"
        
        return rep
        
class MessageCollection(list):
    """docstring for Message"""
    def __init__(self, *args, **kwargs):
        super(MessageCollection, self).__init__(*args, **kwargs)
    
    def findBy(self, prop, value):
        try:
            return filter(lambda msg: msg.get(prop) == value, self)
        except AttributeError, e:
            raise AttributeError("Message doesn't have property '%s'" % prop)
        
class Contact(object):
    """docstring for Contact"""
    def __init__(self, name, number):
        super(Contact, self).__init__()
        self.name = name
        self.number = number
    
    def get(self, key):
        return self.__dict__.get(key, None)
    
    def __repr__(self):
        return "Contact(name=%s, number=%s)" % (self.name, self.number)