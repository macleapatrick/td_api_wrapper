from exceptions import InvalidOrder
from enumerations import Const

class OrderHistory(dict):
    """
    subclass of dict to store the previously made orders on the account.
    class is nested under tda client class

    each item in dict is an instance of the RecievedOrder class that 
    stores the information for a given order
    """
    def __init__(self):
        super().__init__(self)

    def __repr__(self):
        return f"<Class: '{self.__class__.__name__}', Number Of Orders: '{len(self)}'>"

    def update(self, orders):
        """
        """
        for d in orders:
            orderId = d['orderId']
            if orderId in self:
                self[orderId].update(d)
            else:
                self[orderId] = RecievedOrder(d)


class RecievedOrder:
    """
    Data Container for order infomation recieved from TDA
    """
    def __init__(self, d):
        self.update(d)

    def __repr__(self):
        return f"<Class: '{self.__class__.__name__}', Status: '{self.status}'>"

    def update(self, d):
        self.__dict__.update(d)

    def get(self, attr, fail):
        if attr in self.__dict__:
            return self.__dict__[attr]
        else:
            return fail


class Order:
    """
    Order to store information about an order to be made through the TDA client
    Pass order subclass (See Equity and Option) to client place_order method
    """
    def __init__(
        self,
        orderType='MARKET',
        session='NORMAL',
        duration='DAY',
        orderStrategyType='SINGLE',
        **kwargs
        ):

        self.orderType = orderType
        self.session = session
        self.duration = duration
        self.orderStrategyType = orderStrategyType
        self.orderLegCollection = []
        self.childOrderStrategies = []
        self.price = ''
        self.__dict__.update(kwargs)

    def form(self):
        """
        Return a dict of all class attributes if they have a value
        """
        if self._validate():
            return {kw : self.__dict__[kw] for kw in self.__dict__ if self.__dict__[kw]}
        else:
            raise InvalidOrder

    def addChildOrder(self, order):
        """
        Adds a child order, used for Trigger and OCO orders
        """
        self.childOrderStrategies.append(order)

    def set_limit(self, price):
        """
        Changes the order to a limit order
        """
        self.orderType = Const.OrderType.LIMIT
        self.price = price

    def set_stop(self, price):
        """
        Changes the order to a stop order
        """
        self.orderType = Const.OrderType.STOP
        self.stopPrice = price
        
    def set_stop_limit(self, limitPrice, stopPrice):
        """
        Changes the order to a stop limit order
        """
        self.orderType = Const.OrderType.STOP_LIMIT
        self.stopPrice = stopPrice
        self.price = limitPrice

    def set_duration(self, gtc=False, fof=False):
        """
        Sets order to 'Good till canceled' or 'Fill or Kill'
        Only needed if not using the default 'DAY'
        """
        if gtc:
            self.duration = Const.Duration.GOOD_TILL_CANCLED
        elif fof:
            self.duration = Const.Duration.FILL_OR_KILL

    def set_strategy_type(self, trigger=False, oco=False):
        """
        Set stategy type
        """
        if trigger:
            self.orderStrategyType = Const.OrderStrategyType.TRIGGER
        elif oco:
            self.orderStrategyType = Const.OrderStrategyType.OCO

    def set_session(self, am=False, pm= False, seamless=False):
        """
        Sets the session of the order. Only needed if not
        use the default 'NORMAL'
        """
        if am:
            self.session = Const.Session.AM
        elif pm:
            self.session = Const.Session.PM
        elif seamless:
            self.session = Const.Session.SEAMLESS

    def _validate(self):
        pass


class Equity(Order):
    """
    Subclass of Order class used to create orders that are fed to the 
    tda client class.  Used for equity orders
    """
    def __init__(self, **kwargs):
        """
        """
        super().__init__()

        self.__dict__.update(kwargs)

    def add_leg(self, symbol, quantity, closing=False):
        """
        Add leg to an Equity Order

            args: 
                symbol (type: string)
                    ticker of equity to trade
                quantity (type: int)
                    quantity for transaction (negative to sell short position)
                closing (type: bool)
                    is the order closing an existing trade
        """
        if closing:
            if quantity > 0:
                instruction = Const.Instructions.BUY_TO_COVER
            else:
                instruction = Const.Instructions.SELL
        else:
            if quantity > 0:
                instruction = Const.Instructions.BUY
            else:
                instruction = Const.Instructions.SELL_SHORT

        self.orderLegCollection.append(
            {
                'instruction':instruction,
                'quantity':abs(quantity),
                'instrument': {
                        'symbol': symbol,
                        'assetType':'EQUITY'
                }
            })

    def _validate(self):
        """
        """
        return 1


class Option(Order):
    """
    Subclass of Order class used to create orders that are fed to the 
    tda client class.  Used for options orders
    """
    def __init__(
        self, 
        complexOrderStrategyType='NONE',
        **kwargs
    ):
        """
        """
        super().__init__()

        self.complexOrderStrategyType = complexOrderStrategyType
        self.__dict__.update(kwargs)

    def add_leg(self, symbol, quantity, closing=False):
        """
        Add leg to an Equity Order

            args: 
                symbol (type: string)
                    symbol code of option to trade
                quantity (type: int)
                    quantity for transaction (negative to sell short position)
                closing (type: bool)
                    is the order closing an existing trade
        """
        if closing:
            if quantity > 0:
                instruction = Const.Instructions.BUY_TO_CLOSE
            else:
                instruction = Const.Instructions.SELL_TO_CLOSE
        else:
            if quantity > 0:
                instruction = Const.Instructions.BUY_TO_OPEN
            else:
                instruction = Const.Instructions.SELL_TO_OPEN

        self.orderLegCollection.append(
            {
                'instruction':instruction,
                'quantity':abs(quantity),
                'instrument': {
                        'symbol': symbol,
                        'assetType:':'OPTION'
                }
            })

    def _validate(self):
        """
        """
        return 1



        