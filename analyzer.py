import re

# Define token patterns
token_patterns = [
    (r'\d+(\.\d+)?', 'REAL'),  # Match integers and decimals
    (r'[a-zA-Z_][a-zA-Z0-9_]*', 'VAR'),  # Match variables
    (r'\+', '+/INT'),  # Match addition
    (r'-', '-/INT'),  # Match subtraction
    (r'\*', '*/INT'),  # Match multiplication
    (r'/', '/INT'),  # Match division
    (r'\^', '^/POW'),  # Match exponentiation
    (r'=', '=/='),
    (r'!=', '!=/!='),
    (r'\(', '(/LPAREN'),
    (r'\)', ')/RPAREN'),
    (r'\s+', 'SKIP'),  # Skip whitespace
    (r'.', '^/ERR'),  # Match any other character as an error
]

def tokenize(input_string):
    tokens = []
    while input_string:
        for pattern, token_type in token_patterns:
            match = re.match(pattern, input_string)
            if match:
                value = match.group(0)
                tokens.append(f"{value}/{token_type}")
                input_string = input_string[len(value):].lstrip()
                break
        else:
            # If no pattern matched, raise an error
            raise ValueError(f"Unexpected character: {input_string[0]}")
    return tokens

