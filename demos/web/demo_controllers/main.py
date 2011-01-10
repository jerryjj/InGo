from ingo.web.utils.url import url
from ingo.web.controller import BaseController

from ingo.ext.templating.engine import output, render

class Controller(BaseController):    
    def index(self):
        view_url = url("main_view", action="view", entry_id=1)
        print self.request
        trans = _('Hello, World!')
        #trans = ''
        return "%s. This is the main page <a href=\"%s\">static file</a> <a href=\"%s\">view 1</a>" % (trans, url('/static/test.txt'), view_url)
    def view(self, entry_id, format='html'):
        return "view entry no. %s in format (%s)" % (entry_id, format)
    
    @output('delete.html')
    def delete(self):
        return render(title = 'delete')