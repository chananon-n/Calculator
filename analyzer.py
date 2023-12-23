import re

# Define token patterns
token_patterns = [
    (r'\d+', 'INT'),  # Match integers
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
                if token_type != 'INT':
                    tokens.append(f"{value}/{token_type}")
                else:
                    tokens.append(value)
                input_string = input_string[len(value):].lstrip()
                break
        else:
            # If no pattern matched, raise an error
            raise ValueError(f"Unexpected character: {input_string[0]}")
    return tokens

# Examples
examples = [
    "23-9",
    "2.5*0",
    "5NUM^3.0",
    "x=5",
    "10*x",
    "x=y",
    "x!=5",
    "X#+8",
]

for example in examples:
    try:
        result = tokenize(example)
        print(f"{example} => {' '.join(result)}")
    except ValueError as e:
        print(f"Error: {e}")
