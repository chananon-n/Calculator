
def parse_expression(tokens):
    operators = set(['+', '-', '*', '/', '^', '=','!='])
    stack = []
    for token in tokens:
        parts = token.split('/')
        if len(parts) == 2:
            value,token_type = parts
            if token_type == 'INT' or token_type == 'REAL' or token_type == 'VAR':
                stack.append(value)
                if len(stack) >= 2 and stack[-2] in operators:
                    operand2 = stack.pop()
                    operator = stack.pop()
                    operand1 = stack.pop()
                    stack.append(f"({operand1}{operator}{operand2})")
            elif value in operators:
                stack.append(value)
            else:
                raise SyntaxError(f"Invalid token in expression: {value}")
        elif len(parts) == 1 and parts[0] == 'ERR':
            raise SyntaxError("Error token in expression")
        else:
            raise SyntaxError(f"Invalid token format: {token}")

    if len(stack) != 1:
        raise SyntaxError("Invalid expression")

    return stack[0]

def parse_assignment(tokens):
    if '=' not in [token.split('/')[2] for token in tokens if token.split('/')[0] == 'VAR']:
        raise SyntaxError("No '=' found in assignment")

    index_of_equals = [i for i, token in enumerate(tokens) if token.split('/')[2] == '='][0]

    if index_of_equals != 1 or not tokens[0].split('/')[0] == 'VAR':
        raise SyntaxError("Invalid assignment format")

    variable = tokens[0].split('/')[1]
    expression_tokens = tokens[index_of_equals + 1:]

    try:
        expression_result = parse_expression(expression_tokens)
        return f"({variable}={expression_result})"
    except SyntaxError as e:
        raise SyntaxError(e)

