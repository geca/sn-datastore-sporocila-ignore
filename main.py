# -*- coding: utf-8 -*-

import webapp2
import jinja2
import os
from models import Sporocilo

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

        sporocilo_db = Sporocilo(vnos=sporocilo)
        sporocilo_db.put()

        return self.response.write(u"Vnesli ste sporočilo: %s" % sporocilo)

class SeznamHandler(webapp2.RequestHandler):
    def get(self):

        sporocila = Sporocilo.query().fetch()

        template = jinja_env.get_template("seznam.html")
        return self.response.write(template.render({"sporocila": sporocila}))

class PosameznoHandler(webapp2.RequestHandler):
    def get(self, sporocilo_id):

        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        template = jinja_env.get_template("sporocilo.html")
        return self.response.write(template.render({"sporocilo": sporocilo}))

class IzbrisiHandler(webapp2.RequestHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        sporocilo.key.delete()
        self.redirect("/seznam")

# URLs
app = webapp2.WSGIApplication([
    webapp2.Route('/', VnosHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/seznam', SeznamHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>', PosameznoHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>/izbrisi', IzbrisiHandler)
], debug=True)
