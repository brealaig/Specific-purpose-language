from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont
from PyQt5.QtCore import Qt, QRegExp


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super(CodeEditor, self).__init__(parent)
        self.setFont(QFont("Consolas", 10))
        self.highlighter = SyntaxHighlighter(self.document())

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super(SyntaxHighlighter, self).__init__(document)
        self.highlightingRules = []

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.darkBlue)
        keywordFormat.setFontWeight(QFont.Bold)
        keywords = [
            "func", "recipe", "input", "output", "tool_required", "quantity",
            "if", "else", "while", "for", "craft", "log", "return", "int", "float", "char"
        ]
        for keyword in keywords:
            pattern = QRegExp(r"\b" + keyword + r"\b")
            self.highlightingRules.append((pattern, keywordFormat))
        
        numberFormat = QTextCharFormat()
        numberFormat.setForeground(Qt.darkRed)
        pattern = QRegExp(r"\b\d+(\.\d+)?\b")
        self.highlightingRules.append((pattern, numberFormat))
        
        stringFormat = QTextCharFormat()
        stringFormat.setForeground(Qt.darkGreen)
        pattern = QRegExp(r'"[^\"]*"')
        self.highlightingRules.append((pattern, stringFormat))
        
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(Qt.gray)
        pattern = QRegExp(r"//[^\n]*")
        self.highlightingRules.append((pattern, commentFormat))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)
