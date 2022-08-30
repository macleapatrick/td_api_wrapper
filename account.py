

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

        instrument = position.pop('instrument')

        self.__dict__.update({kw : position[kw] for kw in position.keys()})
        self.__dict__.update({kw : instrument[kw] for kw in instrument.keys()})
        
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

    

        