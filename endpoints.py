class Endpoints(dict):
    """
    Container class to store API endpoints used by class TDClient
    """
    def __init__(self):
        super().__init__(self)

        auth_base = "https://auth.tdameritrade.com/auth"
        api_base = "https://api.tdameritrade.com/v1/"

        self['auth']           =  auth_base
        self['token']          =  api_base + "oauth2/token"
        self['accounts']       =  api_base + "accounts"
        self['account']        =  api_base + "accounts/{accountId}"
        self['place_order']    =  api_base + "accounts/{accountId}/orders"
        self['all_orders']     =  api_base + "accounts/{accountId}/orders"
        self['cancel_order']   =  api_base + "accounts/{accountId}/orders/{orderId}"
        self['get_order']      =  api_base + "accounts/{accountId}/orders/{orderId}"
        self['replace_order']  =  api_base + "accounts/{accountId}/orders/{orderId}"
        self['transaction']    =  api_base + "accounts/{accountId}/transaction/{transactionId}"
        self['transactions']   =  api_base + "accounts/{accountId}/transactions"
        self['instruments']    =  api_base + "instruments"
        self['market_hours']   =  api_base + "marketdata/{market}/hours"
        self['movers']         =  api_base + "marketdata/{index}/movers"
        self['options']        =  api_base + "marketdata/chains"
        self['price_history']  =  api_base + "marketdata/{symbol}/pricehistory"
        self['quote']          =  api_base + "marketdata/{symbol}/quotes"
        
