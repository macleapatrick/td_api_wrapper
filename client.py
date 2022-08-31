from requests_oauthlib import OAuth2Session
from datetime import datetime, timedelta
from time import sleep

import pickle

from account import Account
from orders import Order, OrderHistory

from enumerations import Endpoints
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
        
        self.account = Account()
        self.orders = OrderHistory()

        self.redirect_uri = redirect_uri

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
        authorization_url, _ = self.authorization_url(Endpoints.AUTH)

        webbrowser.get(authorization_url)

        # wait for redirect
        while Endpoints.AUTH[:28] in webbrowser.current_url:
            sleep(.1)

        # check if proper redirect
        if self.redirect_uri not in webbrowser.current_url:
            raise ValueError('Redirect url not valid')

        # fetch tokens
        self.fetch_token(
                Endpoints.TOKEN,
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

    def transactionCheck(self):
        """
        Check if the program can procede with the transacton
            Check if we have an access code 
            Check if the default account is set
        """
        self.is_authorized()
        self.is_account_set()

    def refresh_token(self, **kwargs):
        """
        Refresh token if expired
        """
        if datetime.now().timestamp() > self.token['expires_at']:

            super().refresh_token(
                Endpoints.TOKEN, 
                self.token['refresh_token'],
                client_id=self._client.client_id,
                **kwargs
            )

    def is_authorized(self):
        """
        Raise exception is session does not have access code
        """
        if not self.authorized:
            raise NotAuthorized("Session not authorized")
        else:
            return 1

    def is_account_set(self):
        """
        Raise exception if there is not account id defined
        """
        if not self.account.account_id:
            raise ValueError("Client account id not set")
        else:
            return 1 

    def get_accounts(
        self, 
        params={}
    ):
        """
        returns all accounts associated with the given login
        """
        self.transactionCheck()
        self.refresh_token()

        r = self.get(
                Endpoints.ACCOUNTS, 
                params=params
            )

        if r.status_code == 200:
            return (1, r)
        else:
            return (0, r)

    def get_account(
        self, 
        accountId, 
        params={}
    ):
        """
        gets the account specified in the accountId input

            args:
                accountId (type: int)
                    account to get from td ameritrade
                params (type: dict)
                    query parameters for returning more information
                    ex: fields=positions,orders 
                    returns information for positions and orders, if not 
                    supplied only information for account balances is
                    returned
        """
        self.transactionCheck()
        self.refresh_token()

        r = self.get(
                Endpoints.ACCOUNT.format(accountId=accountId), 
                params=params
            )

        if r.status_code == 200:
            return (1, r)
        else:
            return (0, None)

    def refresh_account(
        self, 
        options=['positions'], 
        params={}
    ):
        """
        Refresh the account status
        """
        self.transactionCheck()
        self.refresh_token()

        if not self.account.account_id:
            raise ValueError("account_id not defined")

        params['fields'] = ','.join(options)

        status, r = self.get_account(
                accountId=self.account.account_id, 
                params=params
            )

        if status:
            self.account.update(r.json())
            return 1
        else:
            return 0

    def refresh_orders(self):
        """
        Refreshes status of the orders and stores
        results in the self.orders class
        """
        self.transactionCheck()
        self.refresh_token()

        status, r = self.all_orders()

        if status:
            d = {}
            for order in r.json():
                d[int(order['orderId'])] = order

            self.orders.update(d)
            return 1
        else:
            return 0

    def place_order(self, order):
        """
        Place an order through TD ameritrade

            args: 
                order (type: Order) 
                    Takes instances of any subclasse of order (Equity, Option, etc)

            returns:
                Tuple in the form of (Status, Response, orderId)
                    Status (type: bool) 
                        indicating successful post transaction
                    Response (type: response) 
                        full response from request
                    OrderId (type: int)
                        orderId of posted transaction
        """
        self.transactionCheck()
        self.refresh_token()

        if not issubclass(type(order), Order):
            raise TypeError("Given order not subclass of type Order")

        r = self.post(
                Endpoints.PLACE_ORDER.format(
                    accountId=self.account.account_id), 
                json=order.form()
            )

        if r.status_code == 201:
            orderId = int(r.headers.get('Location').split('/')[-1])
            return (1, r, orderId)
        else:
            return (0, r, None)

    def cancel_order(
        self, 
        orderId, 
        checkCancelable=True
    ):
        """
        Cancels previously placed order

            args:
                orderId (type: int) 
                    orderId for order to cancel
                checkCancelable (type: bool)
                    check order log and see if order is cancelable

            returns:
                Tuple in the form of (status, response)
                    status (type: bool) 
                        indicating successful transaction
                    response (type: response) 
                        full response from requests or None if order is not cancelable
        """
        self.transactionCheck()
        self.refresh_token()

        if checkCancelable and not self.orders.get(orderId, {}).get('cancelable',''):
            return (0, None)

        r = self.delete(
                Endpoints.CANCLE_ORDER.format(
                    accountId=self.account.account_id,
                    orderId=orderId)
            )

        if r.status_code == 200:
            return (1, r)
        else:
            return (0, r)

    def all_orders(
        self,
        **kwargs
    ):
        """
        Retrieves all order from account filter by the kwargs

            kwargs:
                maxResults - The max number of orders to retireve
                fromEnteredTime - Start of orders to retrieve (yyyy-MM-dd)
                toEnteredTime - End of orders to retrieve (yyyy-MM-dd)
                status - Specific that only orders of this status should be returned
        """ 
        self.transactionCheck()
        self.refresh_token()

        r = self.get(
            Endpoints.ALL_ORDERS.format(
                accountId=self.account.account_id),
            params=kwargs
        )
        
        if r.status_code == 200:
            return (1, r)
        else:
            return (0, r)

    def get_order(
        self, 
        orderId
    ):
        """
        Get order information for a specific order

            args:
                orderId (type: str) 
                    orderId for order to get information for

            return:
                Tuple in the form of (Status, Response)
                    Status (type: bool) 
                        indicating successful get transaction
                    Response (type: response) 
                        full response from request
        """
        self.transactionCheck()
        self.refresh_token()

        r = self.get(
            Endpoints.GET_ORDER.format(
                accountId=self.account.account_id,
                orderId=orderId)
        )

        if r.status_code == 200:
            return (1, r)
        else:
            return (0, r)
    
    def replace_order(
        self, 
        orderId, 
        order, 
        checkEditable=True
    ):
        """
        Replace an existing order through td ameritrade

            args: 
                orderId (type: int)
                    The order Id of the order to replace
                order (type: Order) 
                    Takes instances of any subclasse of order (Equity, Option, etc)
                checkEditable (type: Bool)
                    Check orders to see if this order can be edited. Note this
                    will only check stored orders and won't refresh orders
            returns:
                Tuple in the form of (Status, Response)
                    Status (type: Bool)
                        indicating successful put transaction
                    Response (type: response)
                        full response from request
        """
        self.transactionCheck()
        self.refresh_token()

        if not issubclass(type(order), Order):
            raise TypeError("Given order not subclass of type Order")

        if checkEditable and not self.orders.get(orderId, {}).get('editable',''):
            return (0, None)

        r = self.put(
                Endpoints.REPLACE_ORDER.format(
                    accountId=self.account.account_id,
                    orderId=orderId), 
                json=order.form()
            )

        if r.status_code == 201:
            orderId = r.headers.get('Location').split('/')[-1]
            return (1, orderId, r)
        else:
            return (0, None, r)

    def instruments(
        self, 
        symbol, 
        projection='symbol-search'
    ):
        """
        Returns information associated with symbol

        args:
            symbol (type: str)
                symbol to search for
            projection (type: str) - Optional
                type of search
                valid entries:
                    'symbol-search'
                    'symbol-regex'
                    'desc-search'
                    'desc-regex',
                    'fundamental'
        returns:
              Tuple in the form of (Status, Response)
                    Status (type: bool) 
                        indicating successful get transaction
                    Response (type: response)
                        full response from request

        """
        self.transactionCheck()
        self.refresh_token()
        
        local = locals()
        params = {kw : local.get(kw) for kw in ['symbol','projection']}

        r = self.get(
            Endpoints.INSTRUMENTS,
            params=params
        )

        if r.status_code == 200:
            return (1, r)
        else:
            return (0, r)

    def markets_hours(
        self, 
        markets=['EQUITY','OPTION'],
        date=datetime.now().strftime("%Y-%m-%d'T'%H:%M:%SZ")
    ):
        """
        Returns market hours for given markets

        args:
            markets (type: list)
                List of markets to include in response
                can be (EQUITY, OPTION, FUTURE, BOND, or FOREX)
            date (type: str)
                date to retrieve market hours for in the form of 
                yyyy-MM-dd or yyyy-MM-dd'T'HH:mm:ssz

        returns:
            Tuple in the form of (Status, Response)
                Status (type: bool) 
                    indicating successful get transaction
                Response (type: response)
                    full response from request
        """
        self.transactionCheck()
        self.refresh_token()

        params = {}
        params['markets'] = ','.join(markets)
        params['date'] = date

        r = self.get(
            Endpoints.MARKETS_HOURS, 
            params=params
        )

        if r.status_code == 200:
            return (1, r)
        else:
            return (0, r)

    def movers(
        self, 
        index,
        direction='up',
        change='percent'
    ):
        """
        """
        self.transactionCheck()
        self.refresh_token()

        local = locals()
        params = {kw : local.get(kw) for kw in ['direction','change']}

        r = self.get(
            Endpoints.MOVERS.format(index=index),
            params=params
        )

        if r.status_code == 200:
            return (1, r)
        else:
            return (0, r)

    def options(
        self,
        symbol,
        contractType='ALL',
        strikeCount='10',
        includeQuotes='TRUE',
        stategy='SINGLE',
        range='ALL',
        days=10,
        fromDate='',
        toDate='',
        expMonth='ALL',
        optionType='ALL',
    ):
        """
        """
        self.transactionCheck()
        self.refresh_token()

        if not fromDate: fromDate= str(datetime.now().date()),
        if not toDate: toDate= str((datetime.now()+timedelta(days=days)).date()),

        kws = ['symbol','contractType','strikeCount','includeQuotes',
               'stategy','range','days','fromDate','toDate','expMonth',
               'optionType']

        local = locals()
        params = {kw : local.get(kw) for kw in kws if local.get(kw)}

        r = self.get(
            Endpoints.OPTIONS,
            params=params
        )

        if r.status_code == 200:
            return (1, r)
        else:
            return (0, r)

    def price_history(
        self, 
        symbol,
        periodType='day',
        frequencyType='minute',
        period=None,
        frequency=1,
        endDate=None,
        startDate=None,
        needExtendedHoursData=False
    ):
        """
        """
        self.transactionCheck()
        self.refresh_token()

        kws = ['symbol','frequencyType','period','frequency',
               'endDate','startDate','needExtendedHoursData']

        local = locals()
        params = {kw : local.get(kw) for kw in kws if local.get(kw) is not None}

        r = self.get(
            Endpoints.PRICE_HISTORY.format(symbol=symbol),
            params = params
        )

        if r.status_code == 200:
            return (1, r)
        else:
            return (0, r)

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


