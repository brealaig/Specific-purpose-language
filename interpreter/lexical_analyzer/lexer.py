from .lexeme import TOKEN_PATTERNS
from .lexical_error import LexicalError
import re

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.tokens = []

    def tokenize(self):
        while self.position < len(self.code):
            match_found = self._match_next_token()
            if not match_found:
                self._handle_invalid_character()
        return self.tokens
    
    def _match_next_token(self):
        for token_name, pattern in TOKEN_PATTERNS:
            match = pattern.match(self.code, self.position)
            if match:
                lexeme = match.group()
                position = self.position
                self.position = match.end()
                
                self._validate_token(token_name, lexeme, position)

                if token_name not in ("WHITESPACE", "COMMENT"):
                    self.tokens.append((token_name, lexeme, position))
                return True
        return False
    
    def _validate_token(self, token_name, lexeme, position):
        if token_name == "STRING" and not lexeme.endswith('"'):
            raise LexicalError("Unterminated string literal", position)
        elif token_name == "NUMBER":
            try:
                float(lexeme)
            except ValueError:
                raise LexicalError("Number literal overflow or invalid format", position)
    
    def _handle_invalid_character(self):
        current_char = self.code[self.position]
        position = self.position
        
        if current_char.isprintable():
            raise LexicalError(f"Invalid character '{current_char}'", position)
        else:
            raise LexicalError("Non-printable character detected", position)