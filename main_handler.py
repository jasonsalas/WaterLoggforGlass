import jinja2
import logging
import webapp2
import os
import io

import httplib2
from oauth2client.appengine import StorageByKeyName

from model import Credentials
import util

from datetime import date, datetime, timedelta

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

	
class MainHandler(webapp2.RequestHandler):
	@util.auth_required
	def get(self):		
		# self.mirror_service is initialized in util.auth_required
		template_values = {
			'greeting' : 'Thanks for enabling',
			'voice_command' : 'Post an update',
			'glassware_title' : 'Waterlogg'
		}
		template = jinja_environment.get_template('templates/timeline.html')
		self.response.out.write(template.render(template_values))

	
MAIN_ROUTES = [
	('/', MainHandler)
]