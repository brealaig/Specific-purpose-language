class Interpreter:
    def __init__(self):
        # Global environment to store variables, functions, recipes, etc.
        self.global_env = {}

    def run(self, abstract_syntax_tree):
        """
        Execute the Abstract Syntax Tree (AST), which is assumed to be a list of AST nodes.
        """
        for node in abstract_syntax_tree:
            self.visit(node)

    def visit(self, node):
        """
        Dispatch the node to the appropriate visitor method based on its 'node_type'.
        """
        node_type = node.get("node_type")
        method_name = "visit_" + node_type
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception("No visitor method defined for node type: " + str(node.get("node_type")))

    # ------------------ Visitor Methods for AST Nodes ------------------

    def visit_recipe(self, node):
        """
        Processes a recipe node.
        Expected node structure:
          - "name": recipe name.
          - "input": list of items (each item is a dict with "position", "quantity", "material").
          - "output": name of the resulting item.
          - "tool_required": required tool.
          - "quantity": output quantity.
        """
        print(f"Processing recipe: {node['name']}")
        print("Input materials:")
        for item in node["input"]:
            print(f"  Place {item['quantity']} of {item['material']} at position {item['position']}")
        print(f"Output: {node['output']}")
        print(f"Required tool: {node['tool_required']}")
        print(f"Quantity: {node['quantity']}")
        return None

    def visit_function_definition(self, node):
        """
        Processes a function definition node.
        Expected node structure:
          - "name": function name.
          - "params": list of parameters.
          - "body": list of AST nodes representing the function body.
        """
        # Store the function definition in the global environment.
        self.global_env[node["name"]] = node
        print(f"Defined function: {node['name']}")
        return None

    def visit_assignment(self, node):
        """
        Processes an assignment node.
        Expected node structure:
          - "identifier": variable name.
          - "expression": AST node representing the expression.
        """
        value = self.visit(node["expression"])
        self.global_env[node["identifier"]] = value
        return value

    def visit_conditional(self, node):
        """
        Processes a conditional node.
        Expected node structure:
          - "condition": AST node for the condition.
          - "then_branch": list of AST nodes for the 'if' block.
          - "else_branch": (optional) list of AST nodes for the 'else' block.
        """
        condition = self.visit(node["condition"])
        if condition:
            for stmt in node["then_branch"]:
                self.visit(stmt)
        elif node.get("else_branch") is not None:
            for stmt in node["else_branch"]:
                self.visit(stmt)
        return None

    def visit_while_loop(self, node):
        """
        Processes a while loop node.
        Expected node structure:
          - "condition": AST node for the loop condition.
          - "body": list of AST nodes for the loop body.
        """
        while self.visit(node["condition"]):
            for stmt in node["body"]:
                self.visit(stmt)
        return None

    def visit_for_loop(self, node):
        """
        Processes a for loop node.
        Expected node structure:
          - "init": AST node for the initialization.
          - "condition": AST node for the loop condition.
          - "post": AST node for the post-loop assignment.
          - "body": list of AST nodes for the loop body.
        """
        self.visit(node["init"])
        while self.visit(node["condition"]):
            for stmt in node["body"]:
                self.visit(stmt)
            self.visit(node["post"])
        return None

    def visit_log(self, node):
        """
        Processes a log command node.
        Expected node structure:
          - "expression": AST node to be evaluated and logged.
        """
        value = self.visit(node["expression"])
        print(f"LOG: {value}")
        return value

    def visit_craft_command(self, node):
        """
        Processes a craft command node.
        Expected node structure:
          - "recipe_name": name of the recipe to craft.
        """
        recipe_name = node["recipe_name"]
        print(f"Craft command invoked for recipe: {recipe_name}")
        return None

    def visit_binary_expression(self, node):
        """
        Processes a binary expression node.
        Expected node structure:
        - "operator": operator string (e.g., '+', '-', etc.).
        - "left": left operand (AST node).
        - "right": right operand (AST node).
        """
        left = self.visit(node["left"])
        right = self.visit(node["right"])
        op = node["operator"]

        if op == "+":
            # Attempt numeric addition; if conversion fails, perform string concatenation.
            try:
                return float(left) + float(right)
            except (ValueError, TypeError):
                # Replace None with an empty string if necessary.
                if left is None:
                    left = ""
                if right is None:
                    right = ""
                return str(left) + str(right)
        elif op == "-":
            return float(left) - float(right)
        elif op == "*":
            return float(left) * float(right)
        elif op == "/":
            return float(left) / float(right)
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        elif op == "<":
            return float(left) < float(right)
        elif op == ">":
            return float(left) > float(right)
        elif op == "<=":
            return float(left) <= float(right)
        elif op == ">=":
            return float(left) >= float(right)
        else:
            raise Exception("Unsupported operator: " + op)

    def visit_literal(self, node):
        """
        Processes a literal node (number or string).
        Expected node structure:
          - "value": the literal value as a string.
        """
        value = node["value"]
        # If it's a string literal, remove quotes.
        if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        try:
            return float(value)
        except ValueError:
            return value

    def visit_identifier(self, node):
        """
        Processes an identifier node.
        Expected node structure:
          - "name": variable name.
        """
        name = node["name"]
        if name in self.global_env:
            return self.global_env[name]
        else:
            raise Exception("Undefined variable: " + name)
