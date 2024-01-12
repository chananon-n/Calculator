
def parse_expression(tokens):
    operators = set(['+', '-', '*', '/', '^'])

    stack = []
    for token in tokens:
        parts = token.split()
        if len(parts) == 2:
            token_type, value = parts
            if token_type == 'INT' or token_type == 'REAL' or token_type == 'VAR':
                stack.append(value)
            elif value in operators:
                if len(stack) < 2:
                    raise SyntaxError("Not enough operands for operator")
                operand2 = stack.pop()
                operand1 = stack.pop()
                stack.append(f"({operand1}{value}{operand2})")
            else:
                raise SyntaxError(f"Invalid token in expression: {value}")
        elif len(parts) == 1 and parts[0] == 'ERR':
            raise SyntaxError("Error token in expression")
        else:
            # Handle other cases or raise an error if needed
            raise SyntaxError(f"Invalid token format: {token}")

    if len(stack) != 1:
        raise SyntaxError("Invalid expression")

    return stack[0]


def parse_assignment(tokens):
    if '=' not in [token.split()[1] for token in tokens if token.split()[0] == 'ASSIGN']:
        raise SyntaxError("No '=' found in assignment")

    index_of_equals = [i for i, token in enumerate(tokens) if token.split()[1] == '='][0]

    if index_of_equals != 1 or not tokens[0].split()[0] == 'VAR':
        raise SyntaxError("Invalid assignment format")

    variable = tokens[0].split()[1]
    expression_tokens = tokens[index_of_equals + 1:]

    try:
        expression_result = parse_expression(expression_tokens)
        return f"({variable}={expression_result})"
    except SyntaxError as e:
        raise SyntaxError(e)


def main():
    input_filename = "64011366_64011397.tok"
    output_filename = "64011366_64011397.bracket"

    with open(input_filename, 'r') as file:
        input_lines = file.readlines()

    with open(output_filename, 'w') as output_file:
        for i, input_line in enumerate(input_lines, start=1):
            tokens = input_line.strip()

            try:
                if '=' in [token.split()[1] for token in tokens if token.split()[0] == 'ASSIGN']:
                    result = parse_assignment(tokens)
                else:
                    result = parse_expression(tokens)

                output_file.write(f"({result})\n")
            except SyntaxError as e:
                output_file.write(f"SyntaxError at line {i}, pos {e.args[0]}\n")
            except NameError as e:
                output_file.write(f"Undefined variable {e.args[0]} at line {i}, pos {e.args[1]}\n")


if __name__ == "__main__":
    main()
