import re


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
        self.positions = {}
        self.orderStrategies = {}
    
    def __str__(self):
        return f"ACCOUNT ID: {self.account_id}\n" + \
               f"ACCOUNT TYPE: {self.type}\n" + \
               f"LIQUIDATION VALUE: {self.currentBalances['liquidationValue']}\n" + \
               f"OPENED POSITIONS: {len(self.positions)}"          

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        self._account_id = account_id

    def parse_response(self, r):
        d = r['securitiesAccount']
        self.type = d.get('type')
        self.roundTrips = d.get('roundTrips')
        self.isDayTrader = d.get('isDayTrader')
        self.isClosingOnlyRestricted = d.get('isClosingOnlyRestricted')
        self.initalBalances = d.get('initialBalances', {})
        self.currentBalances = d.get('currentBalances', {})
        self.projectedBalances = d.get('projectedBalances', {})
        self.positions = d.get('positions', {})
        self.orderStrategies = d.get('orderStrategies', {})
    
    def account_overview(self):
        """
        prints all account details into console including account id, type,
        current balances, and opened positions. 
        """
        print(f"ACCOUNT ID: {self.account_id}")
        print(f"ACCOUNT TYPE: {self.type}")


        print('\nINITAL BALANCES:')
        self.print_dict(self.initalBalances, prefix=' '*4)


        print('\nCURRENT BALANCES:')
        self.print_dict(self.currentBalances, prefix=' '*4)


        print('\nOPENED POSITIONS:')
        for i, position in enumerate(self.positions):
            print(f"\n    POSITION {i}:")
            self.print_dict(position['instrument'], prefix=' '*8)
            self.print_dict(position, prefix=' '*12, ignore=['instrument'])

    @staticmethod
    def convert_case(s):
        """
        """
        return ' '.join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', s)).split()).capitalize()

    def print_dict(self, d, prefix='', ignore=[]):
        """
        """
        for kv in d.keys():
            if kv not in ignore:
                print(f"{prefix}{self.convert_case(kv)}: {d[kv]}")
    
