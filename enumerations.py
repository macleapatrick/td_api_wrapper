from enum import Enum

class Endpoints:
    """
    Container class to store API endpoints used by class TDClient
    """
    AUTH_BASE               = "https://auth.tdameritrade.com/auth"
    API_BASE                = "https://api.tdameritrade.com/v1/"

    AUTH                    =  AUTH_BASE
    TOKEN                   =  API_BASE + "oauth2/token"
    ACCOUNTS                =  API_BASE + "accounts"
    ACCOUNT                 =  API_BASE + "accounts/{accountId}"
    PLACE_ORDER             =  API_BASE + "accounts/{accountId}/orders"
    ALL_ORDERS              =  API_BASE + "accounts/{accountId}/orders"
    CANCLE_ORDER            =  API_BASE + "accounts/{accountId}/orders/{orderId}"
    GET_ORDER               =  API_BASE + "accounts/{accountId}/orders/{orderId}"
    REPLACE_ORDER           =  API_BASE + "accounts/{accountId}/orders/{orderId}"
    TRANSACTION             =  API_BASE + "accounts/{accountId}/transaction/{transactionId}"
    TRANSACTIONS            =  API_BASE + "accounts/{accountId}/transactions"
    INSTRUMENTS             =  API_BASE + "instruments"
    MARKETS_HOURS           =  API_BASE + "marketdata/hours" 
    MARKET_HOURS            =  API_BASE + "marketdata/{market}/hours"
    MOVERS                  =  API_BASE + "marketdata/{index}/movers"
    OPTIONS                 =  API_BASE + "marketdata/chains"
    PRICE_HISTORY           =  API_BASE + "marketdata/{symbol}/pricehistory"
    QUOTE                   =  API_BASE + "marketdata/{symbol}/quotes"
    QUOTES                  =  API_BASE + "marketdata/quotes"
    USER_PRINCIPALS         =  API_BASE + "userprincipals"


class Index:
    COMPX                   = '$COMPX' 
    DJI                     = '$DJI'  
    SPX                     = 'SPX.X'  


class OrderType:
    MARKET                  = 'MARKET'
    LIMIT                   = 'LIMIT'
    STOP                    = 'STOP'
    STOP_LIMIT              = 'STOP_LIMIT'
    TRAILING_STOP           = 'TRAILING_STOP'
    MARKET_ON_CLOSE         = 'MARKET_ON_CLOSE'
    EXERCISE                = 'EXERCISE'
    TRAILING_STOP_LIMIT     = 'TRAILING_STOP_LIMIT'
    NET_DEBIT               = 'NET_DEBIT'
    NET_CREDIT              = 'NET_CREDIT'
    NET_ZERO                = 'NET_ZERO'


class Instructions:
    BUY                     = 'BUY'
    SELL                    = 'SELL'  
    BUY_TO_OPEN             = 'BUY_TO_OPEN'
    BUY_TO_COVER            = 'BUY_TO_COVER'
    BUY_TO_CLOSE            = 'BUY_TO_CLOSE'
    SELL_TO_OPEN            = 'SELL_TO_OPEN'
    SELL_SHORT              = 'SELL_SHORT'
    SELL_TO_CLOSE           = 'SELL_TO_CLOSE'


class OrderStrategyType:
    SINGLE                  = 'SINGLE'
    TRIGGER                 = 'TRIGGER'
    OCO                     = 'OCO'


class Session:
    NORMAL                  = 'NORMAL'
    AM                      = 'AM'
    PM                      = 'PM'
    SEAMLESS                = 'SEAMLESS'


class Duration:
    DAY                     = 'DAY'
    GOOD_TILL_CANCLED       = 'GOOD_TILL_CANCLED'
    FILL_OR_KILL            = 'FILL_OR_KILL'


class ComplexOrderType:
    NONE                    = 'NONE'
    COVERED                 = 'COVERED'
    VERTICAL                = 'VERTICAL'
    BACK_RATIO              = 'BACK_RATIO'
    CALENDAR                = 'CALENDAR'
    DIAGONAL                = 'DIAGONAL'
    STRADDLE                = 'STRADDLE'
    STRANGLE                = 'STRANGLE'
    COLLAR_SYNTHETIC        = 'COLLAR_SYNTHETIC'
    BUTTERYFLY              = 'BUTTERFLY'
    CONDOR                  = 'CONDOR'
    IRON_CONDOR             = 'IRON_CONDOR'
    CUSTOM                  = 'CUSTOM'


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


class Admin:
    NAME                    = 'ADMIN'
    LOGIN                   = 'LOGIN'
    LOGOUT                  = 'LOGOUT'
    QOS                     = 'QOS'


