from flask import Flask, request, jsonify


# Node class to represent conditions or operators in the tree (AST)
class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type  # 'operator' (AND/OR) or 'operand' (condition like "age > 30")
        self.left = left  # Left child node (for AND/OR operators)
        self.right = right  # Right child node
        self.value = value  # Condition (e.g., "age > 30") or operator (e.g., "AND")


# Function to create the AST from a rule string
def create_rule(rule_string):
    # Split by AND (you can extend this to handle complex rules with OR, etc.)
    if "AND" in rule_string:
        conditions = rule_string.split("AND")
        left_condition = conditions[0].strip()
        right_condition = conditions[1].strip()

        # Create operand nodes for the conditions
        left_node = Node(node_type="operand", value=left_condition)
        right_node = Node(node_type="operand", value=right_condition)

        # Create a root node for the AND operator
        return Node(node_type="operator", value="AND", left=left_node, right=right_node)
    elif "OR" in rule_string:
        conditions = rule_string.split("OR")
        left_condition = conditions[0].strip()
        right_condition = conditions[1].strip()

        # Create operand nodes for the conditions
        left_node = Node(node_type="operand", value=left_condition)
        right_node = Node(node_type="operand", value=right_condition)

        # Create a root node for the OR operator
        return Node(node_type="operator", value="OR", left=left_node, right=right_node)


# Function to evaluate the AST against user data
def evaluate_rule(node, user_data):
    if node.node_type == "operand":
        # Extract the condition and split it into parts
        attribute, operator, threshold = node.value.split()
        user_value = user_data.get(attribute)

        # Simple evaluation logic (extend as needed)
        if operator == ">":
            return user_value > int(threshold)
        elif operator == "<":
            return user_value < int(threshold)
        elif operator == "==":
            return user_value == threshold

    elif node.node_type == "operator":
        # Recursively evaluate left and right child nodes
        left_result = evaluate_rule(node.left, user_data)
        right_result = evaluate_rule(node.right, user_data)

        # Return result based on operator type (AND/OR)
        if node.value == "AND":
            return left_result and right_result
        elif node.value == "OR":
            return left_result or right_result


# Initialize the Flask application
app = Flask(__name__)


# API endpoint to create a rule and return the AST (for testing purposes)
@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    rule_string = request.json.get('rule')
    rule_ast = create_rule(rule_string)  # Parse rule string into AST
    return jsonify({"ast": str(rule_ast)})


# API endpoint to evaluate the rule against user data
@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    rule_string = request.json.get('rule')  # Rule string (e.g., "age > 30 AND salary > 50000")
    user_data = request.json.get('data')  # User data (e.g., {"age": 35, "salary": 60000})

    rule_ast = create_rule(rule_string)  # Convert rule string into AST
    result = evaluate_rule(rule_ast, user_data)  # Evaluate the AST against user data

    return jsonify({"result": result})


# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)
