import re

def is_valid_variable_name(variable_name):
    return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', variable_name) is not None

def evaluate_expression(expr, variables):
    try:
        # Check for expressions within parentheses
        while '(' in expr and ')' in expr:
            # Find the innermost set of parentheses
            start = expr.rfind('(')
            end = expr.find(')', start)

            # Evaluate the expression within parentheses
            inner_expr = expr[start + 1:end]
            inner_result = evaluate_expression(inner_expr, variables)

            # Replace the expression within parentheses with its result
            expr = expr[:start] + str(inner_result) + expr[end + 1:]

        # Check for different comparison operators
        if '==' in expr:
            left, right = [part.strip() for part in expr.split('==')]
            left_value = variables.get(left, eval(left, variables))
            right_value = variables.get(right, eval(right, variables))
            result = left_value == right_value
        elif '>=' in expr:
            left, right = [part.strip() for part in expr.split('>=')]
            left_value = variables.get(left, eval(left, variables))
            right_value = variables.get(right, eval(right, variables))
            result = left_value >= right_value
        elif '<=' in expr:
            left, right = [part.strip() for part in expr.split('<=')]
            left_value = variables.get(left, eval(left, variables))
            right_value = variables.get(right, eval(right, variables))
            result = left_value <= right_value
        elif '!=' in expr:
            left, right = [part.strip() for part in expr.split('!=')]
            left_value = variables.get(left, eval(left, variables))
            right_value = variables.get(right, eval(right, variables))
            result = left_value != right_value
        else:
            # If it doesn't contain any of the specified operators, consider it a standalone expression
            result = eval(expr, variables)

        return result

    except Exception as e:
        raise ValueError(f"Error evaluating expression '{expr}': {str(e)}")

# Initialize an empty list to store the results
results = []

# Define the expressions in each line
# expressions = [
#     "4**2==16",
#     "x = 10",
#     "y = x // 3",
#     "x <= y",
#     "x >= y",
#     "y + 25.0",
#     "x != y",
#     "x != 3",
#     "5 != 5",
#     "5 >= 5",
#     "(2 + 3) * (4 - 1)",
#     "((x +y) * 2) / 3", 
#     "2 +3 ==5",
#     "(5+1) *2 == 12",
#     "(9+1) *2 == 20",
# ]

expressions = []

test_array = []
formatted_results = []
text_file = open("input.txt", "r")
line = text_file.readlines()

for k in line:
    test_array.append(k)

for j in test_array:
    formatted_result = f'{j.strip()}'
    expressions = line
    
text_file.close()

# Create a dictionary to store variable values
variables = {}

# Evaluate each expression and load the result into the 'results' list or update variables
for expr in line:
    try:
        variables_snapshot = variables.copy()
        # Check if "!=" is a standalone operator
        if "!=" in expr:
            left, right = [part.strip() for part in expr.split("!=")]
            left_value = variables.get(left, eval(left, variables))
            right_value = variables.get(right, eval(right, variables))
            result = left_value != right_value
        elif '==' in expr:
            left, right = [part.strip() for part in expr.split("==")]
            left_value = variables.get(left, eval(left, variables))
            right_value = variables.get(right, eval(right, variables))
            result = left_value == right_value

        # Check if ">=" is a standalone operator
        elif ">=" in expr:
            left, right = [part.strip() for part in expr.split(">=")]
            left_value = variables.get(left, eval(left, variables))
            right_value = variables.get(right, eval(right, variables))
            result = left_value >= right_value
        elif "<=" in expr:
            left, right = [part.strip() for part in expr.split("<=")]
            left_value = variables.get(left, eval(left, variables))
            right_value = variables.get(right, eval(right, variables))
            result = left_value <= right_value
        # Separate variable assignment from expression
        elif "=" in expr:
            variable_name, expr = [part.strip() for part in expr.split("=")]
            if not is_valid_variable_name(variable_name):
                raise ValueError(f"Invalid variable name: {variable_name}")

            result = evaluate_expression(expr, variables)
            variables[variable_name] = result
        # Handle other types of expressions
        else:
            result = evaluate_expression(expr, variables)
        results.append(result)

    except ValueError as ve:
        results.append(str(ve))

# Print the results
for i, result in enumerate(results):
    print(f"Line {i + 1}: {result}")



