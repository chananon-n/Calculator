import re

# Define token patterns
token_patterns = [
    (r'\d+\.\d+', '/REAL'), # Match real numbers
    (r'\d+', '/INT'),  # Match integers
    (r'[a-zA-Z_][a-zA-Z0-9_]*', '/VAR'),  # Match variables
    (r'\+', '/+'),  # Match addition
    (r'-', '/-'),  # Match subtraction
    (r'\*', '/*'),  # Match multiplication
    (r'/', '/'),  # Match division
    (r'\^', '/POW'),  # Match exponentiation
    (r'=', '/='),
    (r'!=', '/!='),
    (r'\(', '(/LPAREN'),
    (r'\)', ')/RPAREN'),
    (r'\s+', '/SKIP'),  # Skip whitespace
    (r'.', '/^/ERR'),  # Match any other character as an error
]

def tokenize(input_string):
    tokens = []
    while input_string:
        for pattern, token_type in token_patterns:
            match = re.match(pattern, input_string)
            if match:
                value = match.group(0)
                tokens.append(f"{value}{token_type} ")
                input_string = input_string[len(value):].lstrip()
                break
        else:
            # If no pattern matched, raise an error
            raise ValueError(f"Unexpected character: {input_string[0]}")
    return tokens