class QuoteFields(Enum):
    SYMBOL                  = '0'
    BID_PRICE               = '1'
    ASK_PRICE               = '2'
    LAST_PRICE              = '3'
    BID_SIZE                = '4'
    ASK_SIZE                = '5'
    ASK_ID                  = '6'
    BID_ID                  = '7'
    TOTAL_VOLUME            = '8'
    LAST_SIZE               = '9'
    TRADE_TIME              = '10'
    QUOTE_TIME              = '11'
    HIGH_PRICE              = '12'
    LOW_PRICE               = '13'
    BID_TICK                = '14'
    CLOSE_PRICE             = '15'
    EXCHANGE_ID             = '16'
    MARGINABLE              = '17'
    SHORTABLE               = '18'
    ISLAND_BID              = '19'
    ISLAND_ASK              = '20'
    ISLANE_VOLUME           = '21'
    QUOTE_DAY               = '22'
    TRADE_DAY               = '23'
    VOLATILITY              = '24'
    DESCRIPTION             = '25'
    LAST_ID                 = '26'
    DIGITS                  = '27'
    OPEN_PRICE              = '28'
    NET_CHANGE              = '29'
    WEEK_52_HIGH            = '30'
    WEEK_52_LOW             = '31'
    PE_RATIO                = '32'
    DIVIDEND_AMOUNT         = '33'
    DIVIDENT_YIELD          = '34'
    ISLAND_BID_SIZE         = '35'
    ISLANE_ASK_SIZE         = '36'
    NAV                     = '37'
    FUND_PRICE              = '38'
    EXCHANGE_NAME           = '39'
    DIVIDEND_DATE           = '40'
    REG_MARKET_QUOTE        = '41'
    REG_MARKET_TRADE        = '42'
    REG_MARKET_LAST_PRICE   = '43'
    REG_MARKET_LAST_SIZE    = '44'
    REG_MARKET_TRADE_TIME   = '45'
    REG_MARKET_TRADE_DAY    = '46'
    REG_MARKET_NET_CHANGE   = '47'
    SECURITY_STATUS         = '48'
    MARK                    = '49'
    QUOTE_TIME_IN_LONG      = '50'
    TRADE_TIME_IN_LONG      = '51'
    REG_MRK_TRADE_TIME_LONG = '52'


class QuoteOHLC(Enum):
    SYMBOL                  = '0'
    BID_PRICE               = '1'
    ASK_PRICE               = '2'
    LAST_PRICE              = '3'
    TOTAL_VOLUME            = '8'


class Quote:
    NAME                    = 'QUOTE'
    SUBS                    = 'SUBS'
    UNSUBS                  = 'UNSUBS'
    FIELDS                  = QuoteFields
    OHLC_STREAM             = QuoteOHLC


class FutureFields(Enum):
    SYMBOL                  = '0'
    BID_PRICE               = '1'
    ASK_PRICE               = '2'
    LAST_PRICE              = '3'
    BID_SIZE                = '4'
    ASK_SIZE                = '5'
    ASK_ID                  = '6'
    BID_ID                  = '7'
    TOTAL_VOLUME            = '8'
    LAST_SIZE               = '9'
    TRADE_TIME              = '10'
    QUOTE_TIME              = '11'
    HIGH_PRICE              = '12'
    LOW_PRICE               = '13'
    CLOSE_PRICE             = '14'
    EXCHANGE_ID             = '15'
    DESCRIPTION             = '16'
    LAST_ID                 = '17'
    OPEN_PRICE              = '18'
    NET_CHANGE              = '19'
    FUTURE_PERCENT_CHANGE   = '20'
    EXCHANGE_NAME           = '21'
    SECURITY_STATUS         = '22'
    OPEN_INTEREST           = '23'
    MARK                    = '24'
    TICK                    = '25'
    TICK_AMOUNT             = '26'
    PRODUCT                 = '27'
    FUTURE_PRICE_FORMAT     = '28'
    FUTURE_TRADING_HOURS    = '29'
    FUTURE_IS_TRADABLE      = '30'
    FUTURE_MUTIPLIER        = '31'
    FUTURE_IS_ACTIVE        = '32'
    FUTURE_SETTLETMENT_PRICE= '33'
    FUTURE_ACTIVE_SYMBOL    = '34'
    FUTURE_EXPIRATION_DATE  = '35'


class FutureOHLC(Enum):
    SYMBOL                  = '0'
    BID_PRICE               = '1'
    ASK_PRICE               = '2'
    LAST_PRICE              = '3'
    TOTAL_VOLUME            = '8'


class LevelOneFutures:
    NAME                    = 'LEVELONE_FUTURES'
    SUBS                    = 'SUBS'
    UNSUBS                  = 'UNSUBS'
    FIELDS                  = FutureFields
    OHLC_STREAM             = FutureOHLC


class StreamerServices:
    ACCT_ACTIVITY           = None
    ADMIN                   = Admin
    ACTIVES_NASDAQ          = None
    ACTIVES_NYSE            = None
    ACTIVES_OTCBB           = None
    ACTIVES_OPTIONS         = None
    FOREX_BOOK              = None
    FUTURES_BOOK            = None
    LISTED_BOOK             = None
    NASDAQ_BOOK             = None
    OPTIONS_BOOK            = None
    FUTURES_OPTIONS_BOOK    = None
    CHART_EQUITY            = None
    CHART_FUTURES           = None
    CHART_HISTORY_FUTURES   = None
    QUOTE                   = Quote
    LEVELONE_FUTURES        = LevelOneFutures
    LEVELONE_FOREX          = None
    LEVELONE_FUTURES_OPTIONS= None
    OPTION                  = None
    LEVELTWO_FUTURES        = None
    NEWS_HEADLINE           = None
    NEWS_STORY              = None
    NEWS_HEADLINE_LIST      = None
    STREAMER_SERVER         = None
    TIMESALE_EQUITY         = None
    TIMESALE_FUTURES        = None
    TIMESALE_FOREX          = None
    TIMESALE_OPTIONS        = None