import re

lexical_grammar = [
    ('INT', r'\d+'),                 # Integer
    ('REAL', r'\d+\.\d+'),           # Real number
    ('POW', r'\^'),                   # Exponentiation
    ('VAR', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Variable
    ('PLUS', r'\+'),                  # Addition
    ('MINUS', r'-'),                  # Subtraction
    ('TIMES', r'\*'),                 # Multiplication
    ('DIVIDE', r'/'),                 # Division
    ('ASSIGN', r'='),                 # Assignment
    ('NEQ', r'!='),                   # Not Equal
    ('LPAREN', r'\('),                # Left Parenthesis
    ('RPAREN', r'\)'),                # Right Parenthesis
    ('WS', r'\s+'),                   # Whitespace
    ('ERR', r'.'),                    # Error
]

def format_output(grammar):
    for token_type, regex in grammar:
        print(f"{token_type} {regex}")

# Display the formatted output
format_output(lexical_grammar)
