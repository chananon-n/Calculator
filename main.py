import re
from analyzer import tokenize


def is_valid_variable_name(var):
    return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', var) is not None


def deleteFileContent(filename):
    with open(filename, "w"):
        pass


def writeLexicalAnalysisResult(res):
    # Open the file in append mode
    with open("64011366_64011397.tok", "a") as text_file:
        # Write the result to the file
        text_file.write(res + '\n')


def writeLexicalGrammarResult(result):
    with open("64011366_64011397.lex", "a") as text_file:
        text_file.write(result + '\n')


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

def readAndFormatFile(filename):
    res = []

    try:
        with open(filename, "r") as text_file:
            lines = text_file.readlines()

            for j in lines:
                temp = f"{j.strip()}"
                res.append(temp)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

    return res


# Initialize an empty list to store the results
results = []
# Create a dictionary to store variable values
variables = {}
# Read the file and format the results
formatted_results = readAndFormatFile("input.txt")
lexical_grammar = [
    ('INT', r'\d+'),  # Integer
    ('REAL', r'\d+\.\d+'),  # Real number
    ('POW', r'\^'),  # Exponentiation
    ('VAR', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Variable
    ('PLUS', r'\+'),  # Addition
    ('MINUS', r'-'),  # Subtraction
    ('TIMES', r'\*'),  # Multiplication
    ('DIVIDE', r'/'),  # Division
    ('ASSIGN', r'='),  # Assignment
    ('NEQ', r'!='),  # Not Equal
    ('LPAREN', r'\('),  # Left Parenthesis
    ('RPAREN', r'\)'),  # Right Parenthesis
    ('WS', r'\s+'),  # Whitespace
    ('ERR', r'.'),  # Error
]

# Evaluate each expression and load the result into the 'results' list or update variables
for expr in formatted_results:
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

# delete file content
deleteFileContent("64011366_64011397.tok")
deleteFileContent("64011366_64011397.lex")

# writing lexical analysis result
for i in formatted_results:
    try:
        result = tokenize(i)
        writeLexicalAnalysisResult(f"{''.join(result)}")
    except ValueError as e:
        print(f"Error: {e}")

# writing lexical grammar result
for token_type, regex in lexical_grammar:
    writeLexicalGrammarResult(f"{token_type} {regex}")

# Print the results
for i, result in enumerate(results):
    print(f"Line {i + 1}: {result}")
