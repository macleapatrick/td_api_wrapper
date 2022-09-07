import asyncio
import websockets
from urllib.parse import urlencode, quote_plus

from datetime import datetime
from enumerations import StreamerServices as Stream

from threading import Thread

import json


class StreamerBase:
    """
    """
    def __init__(self):

        self._websocket = None
        self._accountId = ''
        self._account = {}
        self._streamerInfo = {}
        self._requestid = 0

        self.streamer_url = ''
        self.subscriptions = []
        self.buffer = {}

        self.loggedin = False
        self.logout = False

    @property
    def accountId(self):
        return self._accountId

    @accountId.setter
    def accountId(self, value):
        if self._accountId:
            raise ValueError("AccountId cannot be changed once set")
        else:
            self._accountId = value

    async def main(self):
        """
        Main loop for handling websocket connection
        """
        async with websockets.connect(self.streamer_url) as self._websocket:
            if not self.loggedin:
                await self._websocket.send(json.dumps(self.login_request()))
                print(await self._websocket.recv())

                for subscription in self.subscriptions:
                    await self._websocket.send(json.dumps(subscription))
                    print(await self._websocket.recv())

                self.loggedin = True
            
            while not self.logout:
                message = await self._websocket.recv()
                self._store(message)

                if self.logout:
                    await self._websocket.send(json.dumps(self.logout_request()))
                    print(await self._websocket.recv())
                    self.logout, self.loggedin = False, False

    def _start(self):
        """
        Start the event loop for websocket connection
        """
        asyncio.run(self.main())

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

        return {'requests': [request]}

    def _add_subscription(
            self, 
            service,
            command,
            parameters
        ):
        """
        """
        self.subscriptions.append(self._request(service, command, parameters))

    def _store(self, message):
        """
        Stores all recieved messages from streamer into a buffer broken up by
        service type
        """
        message = json.loads(message)
        for header in message:
            for data in message[header]:
                service = data.get('service')
                if service in self.buffer:
                    self.buffer[service].append(data)
                elif service:
                    self.buffer[service] = []
                    self.buffer[service].append(data)

    def parse_principals(
            self, 
            userPrincipals
        ):
        """
        Store userprinipals from client api
        """
        self._account = self.get_account(userPrincipals)
        self._streamerInfo = userPrincipals['streamerInfo']

        if not self.streamer_url:
            self.streamer_url = f"wss://{self._streamerInfo['streamerSocketUrl']}/ws"

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
            self._account = accounts[0]['accountId']
            return accounts[0]

    def login_request(self):
        """
        Returns request json that can be sent to the streaming endpoint
        """
        parameters = {
                'credential' : self.get_credentials(),
                'token' : self._streamerInfo['token'],
                'version' : '1.0'
        }

        request = self._request(
                Stream.ADMIN.NAME,
                Stream.ADMIN.LOGIN,
                parameters
        )

        return request

    def logout_request(self):
        """
        Returns request json that can be sent to the streaming endpoint
        """
        request = self._request(
                Stream.ADMIN.NAME,
                Stream.ADMIN.LOGOUT,
                parameters={}
        )

        return request

    @staticmethod
    def convert_epoch(string):
        format = '%Y-%m-%dT%H:%M:%S%z'
        return int(datetime.strptime(string,format).timestamp() * 1000)


class Streamer(StreamerBase):
    """
    """
    def __init__(self):
        super().__init__()

    def start(self):
        """
        Start the async websocket event loop on a new thread
        """
        self.thread = Thread(target=self._start)
        self.thread.start()

    def stop(self):
        """
        Stop the async event loop
        """
        self.logout = True
        self.thread.join() 

    def process(self, service):
        """
        return all messages for given service in buffer and then clear buffer
        """
        if service not in self.buffer:
            return None

        messages = self.buffer[service]
        self.buffer[service] = []
        return messages

    def equity_quote_stream(
            self,
            keys,
            fields=[]
        ):
        """
        """
        if not fields:
            fields=[e.value for e in Stream.QUOTE.OHLC_STREAM]

        self._add_subscription(
            service=Stream.QUOTE.NAME,
            command=Stream.QUOTE.SUBS,
            parameters={'keys' : ','.join(keys), 'fields' : ','.join(fields)}
        )

    def futures_quote_stream(
            self,
            keys,
            fields=[]
        ):
        """
        """
        if not fields:
            fields = [e.value for e in Stream.LEVELONE_FUTURES.OHLC_STREAM]

        self._add_subscription(
            service=Stream.LEVELONE_FUTURES.NAME,
            command=Stream.LEVELONE_FUTURES.SUBS,
            parameters={'keys' : ','.join(keys), 'fields' : ','.join(fields)}
        )
    

