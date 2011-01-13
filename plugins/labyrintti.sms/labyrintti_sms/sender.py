from ingo.utils import dottedKeyFromDict 
from ingo.ext.sms import Message

from ingo.ext.sms.plugins import SenderPlugin

import logging
log = logging.getLogger('sms')

import httplib2
import urllib

class LabyrinttiSender(SenderPlugin):
    defaults = {
        'authentication': {
            'username': None,
            'password': None
        },
        'connection': {
            'secure': False,
            'host': 'gw.labyrintti.com',
            'port': 28080,
            'path': '/sendsms'
        }
    }
    
    message_properties = [
    ]
    message_keys = {
        'user': None,
        'source': None,
        'source-name': None,
        'dest': '',
        'text': '',
        'binary': None,
        'class': 'normal'
    }
    message_map = {
        'sender.name': 'source-name',
        'sender.number': 'source',
        'receiver.number': 'dest',
        'content': 'text',
    }
    
    def initialize(self):
        if not self.config['authentication']['username']:
            raise AttributeError("No username defined for sender")
        if not self.config['authentication']['password']:
            raise AttributeError("No password defined for sender")
        
        self.message_keys['user'] = self.config['authentication']['username']
        self.message_keys['password'] = self.config['authentication']['password']
    
    def process(self, msg):
        log.debug("Processing %s" % msg)
        
        if not isinstance(msg, Message):
            log.error("Message %s was not instance of ingo.ext.sms.Message" % msg)
            return False
        
        try:
            msg.validate(self.message_properties)
        except AttributeError, e:
            log.error("Validation failed on message %s" % msg)
            return False
        
        body = urllib.urlencode(self._prepareMessage(msg.properties))
        h = httplib2.Http()
        
        h.add_credentials(self.config['authentication']['username'], self.config['authentication']['password'])
        #h.follow_all_redirects = True
        headers = {'content-type':'application/x-www-form-urlencoded'}
        
        resp, content = h.request(self.generateUri(), method="POST", body=body, headers=headers)
        
        log.debug(resp)
        log.debug(content)
        
        return True
    
    def _prepareMessage(self, props):        
        prepared = SenderPlugin._prepareMessage(self, props)
        
        if prepared.has_key('as_binary'):
            prepared['binary'] = prepared['text']
            del prepared['text']
            del prepared['as_binary']
        
        if prepared.has_key('wap-url'):
            del prepared['text']
            del prepared['binary']
        
        return prepared
        