# Copyright (C) 2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'alainv@google.com (Alain Vongsouvanh)'

""" OAuth 2.0 handlers """

import logging
import webapp2
from urlparse import urlparse

from oauth2client.appengine import StorageByKeyName
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from model import Credentials

import util

SCOPES = ('https://www.googleapis.com/auth/glass.timeline https://www.googleapis.com/auth/userinfo.profile')
			
CLIENT_SECRETS = 'client_secrets.json'
			
class OAuthBaseRequestHandler(webapp2.RequestHandler):
	""" base request handler for OAuth 2.0 flow """
	
	def create_oauth_flow(self):
		""" create an OAuth 2.0 flow controller """
		flow = flow_from_clientsecrets(CLIENT_SECRETS, scope=SCOPES)
		pr = urlparse(self.request.url)
		flow.redirect_uri = '%s://%s/oauth2callback' % (pr.scheme, pr.netloc)
		return flow
		
	
class OAuthCodeRequestHandler(OAuthBaseRequestHandler):
	""" request handler for a OAuth 2.0 auth request """
	
	def get(self):
		flow = self.create_oauth_flow()
		flow.params['approval_prompt'] = 'force'
		
		# create the redirect URI by performing Step 1 of the OAuth 2.0 web server flow
		uri = flow.step1_get_authorize_url()
		
		# perform the redirect
		self.redirect(str(uri))
		
		
class OAuthCodeExchangeHandler(OAuthBaseRequestHandler):
	""" request handler for OAuth 2.0 code exchange """
	
	def get(self):
		""" handle code exchange """
		code = self.request.get('code')
		if not code:
			return None
		
		oauth_flow = self.create_oauth_flow()
		
		# perform the exchange of the code. if there is a failure with the exchange, return None
		try:
			creds = oauth_flow.step2_exchange(code)
		except FlowExchangeError:
			return None
			
		users_service = util.create_service('oauth2', 'v2', creds)
		user = users_service.userinfo().get().execute()
		userid = user.get('id')
		
		# store the credentials in the data store using the 'userid' as the key.
		StorageByKeyName(Credentials, userid, 'credentials').put(creds)
		logging.info('Successfully stored credentials for user: %s', userid)
		util.store_userid(self, userid)
		
		self.perform_post_auth_tasks(userid, creds)
		self.redirect('/')
		
	def perform_post_auth_tasks(self, userid, creds):
		""" perform housekeeping tasks """
		mirror_service = util.create_service('mirror', 'v1', creds)
		
		# insert a TIMELINE subscription
		timeline_subscription_body = {
			'collection' : 'timeline',
			'userToken' : userid,
			'verifyToken' : 'sideout92',
			'callbackUrl' : util.get_full_url(self, '/notify')
		}
		
		mirror_service.subscriptions().insert(body=timeline_subscription_body).execute()
		
		waterlogg_image = util.get_full_url(self, '/static/images/waterlogg.jpg')
		
		# insert a sharing contact for WaterLogg
		waterlogg_body = {
			'id' : 'waterlogg',
			'displayName' : 'WaterLogg',
			'imageUrls' : [ waterlogg_image ],
			'acceptCommands' : [ { 'type' : 'POST_AN_UPDATE' } ]
		}
		
		mirror_service.contacts().insert(body=waterlogg_body).execute()
		
		# insert a greeting card
		timeline_item_body = {
			'html' : '<article><figure><img src="%s"/></figure><section><p class="text-small">Thanks for enabling Waterlogg!</p><p class="text-x-small">Usage: "OK Glass...Post an update...Waterlogg"</p></section><footer>Enjoy!</footer></article>' % waterlogg_image,
			'notification' : { 'level' : 'DEFAULT' },
			'menuItems' : [ { 'action' : 'DELETE' } ]		
		}
		
		mirror_service.timeline().insert(body=timeline_item_body).execute()
		
		
OAUTH_ROUTES = [
	('/auth', OAuthCodeRequestHandler),
	('/oauth2callback', OAuthCodeExchangeHandler)
]