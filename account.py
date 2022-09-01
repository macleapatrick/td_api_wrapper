from orders import Equity, Option 

class Account:
    """
    Class to represent tda account with current balances, status
    and opened positions.  Class designed to be nested inside
    of client class.
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
        if self._account_id == '':
            self._account_id = account_id
        else:
            raise Exception("Account id already is already assigned")

    def update(self, response):
        """
        Take raw response from api and update objects
        """
        response = response['securitiesAccount']

        if response.get('positions', None) is not None:
            positions = response.pop('positions', None)
            self.positions.parse(positions)

        self.__dict__.update(response)
    

class Positions(dict):
    """
    subclass of dict as a container to store the accounts currently opened
    positions.  Each item in dict in another object storing data for
    the given position. 
    """
    def __init__(self):
        pass

    def __repr__(self):
        return f"<Class: '{self.__class__.__name__}', Number Of Positions: '{len(self)}'>"

    def parse(self, positions):
        """
        Parse list object recieved by client into corresponding objects stored 
        in this container class
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
    Stores data for opened position on account
    """
    def __init__(self, position):

        instrument = position.pop('instrument')

        self.__dict__.update({kw : position[kw] for kw in position.keys()})
        self.__dict__.update({kw : instrument[kw] for kw in instrument.keys()})

    def __repr__(self):
        return f"<Class: '{self.__class__.__name__}', "\
               f"Asset: '{self.assetType}', "\
               f"Ticket: '{self.symbol}', "\
               f"Average: '${self.averagePrice}', "\
               f"Quantity: '{max(self.longQuantity,self.shortQuantity)}', "\
               f"Market Value: '${self.marketValue}'>"
                  
    def sub(self):
        if self.longQuantity:  
            return -self.longQuantity
        elif self.shortQuantity:
            return self.shortQuantity

    def add(self):
        if self.longQuantity:  
            return self.longQuantity
        elif self.shortQuantity:
            return -self.shortQuantity


class EquityPosition(Position):
    """
    Subclass of position, stores data for opened equity position on account
    contains methods to modify existing position
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
            quantity=self.sub(),
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
            quantity=int(self.add()*percent/100)
        )
        return order

    def form_sub_order(self, percent, **kwargs):
        """
        Form order object that will reduce this position
        """
        order = Equity(**kwargs)
        order.add_leg(
            symbol=self.symbol,
            quantity=int(self.sub()*percent/100)
        )
        return order


class OptionsPosition(Position):
    """
    Subclass of position, stores data for opened options position on account
    contains methods to modify existing position
    """
    def __init__(self, position):
        super().__init__(position)
    
    def form_close_order(self, **kwargs):
        """
        Form order object that will close this position
        """
        order = Option(**kwargs)
        order.add_leg(
            symbol=self.symbol, 
            quantity=self.sub(),
            closing=True
        )
        return order

    def form_add_order(self, percent, **kwargs):
        """
        Form order object that will add to this position
        """
        order = Option(**kwargs)
        order.add_leg(
            symbol=self.symbol,
            quantity=int(self.add()*percent/100)
        )
        return order
    
    def form_sub_order(self, percent, **kwargs):
        """
        Form order object that will reduce this position
        """
        order = Option(**kwargs)
        order.add_leg(
            symbol=self.symbol,
            quantity=int(self.sub()*percent/100)
        )
        return order


        