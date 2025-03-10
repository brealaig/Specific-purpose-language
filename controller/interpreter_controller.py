import json
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor, QFont
from interpreter.run_interpretation_process import run_interpretation_process
from interpreter.lexical_analyzer.lexical_error import LexicalError
from interpreter.syntax_analyzer.syntax_error import SyntaxError
from interpreter.semantic_analyzer.semantic_error import SemanticError

class InterpreterController(QObject):
    interpretationFinished = pyqtSignal(object)

    def __init__(self, code_editor, crafting_table, debug_panel, parent=None):
        super().__init__(parent)
        self.code_editor = code_editor
        self.crafting_table = crafting_table
        self.debug_panel = debug_panel

    def debug_append(self, msg, color="black", bold=False):
        current_font = self.debug_panel.font()
        new_font = QFont(current_font)
        new_font.setBold(bold)
        self.debug_panel.setCurrentFont(new_font)
        self.debug_panel.setTextColor(QColor(color))
        self.debug_panel.append(msg)

    def interpret_code(self):
        if hasattr(self.debug_panel, 'clear'):
            self.debug_panel.clear()
        else:
            print("Debug panel does not support clear()")
        
        self.debug_append("Starting interpretation process...", color="blue", bold=True)
        code = self.code_editor.toPlainText()

        try:
            recipe_ast = run_interpretation_process(code)
        except LexicalError as le:
            self.debug_append("Lexical Error:\n" + str(le), color="red", bold=True)
            return
        except SyntaxError as se:
            self.debug_append("Syntax Error:\n" + str(se), color="red", bold=True)
            return
        except SemanticError as sme:
            self.debug_append("Semantic Error:\n" + str(sme), color="red", bold=True)
            return
        except Exception as e:
            self.debug_append("Unknown Error:\n" + str(e), color="red", bold=True)
            return

        if recipe_ast is None:
            self.debug_append("Interpretation failed due to errors.", color="red", bold=True)
            return

        if isinstance(recipe_ast, list):
            if len(recipe_ast) > 0:
                recipe_ast = recipe_ast[0]
            else:
                self.debug_append("No recipe found in the code.", color="red", bold=True)
                return

        self.crafting_table.update_from_ast(recipe_ast)
        self.debug_append("Interpretation completed successfully.", color="green", bold=True)

        try:
            ast_details = json.dumps(recipe_ast, indent=4)
            self.debug_append("", color="black")
            self.debug_append("AST Details:", color="black", bold=True)
            self.debug_append(ast_details, color="darkblue")
        except Exception as e:
            self.debug_append("Error formatting AST details: " + str(e), color="red", bold=True)

        self.interpretationFinished.emit(recipe_ast)
