from dis import Instruction
from orders import Equity, Option 

from enumerations import Const

class Account:
    """
    """
    def __init__(self, account_id=''):
        self._account_id = account_id

        self.type = None
        self.roundTrips = None
        self.isDayTrader = None
        self.isClosingOnlyRestricted = None
        
        self.initialBalances = {}
        self.currentBalances = {}
        self.projectedBalances = {}

        self.positions = Positions()
        self.orderStategies = []

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        self._account_id = account_id

    def update(self, response):

        response = response['securitiesAccount']

        if response.get('positions', None) is not None:
            positions = response.pop('positions', None)
            self.positions.parse(positions)

        self.__dict__.update(response)
    

class Positions(dict):
    """
    """
    def __init__(self):
        pass

    def parse(self, positions):
        """
        """
        symbols = [position['instrument']['symbol'] for position in positions]

        for symbol in self.keys():
            if symbol not in symbols:
                self.pop(symbol)

        for i, symbol in enumerate(symbols):

            assetType = positions[i]['instrument']['assetType']
            if assetType == 'EQUITY':
                self[symbol] = EquityPosition(positions[i])
            elif assetType == 'OPTION':
                self[symbol] = OptionsPosition(positions[i])


class Position:
    """
    """
    def __init__(self, position):

        instrument = position.pop('instrument')

        self.__dict__.update({kw : position[kw] for kw in position.keys()})
        self.__dict__.update({kw : instrument[kw] for kw in instrument.keys()})
        
    def form_close_order(self):
        pass

    def form_add_order(self):
        return


class EquityPosition(Position):
    """
    """
    def __init__(self, position):
        super().__init__(position)

    def form_close_order(self, **kwargs):
        """
        Form order object that will close this position
        """
        order = Equity(**kwargs)
        order.add_leg(
            symbol=self.symbol, 
            quantity=self.closing(),
            closing=True
        )
        return order

    def form_add_order(self, percent, **kwargs):
        """
        Form order object that will add to this position
        """
        order = Equity(**kwargs)
        order.add_leg(
            symbol=self.symbol,
            quantity=int(self.adding()*percent/100)
        )
        return order

    def closing(self):
        if self.longQuantity:  
            return -self.longQuantity
        elif self.shortQuantity:
            return self.shortQuantity

    def adding(self):
        if self.longQuantity:  
            return self.longQuantity
        elif self.shortQuantity:
            return -self.shortQuantity


class OptionsPosition(Position):
    """
    """
    def __init__(self, position):
        super().__init__(position)

        