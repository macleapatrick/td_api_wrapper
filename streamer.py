import asyncio
from warnings import WarningMessage
import websockets
from urllib.parse import urlencode, quote_plus

from datetime import datetime

import json

class Streamer:
    """
    """
    def __init__(
        self, 
        accountId=''
    ):
        self._accountId = accountId
        self._account = {}
        self._streamerInfo = {}
        self._requestid = 0

    @property
    def accountId(self):
        return self._accountId

    @accountId.setter
    def accountId(self, value):
        if self._accountId:
            raise ValueError("AccountId cannot be changed once set")
        else:
            self._accountId = value

    @staticmethod
    def convert_epoch(string):
        format = '%Y-%m-%dT%H:%M:%S%z'
        return int(datetime.strptime(string,format).timestamp() * 1000)

    def parse_principals(self, userPrincipals):
        self._account = self.get_account(userPrincipals)
        self._streamerInfo = userPrincipals['streamerInfo']

    def get_credentials(self):
        """
        return credentials in the form of a query string to be used for login requests
        """
        credentials = {
                'userid' : self._account['accountId'],
                'token' : self._streamerInfo['token'],
                'company' : self._account['company'],
                'segment' : self._account['segment'],
                'cddomain' : self._account['accountCdDomainId'],
                'usergroup' : self._streamerInfo['userGroup'],
                'accesslevel' : self._streamerInfo['accessLevel'],
                'authorized' : 'Y',
                'timestamp' : self.convert_epoch(self._streamerInfo['tokenTimestamp']),
                'addid' : self._streamerInfo['appId'],
                'acl' : self._streamerInfo['acl']
        }       

        return urlencode(credentials, quote_via=quote_plus)

    def get_account(self, userPrincipals):
        """
        Return account specified if account id is set otherwise return
        first account
        """
        accounts = userPrincipals['accounts']
        if self._accountId:
            for account in accounts:
                if self._accountId == account.get('accountId'):
                    return account
        else:
            return accounts[0]

    def streamer_url(self):
        """
        return the streamer url
        """
        if self._streamerInfo.get('streamerSocketUrl'):
            return f"wss://{self._streamerInfo['streamerSocketUrl']}/ws"
        else:
            raise KeyError("UserPrincipals not shared with steamer")

    async def login(self):
        """
        """
        async with websockets.connect(self.streamer_url()) as websocket:
            await websocket.send(json.dumps(self.login_request()))
            response = await websocket.recv()

            response = json.loads(response)

            if response['response'][0]['content']['code'] == 0:
                print('Success')
                return 1

    def login_request(self):
        """
        Returns request json that can be sent to the streaming endpoint
        """
        parameters = {
                'credential' : self.get_credentials(),
                'token' : self._streamerInfo['token'],
                'version' : '1.0'
        }

        return {'requests': [self._request('ADMIN','LOGIN', parameters)]}

    def _request(self, service, command, parameters):
        """
        forms a dict object as the base of all requests send to streamer endpoint
        """
        request = {
                'service' : service,
                'requestid' : self._requestid,
                'command' : command,
                'account' : self._account['accountId'],
                'source' : self._streamerInfo['appId'],
                'parameters' : parameters
        }

        self._requestid += 1

        return request

