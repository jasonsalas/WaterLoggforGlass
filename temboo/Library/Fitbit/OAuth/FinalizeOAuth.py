# -*- coding: utf-8 -*-

###############################################################################
#
# FinalizeOAuth
# Completes the OAuth process by retrieving a Fitbit access token, token secret and encoded user id (UserID) for a user, after they have visited the authorization URL returned by the InitializeOAuth choreo and clicked "allow."
#
# Python versions 2.6, 2.7, 3.x
#
# Copyright 2014, Temboo Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
#
#
###############################################################################

from temboo.core.choreography import Choreography
from temboo.core.choreography import InputSet
from temboo.core.choreography import ResultSet
from temboo.core.choreography import ChoreographyExecution

import json

class FinalizeOAuth(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the FinalizeOAuth Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(FinalizeOAuth, self).__init__(temboo_session, '/Library/Fitbit/OAuth/FinalizeOAuth')


    def new_input_set(self):
        return FinalizeOAuthInputSet()

    def _make_result_set(self, result, path):
        return FinalizeOAuthResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return FinalizeOAuthChoreographyExecution(session, exec_id, path)

class FinalizeOAuthInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the FinalizeOAuth
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AccountName(self, value):
        """
        Set the value of the AccountName input for this Choreo. ((optional, string) Deprecated (retained for backward compatibility only).)
        """
        super(FinalizeOAuthInputSet, self)._set_input('AccountName', value)
    def set_AppKeyName(self, value):
        """
        Set the value of the AppKeyName input for this Choreo. ((optional, string) Deprecated (retained for backward compatibility only).)
        """
        super(FinalizeOAuthInputSet, self)._set_input('AppKeyName', value)
    def set_AppKeyValue(self, value):
        """
        Set the value of the AppKeyValue input for this Choreo. ((optional, string) Deprecated (retained for backward compatibility only).)
        """
        super(FinalizeOAuthInputSet, self)._set_input('AppKeyValue', value)
    def set_CallbackID(self, value):
        """
        Set the value of the CallbackID input for this Choreo. ((required, string) The callback token returned by the InitializeOAuth Choreo. Used to retrieve the callback data after the user authorizes.)
        """
        super(FinalizeOAuthInputSet, self)._set_input('CallbackID', value)
    def set_ConsumerKey(self, value):
        """
        Set the value of the ConsumerKey input for this Choreo. ((required, string) The Consumer Key provided by Fitbit.)
        """
        super(FinalizeOAuthInputSet, self)._set_input('ConsumerKey', value)
    def set_ConsumerSecret(self, value):
        """
        Set the value of the ConsumerSecret input for this Choreo. ((required, string) The Consumer Secret provided by Fitbit.)
        """
        super(FinalizeOAuthInputSet, self)._set_input('ConsumerSecret', value)
    def set_OAuthTokenSecret(self, value):
        """
        Set the value of the OAuthTokenSecret input for this Choreo. ((required, string) The oauth_token_secret retrieved during the OAuth process. This is returned by the InitializeOAuth Choreo.)
        """
        super(FinalizeOAuthInputSet, self)._set_input('OAuthTokenSecret', value)
    def set_Timeout(self, value):
        """
        Set the value of the Timeout input for this Choreo. ((optional, integer) The amount of time (in seconds) to poll your Temboo callback URL to see if your app's user has allowed or denied the request for access. Defaults to 20. Max is 60.)
        """
        super(FinalizeOAuthInputSet, self)._set_input('Timeout', value)

class FinalizeOAuthResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the FinalizeOAuth Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_AccessTokenSecret(self):
        """
        Retrieve the value for the "AccessTokenSecret" output from this Choreo execution. ((string) The Access Token Secret retrieved during the OAuth process.)
        """
        return self._output.get('AccessTokenSecret', None)
    def get_AccessToken(self):
        """
        Retrieve the value for the "AccessToken" output from this Choreo execution. ((string) The Access Token retrieved during the OAuth process.)
        """
        return self._output.get('AccessToken', None)
    def get_UserID(self):
        """
        Retrieve the value for the "UserID" output from this Choreo execution. ((string) The user's encoded id associated with the access token that is being retrieved.)
        """
        return self._output.get('UserID', None)

class FinalizeOAuthChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return FinalizeOAuthResultSet(response, path)
