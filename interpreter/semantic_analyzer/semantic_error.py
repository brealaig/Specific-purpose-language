class SemanticError(Exception):
    def __init__(self, message):
        super().__init__(f"Semantic Error: {message}")