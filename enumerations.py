

class Endpoints:
    """
    Container class to store API endpoints used by class TDClient
    """
    AUTH_BASE           = "https://auth.tdameritrade.com/auth"
    API_BASE            = "https://api.tdameritrade.com/v1/"

    AUTH                =  AUTH_BASE
    TOKEN               =  API_BASE + "oauth2/token"
    ACCOUNTS            =  API_BASE + "accounts"
    ACCOUNT             =  API_BASE + "accounts/{accountId}"
    PLACE_ORDER         =  API_BASE + "accounts/{accountId}/orders"
    ALL_ORDERS          =  API_BASE + "accounts/{accountId}/orders"
    CANCLE_ORDER        =  API_BASE + "accounts/{accountId}/orders/{orderId}"
    GET_ORDER           =  API_BASE + "accounts/{accountId}/orders/{orderId}"
    REPLACE_ORDER       =  API_BASE + "accounts/{accountId}/orders/{orderId}"
    TRANSACTION         =  API_BASE + "accounts/{accountId}/transaction/{transactionId}"
    TRANSACTIONS        =  API_BASE + "accounts/{accountId}/transactions"
    INSTRUMENTS         =  API_BASE + "instruments"
    MARKETS_HOURS       =  API_BASE + "marketdata/hours" 
    MARKET_HOURS        =  API_BASE + "marketdata/{market}/hours"
    MOVERS              =  API_BASE + "marketdata/{index}/movers"
    OPTIONS             =  API_BASE + "marketdata/chains"
    PRICE_HISTORY       =  API_BASE + "marketdata/{symbol}/pricehistory"
    QUOTE               =  API_BASE + "marketdata/{symbol}/quotes"


class Index:
    COMPX               = '$COMPX' 
    DJI                 = '$DJI'  
    SPX                 = 'SPX.X'  


class OrderType:
    MARKET              = 'MARKET'
    LIMIT               = 'LIMIT'
    STOP                = 'STOP'
    STOP_LIMIT          = 'STOP_LIMIT'
    TRAILING_STOP       = 'TRAILING_STOP'
    MARKET_ON_CLOSE     = 'MARKET_ON_CLOSE'
    EXERCISE            = 'EXERCISE'
    TRAILING_STOP_LIMIT = 'TRAILING_STOP_LIMIT'
    NET_DEBIT           = 'NET_DEBIT'
    NET_CREDIT          = 'NET_CREDIT'
    NET_ZERO            = 'NET_ZERO'


class Instructions:
    BUY                 = 'BUY'
    SELL                = 'SELL'  
    BUY_TO_OPEN         = 'BUY_TO_OPEN'
    BUY_TO_COVER        = 'BUY_TO_COVER'
    BUY_TO_CLOSE        = 'BUY_TO_CLOSE'
    SELL_TO_OPEN        = 'SELL_TO_OPEN'
    SELL_SHORT          = 'SELL_SHORT'
    SELL_TO_CLOSE       = 'SELL_TO_CLOSE'


class OrderStrategyType:
    SINGLE              = 'SINGLE'
    TRIGGER             = 'TRIGGER'
    OCO                 = 'OCO'


class Session:
    NORMAL              = 'NORMAL'
    AM                  = 'AM'
    PM                  = 'PM'
    SEAMLESS            = 'SEAMLESS'


class Duration:
    DAY                 = 'DAY'
    GOOD_TILL_CANCLED   = 'GOOD_TILL_CANCLED'
    FILL_OR_KILL        = 'FILL_OR_KILL'


class ComplexOrderType:
    NONE                = 'NONE'
    COVERED             = 'COVERED'
    VERTICAL            = 'VERTICAL'
    BACK_RATIO          = 'BACK_RATIO'
    CALENDAR            = 'CALENDAR'
    DIAGONAL            = 'DIAGONAL'
    STRADDLE            = 'STRADDLE'
    STRANGLE            = 'STRANGLE'
    COLLAR_SYNTHETIC    = 'COLLAR_SYNTHETIC'
    BUTTERYFLY          = 'BUTTERFLY'
    CONDOR              = 'CONDOR'
    IRON_CONDOR         = 'IRON_CONDOR'
    CUSTOM              = 'CUSTOM'


class Const:
    """
    Genertic constant data container used throughout the module
    """
    Instructions        = Instructions()
    OrderType           = OrderType()
    OrderStrategyType   = OrderStrategyType()
    Session             = Session()
    Duration            = Duration()
    ComplexOrderType    = ComplexOrderType()