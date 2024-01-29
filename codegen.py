import re

def generate_assembly(expression):
    try:
        # Extract content within parentheses
        match = re.match(r'\(([^)]+)\)', expression)
        if not match:
            raise ValueError("SyntaxError: Invalid expression")

        inner_content = match.group(1)
        if "!=" in inner_content:
            variable, value = inner_content.split("!=")
            assembly_code = f"LD R0 #{value}\nLD R1 @{variable}\nFL.i R0 R0\nFL.i R1 R1\nNE.f R2 R0 R1\nST @print R2"
        elif "=" in inner_content:
            variable, value = inner_content.split("=")
            assembly_code = f"LD R0 #{value}\nST @{variable} R0"
        else:
            # Updated tokenization to group consecutive digits with a dot
            tokens = re.findall(r'\d*\.\d+|\d+|[^\d\s]', inner_content)
            if len(tokens) == 3:
                operand1, operator, operand2 = tokens
                if '.' in operand1 or '.' in operand2:
                    # If operands are floats
                    assembly_code = f"LD R0 #{operand1}\nLD R1 #{operand2}\nFL.i R0 R0\nFL.i R1 R1\n"
                else:
                    # If operands are integers
                    assembly_code = f"LD R0 #{operand1}\nLD R1 #{operand2}\n"

                if operator == '+':
                    assembly_code += f"ADD.i R2 R0 R1\nST @print R2"
                elif operator == '-':
                    assembly_code += f"SUB.i R2 R0 R1\nST @print R2"
                elif operator == '*':
                    assembly_code += f"MUL.f R2 R0 R1\nST @print R2"
                elif operator == '/':
                    assembly_code += f"DIV.f R2 R0 R1\nST @print R2"
                else:
                    raise ValueError("Unsupported operator")
            elif len(tokens) == 1:
                variable = tokens[0]
                assembly_code = f"LD R0 #{variable}\nST @print R0"
            else:
                raise ValueError("Invalid expression")
    except ValueError as e:
        assembly_code = "ERROR"
    print(assembly_code + "\n")

# # Example usage:
# expressions = [
#     "(23+8)",
#     "(2.5*0)",
#     "(x=5)",
#     "(10*x)",
#     "(x!=5)",
# ]

# for expr in expressions:
#     generate_assembly(expr)