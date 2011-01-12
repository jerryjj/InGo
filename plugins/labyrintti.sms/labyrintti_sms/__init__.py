from ingo import config
from ingo.plugin.base import Plugin

import logging
log = logging.getLogger('sms')

from labyrintti_sms.sender import LabyrinttiSender
from labyrintti_sms.receiver import LabyrinttiReceiver

class LabyrinttiSMSGateway(Plugin):
    """docstring for LabyrinttiSMSGateway"""
    
    __name__ = __name__

    def initialize(self):
        log.debug("LabyrinttiSMSGateway :: initialize")
        print self.config
        self.sender = LabyrinttiSender(config=config.get('sms.sender.config', {}))
        self.receiver = LabyrinttiReceiver(config=config.get('sms.receiver.config', {}))

    def load(self):
        log.debug("LabyrinttiSMSGateway :: load")

    def unload(self):
        log.debug("LabyrinttiSMSGateway :: unload")

    def activate(self):
        log.debug("LabyrinttiSMSGateway :: activate")
        super(LabyrinttiSMSGateway, self).activate()        

    def deactivate(self):
        log.debug("LabyrinttiSMSGateway :: deactivate")
        super(LabyrinttiSMSGateway, self).deactivate()        

    def isActive(self):        
        log.debug("LabyrinttiSMSGateway :: isActive %s" % self._activated)
        return super(LabyrinttiSMSGateway, self).isActive()
        

def make(conf=None):
    return LabyrinttiSMSGateway(config=conf)