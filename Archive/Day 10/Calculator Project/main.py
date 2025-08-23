from art import logo

def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

operations = {"+": add, "-": subtract, "*": multiply, "/": divide}

# print(operations["*"](8, 8))
def calculator():
    print(logo)
    should_accumulate = True
    num1 = float(input("What's the first number: "))

    while should_accumulate:

        for symbol in operations:
            print(symbol)

        operations_symbol = input("Pick an operation: ")
        num2 = float(input("What's the next number: "))
        answer = operations[operations_symbol](num1, num2)
        print(f"{num1} {operations_symbol} {num2} = {answer}")

        choice = input(f"Type 'y' to continue with {answer} or type 'n' to cancel: ")

        if choice == "y":
            num1 = answer
        else:
            should_accumulate = False
            print("\n" * 20)
            calculator()
calculator()