""" Request handler for '/notify' endpoint """

import io
import json
import logging
import webapp2

from datetime import date
from oauth2client.appengine import StorageByKeyName
from google.appengine.api import taskqueue

from temboo.Library.Fitbit.Foods import LogWater
from temboo.core.session import TembooSession

from model import Credentials
import util

class NotifyHandler(webapp2.RequestHandler):
	""" request handler for notifications from Google """
	def post(self):
		callback_body = self.request.body
		data = json.loads(callback_body)
		
		if data.get('collection') == 'timeline':
			""" hand the data off to the Google App Engine Task Queue at the '/queueHandler' endpoint for asynchronous processing """
			taskqueue.add(url='/queueHandler', params={ 'callback_body' : callback_body })	
			self.response.set_status(200)
		
class ProcessPing(webapp2.RequestHandler):
	""" Task Queue handler """
	def post(self):
		callback_body = self.request.get('callback_body')
		data = json.loads(callback_body)
	
		for user_action in data.get('userActions', []):
			""" update data via the Fitbit API """
			if user_action.get('type') == 'LAUNCH':			
				# fetch the timeline item
				itemId = data['itemId']
				self.mirror_service = util.create_service('mirror', 'v1', StorageByKeyName(Credentials, data['userToken'], 'credentials').get())
				item = self.mirror_service.timeline().get(id=itemId).execute()
				water_volume = item.get('text')
				
				# set Temboo parameters
				UNIT = 'fl oz'
				TIME_OFFSET = str(date.today())
				ACCESS_TOKEN = 'YOUR_TEMBOO_ACCESS_TOKEN'
				ACCESS_TOKEN_SECRET = 'YOUR_TEMBOO_ACCESS_TOKEN_SECRET'
				CONSUMER_SECRET = 'YOUR_TEMBOO_CONSUMER_SECRET'
				CONSUMER_KEY = 'YOUR_TEMBOO_CONSUMER_KEY'
				
				# create a session with the Temboo account details
				session = TembooSession('YOUR_APP_ARGUMENTS')

				# instantiate the Choreo
				logWaterChoreo = LogWater(session)

				# get an InputSet object for the Choreo
				logWaterInputs = logWaterChoreo.new_input_set()
				
				# Set credential to use for execution
				logWaterInputs.set_credential('YOUR_APP_CREDENTIAL_NAME')
				
				# values from the Tembloo app console
				logWaterInputs.set_Amount(water_volume)
				logWaterInputs.set_AccessToken(ACCESS_TOKEN)
				logWaterInputs.set_Date(TIME_OFFSET)
				logWaterInputs.set_AccessTokenSecret(ACCESS_TOKEN_SECRET)
				logWaterInputs.set_ConsumerSecret(CONSUMER_SECRET)
				logWaterInputs.set_ConsumerKey(CONSUMER_KEY)
				logWaterInputs.set_Unit(UNIT)
				
				#execute the Choreo
				logWaterResults = logWaterChoreo.execute_with_results(logWaterInputs)

				# log the Choreo outputs
				logging.info('WATER VOLUME POSTED TO FITBIT API: %s' % logWaterResults.get_Response())
				
				# insert a card thanking the user for the transaction
				waterlogg_image = util.get_full_url(self, '/static/images/waterlogg-welcome.jpg')
				
				confirmation_card = {
					'html' : '<article><figure><img src="%s"/></figure><section><p class="text-normal">You have logged <span class="green text-large"><strong>%s</strong></span> fluid ounces of water in Fitbit!</p></section></article>' % (waterlogg_image, water_volume),
					'notification' : { 'level' : 'DEFAULT' },
					'menuItems' : [ { 'action' : 'DELETE' } ]
				}
				
				self.mirror_service.timeline().insert(body=confirmation_card).execute()

				
NOTIFY_ROUTES = [
	('/notify', NotifyHandler),
	('/queueHandler', ProcessPing) 
]