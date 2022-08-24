class InvalidOrder(Exception):
    """
    """
    def __init__(self):
        super().__init__("Current order is not valid")

class NotAuthorized(Exception):
    """
    """
    def __init__(self):
        super().__init__("Current session not authorized")