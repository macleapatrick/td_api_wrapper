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

        print('\n')

        print('INITAL BALANCES:')
        for kv in self.initalBalances.keys():
            print(f"    {self.convert_case(kv)}: $ {self.initalBalances[kv]}")

        print('\n')

        print('CURRENT BALANCES:')
        for kv in self.currentBalances.keys():
            print(f"    {self.convert_case(kv)}: $ {self.currentBalances[kv]}")

        print('\n')
        
        print('OPENED POSITIONS:')
        for position in self.positions:
            for kv in position['instrument'].keys():
                print(f"    {self.convert_case(kv)}: {position['instrument'][kv]}")
            for kv in position.keys():
                if kv == 'instrument':
                    continue
                else:
                    print(f"        {self.convert_case(kv)}: {position[kv]}")
            print('\n')

    @staticmethod
    def convert_case(s):
        """
        """
        return ' '.join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', s)).split()).capitalize()
    
