# -*- coding: utf-8 -*-

import webapp2
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)

class BaseHandler(webapp2.RequestHandler):
    def render_template(self, filename, params_dict):
        template = jinja_env.get_template(filename)
        return self.response.write(template.render(params_dict))

class VnosHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("vnos.html")
        return self.response.write(template.render({}))

class RezultatHandler(webapp2.RequestHandler):
    def post(self):
        sporocilo = self.request.get("sporocilo")
        return self.response.write(u"Vnesli ste sporočilo: %s" % sporocilo)

# URLs
app = webapp2.WSGIApplication([
    webapp2.Route('/', VnosHandler),
    webapp2.Route('/rezultat', RezultatHandler)
], debug=True)
