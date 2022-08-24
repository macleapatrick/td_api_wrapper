class Account():
    """
    """
    def __init__(self, account_id=''):
        self._account_id = account_id
        self.type = ''
        self.roundTrips = 0
        self.isDayTrader = False
        self.isClosingOnlyRestricted = False
        self.initalBalances = {}
        self.currentBalances = {}
        self.projectedBalances = {}

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        self._account_id = account_id

    def parse_response(self, r):
        d = r['securitiesAccount']
        self.type = d['type']
        self.roundTrips = d['roundTrips']
        self.isDayTrader = d['isDayTrader']
        self.isClosingOnlyRestricted = d['isClosingOnlyRestricted']
        self.initalBalances = d['initialBalances']
        self.currentBalances = d['currentBalances']
        self.projectedBalances = d['projectedBalances']
