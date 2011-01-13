import ingo.project

from ingo.ext.sms import MessageSender, Contact, Message, MessageCollection

import logging
log = logging.getLogger('ingo')

class MyProj(ingo.project.Project):
    """docstring for MyProj"""
    def __init__(self):
        super(MyProj, self).__init__()
        
        self.sms_sender = MessageSender()
        
        msg = Message(sender=Contact('InGo', None), receiver=Contact(None, '+358456365097'), content='Hello, World')
        coll = MessageCollection()
        coll.append(msg)
        
        msg.set('content', msg.get('content') + '!')
        msg.set('sender.name', msg.get('sender.name') + '!')
        
        coll.append(Message(sender=Contact('InGo', '1234'), receiver=Contact(None, '123456789'), content='Hello'))
        
        coll[1].set('receiver.number', '1234567890')
        
        print "Message:"
        print msg
        print "MessageCollection:"
        print coll
        
        print "findBy:"
        print coll.findBy('receiver', '1234567890')
        
        #self.sms_sender.queue.push(coll)"
        #self.sms_sender.queue.load()
        
        self.sms_sender.quickSend(msg)
        #self.sms_sender.quickSend(coll)
        
    def initialize(self):
        pass
    
    def doSend(self):
        pass

if __name__ == "__main__":
    project = MyProj()
    project.doSend()