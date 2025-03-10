class LexicalError(Exception):
    def __init__(self, message, position):
        super().__init__(f"Lexical error at position {position}: {message}")
        self.position = position