# TODO: Implement this

from ingo.web.controller import BaseController

class ErrorController(BaseController):
    def index(self):
        return "Error"
    def show(self, id):
        return "Error %s" % id