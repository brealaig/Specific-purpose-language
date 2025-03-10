from interpreter.lexical_analyzer.lexer import Lexer
from interpreter.syntax_analyzer.parser import Parser
from interpreter.semantic_analyzer.semantic_analyzer import SemanticAnalyzer
from interpreter.evaluator.interpreter import Interpreter

def run_interpretation_process(code):
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    abstract_syntax_tree = parser.parse()
    print("Syntactic analysis completed successfully.")

    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.analyze(abstract_syntax_tree)
    print("Semantic analysis completed successfully.")

    interpreter = Interpreter()
    interpreter.run(abstract_syntax_tree)

    if isinstance(abstract_syntax_tree, dict) and "recipe" in abstract_syntax_tree:
        return abstract_syntax_tree["recipe"]
    else:
        return abstract_syntax_tree

if __name__ == "__main__":
    code = """
        func calculate_area(length, width) {
            result = length * width;
            if (result > 100) {
                log("Large area calculated");
            } else {
                log("Small area calculated");
            }
        }

        recipe bread {
            input: [ (0,0) 1 wheat, (0,1) 1 wheat, (0,2) 1 wheat ];
            output: bread;
            tool_required: crafting_table;
            quantity: 1;
        }

        func greet_user(name) {
            log("Hello, " + name);
        }

        func countdown(number) {
            while (number > 0) {
                log("Countdown: " + number);
                number = number - 1;
            }
            log("Countdown finished");
        }

        func repeat_task(times) {
            for (i = 1; i <= times; i = i + 1) {
                log("Task repetition #" + i);
            }
        }

        func test_semantic_error() {
            log("Testing semantic error: " + undefined_variable);
        }
    """
    ast = run_interpretation_process(code)
    print("AST returned:", ast)

