from exceptions import InvalidOrder


class OrderHistory(list):
    """
    """
    def __init__(self):
        super().__init__(self)

    def __getitem__(self, orderId):
        for order in self:
            if order.orderId == orderId:
                return order
            else:
                return 0 


class Order():
    """
    Order can only be used to complete a single order, once the order is placed, the object
    is stored in the order history 
    """
    def __init__(
        self,
        orderType='MARKET',
        session='NORMAL',
        duration='DAY',
        orderStrategyType='SINGLE',
        **kwargs
        ):

        self._orderId = None
        self._status = None

        self.orderType = orderType
        self.session = session
        self.duration = duration
        self.orderStrategyType = orderStrategyType
        self.orderLegCollection = []
        self.__dict__.update(kwargs)

    @property
    def orderId(self):
        return self._orderId

    @orderId.setter
    def orderId(self, orderId):
        self._orderId = orderId

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    def form(self):
        """
        """
        if self._validate():
            order = {}
            for kv in self.__dict__.keys():
                if self.__dict__[kv] is not None:
                    order[kv] = self.__dict__[kv]
            return order
        else:
            raise InvalidOrder

    def update(self, orderInfo):
        """
        Update the order instance with the json provider by td
        """
        self.__dict__.update(orderInfo)

    def _validate(self):
        """
        """
        pass


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



        