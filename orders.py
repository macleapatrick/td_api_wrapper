from exceptions import InvalidOrder

class Order():
    """
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


class Equity(Order):
    """
    """
    def __init__(self, **kwargs):
        """
        """
        super().__init__()

        self.__dict__.update(kwargs)


    def add_leg(self, symbol, instruction, quantity):
        """
        """
        self.orderLegCollection.append(
            {
                'instruction':instruction,
                'quantity':quantity,
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
    def __init__(self, **kwargs):
        """
        """
        super().__init__()

        self.__dict__.update(kwargs)

    def add_leg(self, symbol, instruction, quantity):
        """
        """
        self.orderLegCollection.append(
            {
                'instruction':instruction,
                'quantity':quantity,
                'instrument': {
                        'symbol': symbol,
                        'assetType:':'OPTION'
                }
            })

    def _validate(self):
        """
        """
        return 1



        