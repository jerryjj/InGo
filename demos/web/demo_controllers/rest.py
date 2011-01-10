from ingo.web.utils.url import redirect, url
class Controller:
    def index(self, format=None):
        if not format:
            redirect(controller="messages", format="html")
            #redirect(url(controller="messages", format="html"))
            #redirect(url(controller="messages", format="html"), internal=False)
        url_to_new = url(controller="messages", action="new", format="json")
        return "index in format %s (%s)" % (format, url_to_new)
    def create(self):
        return "create"
    def new(self, format='html'):
        return "new in format %s" % format
    def show(self, id, format='html'):
        return "show %s in format (%s)" % (id, format)
    def edit(self, id, format='html'):
        return "edit %s in format (%s)" % (id, format)
    def update(self, id):
        return "update %s" % id
    def delete(self, id):
        return "delete %s" % id