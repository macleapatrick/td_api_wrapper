import re

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
            self[symbol] = Position(positions[i])


class Position:
    """
    """
    def __init__(self, position):

        instrument = position['instrument']

        self.assetType = instrument.get('assetType', None)
        self.cusip = instrument.get('cusip', None)
        self.symbol = instrument.get('symbol', None)
        self.description = instrument.get('description', None)
        self.putCall = instrument.get('putCall', None)
        self.underlyingSymbol = instrument.get('underlyingSymbol', None)
        
        self.shortQuantity = position.get('shortQuantity', None)
        self.averagePrice = position.get('averagePrice', None)
        self.currentDayCost = position.get('currentDayCost', None)
        self.currentDayProfitLoss = position.get('currentDayProfitLoss ', None)
        self.currentDayProfitLossPercentage = position.get('currentDayProfitLossPercentage', None)
        self.longQuantity = position.get('longQuantity', None)
        self.settledLongQuantity = position.get('settledLongQuantity', None)
        self.settledShortQuantity = position.get('settledShortQuantity', None)
        self.marketValue = position.get('marketValue', None)
        self.maintenanceRequirement = position.get('maintenanceRequirement', None)
        self.previousSessionLongQuantity = position.get('previousSessionLongQuantity', None)

    def form_close_order(self):
        """
        Form order object that will close this position
        """
        return

    def form_add_order(self, quantity):
        """
        Form order object that will add the given quantity to the position
        """
        return

    

        