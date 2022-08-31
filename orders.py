from exceptions import InvalidOrder
from enumerations import Const

class OrderHistory(dict):
    """
    """
    def __init__(self):
        super().__init__(self)


class RecievedOrder:
    """
    Data Container for order infomation recieved from TDA
    """
    def __init__(self):
        pass


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
        self.__dict__.update(kwargs)

    def form(self):
        """
        """
        if self._validate():
            return self.__dict__
        else:
            raise InvalidOrder

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

    def set_duration(self, gtc=False, fof=False):
        """
        Sets order to 'Good till canceled' or 'Fill or Kill'
        Only needed if not using the default 'DAY'
        """
        if gtc:
            self.duration = Const.Duration.GOOD_TILL_CANCLED
        elif fof:
            self.duration = Const.Duration.FILL_OR_KILL

    def session(self, am=False, pm= False, seamless=False):
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
                    specify if this is a order to close position

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



        