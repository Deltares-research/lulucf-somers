class InvalidLassoError(Exception):
    def __init__(self, message, errors=None):
        self.message = f"{message}\n{'\n'.join(errors)}"


class InvalidBoundsError(Exception):
    def __init__(self, message):
        self.message = message
