class InvalidLassoError(Exception):
    def __init__(self, message):
        self.message = message


class InvalidBoundsError(Exception):
    def __init__(self, message):
        self.message = message
