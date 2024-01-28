class CodeGenerator:
    def __init__(self):
        self.assembly_code = []
        self.var_counter = 0  # Counter for generating unique variable names

    def generate_code(self, expression):
        tokens = expression.split()
        if len(tokens) > 1:
            if tokens[1] == '+':
                self.generate_code(tokens[0])
                self.generate_code(tokens[2])
                self.add()
            elif tokens[1] == '*':
                self.generate_code(tokens[0])
                self.generate_code(tokens[2])
                self.multiply()
            elif tokens[1] == '=':
                self.assignment(tokens[0], tokens[2])
            elif tokens[1] == '!=':
                self.generate_code(tokens[0])
                self.generate_code(tokens[2])
                self.not_equal()
            else:
                self.handle_error()
        else:
            # If it's a single token, it can be a variable, number, or boolean
            if tokens[0].isnumeric() or (tokens[0][0] == '-' and tokens[0][1:].isnumeric()):
                self.push_constant(tokens[0])
            elif '.' in tokens[0]:
                self.push_constant(tokens[0], is_real=True)
            elif tokens[0] == 'TRUE':
                self.push_constant('1')
            elif tokens[0] == 'FALSE':
                self.push_constant('0')
            else:
                self.load_var(tokens[0])

    def add(self):
        self.assembly_code.append("ADD R2 R0 R1")
        self.store_result()

    def multiply(self):
        self.assembly_code.append("MUL R2 R0 R1")
        self.store_result()

    def assignment(self, var_name, value):
        self.load_constant(value)
        self.assembly_code.append(f"ST @{var_name} R2")

    def not_equal(self):
        self.assembly_code.append("NE R2 R0 R1")
        self.store_result()

    def push_constant(self, value, is_real=False):
        # Load the constant into register R2
        if is_real:
            self.assembly_code.append(f"LD R2 {value}")
        else:
            self.assembly_code.append(f"LD R2 #{value}")

    def load_var(self, var_name):
        # Load the value of the variable into register R2
        self.assembly_code.append(f"LD R2 @{var_name}")

    def load_constant(self, value):
        # Load a constant value into register R0
        self.assembly_code.append(f"LD R0 #{value}")

    def store_result(self):
        # Store the result in @print
        self.assembly_code.append("ST @print R2")

    def handle_error(self):
        # Print "ERROR" when an error occurs
        self.assembly_code.append("LD R0 #\"ERROR\"")
        self.assembly_code.append("ST @print R0")

    def generate_assembly(self, tok_filename, std_filename, asm_filename):
        # Read tokens from .tok file
        with open(tok_filename, 'r') as tok_file:
            input_lines = tok_file.read().splitlines()

        # Read expected output from .std file
        with open(std_filename, 'r') as std_file:
            expected_output = std_file.read()

        # Generate assembly code based on input tokens
        try:
            self.generate_assembly(input_lines)
        except Exception as e:
            self.handle_error()

        # Check if generated assembly code matches the expected output
        if '\n'.join(self.assembly_code) == expected_output:
            # Save the assembly code to a file
            with open(asm_filename, 'w') as asm_file:
                asm_file.writelines('\n'.join(self.assembly_code))
        else:
            print("Error: Generated assembly code does not match the expected output.")

# # Example usage
# tok_filename = "input.tok"
# std_filename = "expected_output.std"
# asm_filename = "6401xxxx.asm"  # Replace with your actual student ID

# code_generator = CodeGenerator()
# code_generator.generate_assembly(tok_filename, std_filename, asm_filename)
