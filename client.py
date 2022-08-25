from requests_oauthlib import OAuth2Session
from selenium import webdriver
from time import sleep

import pickle

import account
import endpoints
import orders

from exceptions import NotAuthorized

class TDAClient(OAuth2Session):
    """
    """
    def __init__(
        self, 
        client_id, 
        redirect_uri,
        **kwargs
    ):

        super().__init__(client_id, **kwargs)
        
        self.endpoints = endpoints.Endpoints()
        self.account = account.Account()

        self.redirect_uri = redirect_uri
        self.auto_refresh_url = self.endpoints['token']
        self.auto_refresh_kwargs = {'client_id': self._client.client_id}

    def login(self, webbrowser):
        """
        Direct the user to login on on td ameritrade and retrieve authorization code.  
        Use authorization code to fetch first set of access/refresh Oauth2 tokens

            args:
                webbrowser (type: webdriver) selenium module webdriver class for 
                            browsing session to allow user to login
            returns:
                boolean indicating login success/failure
        """
        #if not isinstance(webbrowser, webdriver):
            #raise TypeError("login session not provided with type 'webdriver'")

        authorization_url, _ = self.authorization_url(self.endpoints['auth'])

        webbrowser.get(authorization_url)

        # wait for redirect
        while self.endpoints['auth'][:28] in webbrowser.current_url:
            sleep(.1)

        # check if proper redirect
        if self.redirect_uri not in webbrowser.current_url:
            raise ValueError('Redirect url not valid')

        # fetch tokens
        self.fetch_token(
                self.endpoints['token'],
                authorization_response=webbrowser.current_url,
                include_client_id=True,
                access_type='offline'
            )

        # close webbrowser
        webbrowser.close()

        # Return success if class has access token
        if self.authorized:
            return 1
        else:
            return 0

    def load_session(self):
        """
        """
        with open("tokens", 'rb') as f:
            self.token = pickle.load(f)
            self.access_token = self.token['access_token']

    def save_session(self):
        """
        """
        with open("tokens", 'wb') as f:
            pickle.dump(self.token, f)

    def is_authorized(self):
        """
        Raise exception is session is not authorized
        """
        if not self.authorized:
            raise NotAuthorized("Session not authorized")

    def get_accounts(self, params={}):
        """
        returns all accounts associated with the given login
        """
        self.is_authorized()

        r = self.get(self.endpoints['accounts'], params=params)

        if r.status_code == 200:
            return (1, r)
        else:
            return (0, r)

    def get_account(self, accountId, params={}):
        """
        gets the account specified in the accountId input

            args:
                accountId - account to get from td ameritrade
                params - query parameters for returning more information
                    ex: fields=positions,orders 
                    returns information for positions and orders, if not 
                    supplied only information for account balances is
                    returned
        """
        self.is_authorized()

        # get account information
        r = self.get(self.endpoints['account'].format(accountId=accountId), params=params)

        if r.status_code == 200:
            return (1, r)
        else:
            return (0, None)

    def refresh_account(self):
        """
        Refresh the account status
        """
        self.is_authorized()

        if not self.account.account_id:
            raise ValueError("account_id not defined")

        # get account information    
        status, r = self.get_account(accountId=self.account.account_id, params={'fields':'positions,orders'})

        # pass to account instance and then return 
        if status:
            self.account.parse_response(r.json())
            return (1, r)
        else:
            return (0, r)

    def place_order(self, order):
        """
        Place an order through TD ameritrade

            args: 
                order (type: Order) Takes instances of any subclasse of order (Equity, Option, etc)

            returns:
                Tuple in the form of (Status, Response)
                    Where:
                        Status - Boolean indicating successful post transaction
                        OrderId - Id of transaction if successful
                        Response - full response from request
        """
        self.is_authorized()

        if not issubclass(type(order), orders.Order):
            raise TypeError("Given order not subclass of type Order")

        # Post order to TDA
        r = self.post(self.endpoints['place_order'].format(accountId=self.account.account_id), json=order.form())

        if r.status_code == 201:
            orderId = r.headers.get('Location').split('/')[-1]
            return (1, orderId, r)
        else:
            return (0, None, r)

    def cancel_order(self, orderId):
        """
        Cancels previously placed order

            args:
                orderId (type: str) orderId for order to cancel

            returns:
                Boolean of whether transaction was successful
 
            TO-DO: ADD LOGGERS AND ORDER HISTORY CLASS
            ALSO What happens when order already went through? Test out
        """
        self.is_authorized()

        # Delete order from TDA
        r = self.delete(self.endpoints['cancel_order'].format(accountId=self.account.account_id,orderId=orderId))

        if r.status_code == 200:
            return 1
        else:
            return 0

    def all_orders(self, **kwargs):
        """
        Retrieves all order from account filter by the kwargs

            kwargs:
                maxResults - The max number of orders to retireve
                fromEnteredTime - Start of orders to retrieve (yyyy-MM-dd)
                toEnteredTime - End of orders to retrieve (yyyy-MM-dd)
                status - Specific that only orders of this status should be returned
        """ 
        self.is_authorized()

        if kwargs:
            params = kwargs
        else:
            params = {}

        r = self.get(self.endpoints['all_orders'].format(accountId=self.account.account_id),params=params)
        
        if r.status_code == 200:
            return (1, r.json())
        else:
            return (0, r.json())

    def get_order(self, orderId):
        """
        Get order information for a specific order

            args:
                orderId (type: str) orderId for order to get information for
        """
        self.is_authorized()

        r = self.get(self.endpoints['get_order'].format(accountId=self.account.account_id,orderId=orderId))

        if r.status_code == 200:
            return (1, r.json())
        else:
            return (0, r.jsoin())
    
    def replace_order(self, order):
        """
        """
        pass

    def instruments(self, symbol, projection='symbol-search'):
        """
        """
        pass

    def market_hours(self, market):
        """
        """
        pass

    def movers(self, market):
        """
        """
        pass

    def options(self):
        """
        """
        pass

    def price_history(self):
        """
        """
        pass

    def quote(self):
        """
        """
        pass

    def transaction(self):
        """
        """
        pass

    def transactions(self):
        """
        """
        pass


