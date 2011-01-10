import ingo.web.application

import logging
log = logging.getLogger('ingo')

class MyApp(ingo.web.application.Application):
    """docstring for MyApp"""
    
    routes = {
        '/': [
            {
                'name': 'main',
                'url': '/',
                'controller': 'demo_controllers.main.Controller',
                'action': 'index'
            },
            {
                'name': 'message',                
                'collection_name': 'messages',
                'controller': 'demo_controllers.rest.Controller',
                #'path_prefix': 'rest'
            },
            {
                'name': 'main_action',
                'url': '/{action}',
                'controller': 'demo_controllers.main.Controller',
            },
            {
                'name': 'main_view',
                'url': '/{action}/{entry_id}',
                'controller': 'demo_controllers.main.Controller',
                'requirements': {
                    'action': 'view|edit'
                }
            },
        ]
    }
    
    def initialize(self):
        import demo_controllers.main
        #import demo_controllers.rest
        
        self.connect('main_view_formatted', '/entries/{entry_id:\d+}{.format}', controller=demo_controllers.main.Controller(), action='view')
        
        #self.dispatcher.controllers['message'] = demo_controllers.rest.Controller()
        #self.map.resource("message", "messages", path_prefix='rest')
        #Log the map
        #print self.map

if __name__ == "__main__":
    myapp = MyApp()
    myapp.run()