from interpreter.semantic_analyzer.semantic_error import SemanticError

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, abstract_syntax_tree):
        for node in abstract_syntax_tree:
            self.visit(node)
        return abstract_syntax_tree

    def visit(self, node):
        if node is None:
            return None
        node_type = node.get("node_type")
        # Si el nodo es una receta, usaremos el método visit_recipe
        if node_type == "recipe":
            return self.visit_recipe(node)
        method_name = "visit_" + node_type if node_type else "generic_visit"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if node is None:
            return None
        for key, value in node.items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self.visit(item)
            elif isinstance(value, dict):
                self.visit(value)
        return node

    def visit_assignment(self, node):
        identifier = node.get("identifier")
        self.symbol_table[identifier] = True
        self.visit(node.get("expression"))
        return node

    def visit_identifier(self, node):
        name = node.get("name")
        if name not in self.symbol_table:
            raise SemanticError(f"Undefined variable '{name}'")
        return node

    def visit_function_definition(self, node):
        self.symbol_table[node.get("name")] = True
        for param in node.get("params", []):
            self.symbol_table[param] = True
        for stmt in node.get("body", []):
            self.visit(stmt)
        return node

    def visit_recipe(self, node):
        """
        Valida que, si la herramienta requerida es 'crafting_table', las posiciones en el input estén entre 0 y 2.
        """
        if node.get("tool_required", "").lower() == "crafting_table":
            input_items = node.get("input", [])
            for item in input_items:
                try:
                    row = int(item["position"][0])
                    col = int(item["position"][1])
                except Exception as e:
                    raise SemanticError(f"Invalid position format for item: {item}")
                if row < 0 or row > 2 or col < 0 or col > 2:
                    raise SemanticError(f"Invalid position {item['position']} for item '{item.get('material', 'unknown')}'. Indices must be between 0 and 2.")
        # Continúa visitando los subnodos, si existen
        return self.generic_visit(node)
