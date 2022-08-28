from enum import Enum

class Endpoints(Enum):
    """
    Container class to store API endpoints used by class TDClient
    """
    AUTH_BASE = "https://auth.tdameritrade.com/auth"
    API_BASE = "https://api.tdameritrade.com/v1/"

    AUTH           =  AUTH_BASE
    TOKEN          =  API_BASE + "oauth2/token"
    ACCOUNTS       =  API_BASE + "accounts"
    ACCOUNT        =  API_BASE + "accounts/{accountId}"
    PLACE_ORDER    =  API_BASE + "accounts/{accountId}/orders"
    ALL_ORDERS     =  API_BASE + "accounts/{accountId}/orders"
    CANCLE_ORDER   =  API_BASE + "accounts/{accountId}/orders/{orderId}"
    GET_ORDER      =  API_BASE + "accounts/{accountId}/orders/{orderId}"
    REPLACE_ORDER  =  API_BASE + "accounts/{accountId}/orders/{orderId}"
    TRANSACTION    =  API_BASE + "accounts/{accountId}/transaction/{transactionId}"
    TRANSACTIONS   =  API_BASE + "accounts/{accountId}/transactions"
    INSTRUMENTS    =  API_BASE + "instruments"
    MARKETS_HOURS  =  API_BASE + "marketdata/hours" 
    MARKET_HOURS   =  API_BASE + "marketdata/{market}/hours"
    MOVERS         =  API_BASE + "marketdata/{index}/movers"
    OPTIONS        =  API_BASE + "marketdata/chains"
    PRICE_HISTORY  =  API_BASE + "marketdata/{symbol}/pricehistory"
    QUOTE          =  API_BASE + "marketdata/{symbol}/quotes"


class Index(Enum):
    """
    Container class to store market index codes
    """

    COMPX = '$COMPX' #Nasdaq
    DJI   = '$DJI'   #Dow jones
    SPX   = 'SPX.X'  #S&P 500