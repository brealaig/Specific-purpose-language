class SyntaxError(Exception):
    def __init__(self, message, position):
        super().__init__(f"Syntax error at position {position}: {message}")
        self.position = position
