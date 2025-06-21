def generate_code(prompt):
    return f"# Kaelira imagined this code based on: {prompt}\nprint('Hello from Kaelira!')"

def save_code(code, filename="generated_code.py"):
    with open(filename, "w") as f:
        f.write(code)
