import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the PyPassword Generator!")
nr_letters = int(input("How many letters would you like in your password?\n"))
nr_symbols = int(input(f"How many symbols would you like?\n"))
nr_numbers = int(input(f"How many numbers would you like?\n"))


letters_length = len(letters)
symbols_length = len(symbols)
numbers_length = len(numbers)

password = []

for i in range(0, nr_letters):
    password += random.choice(letters)
for i in range(0, nr_numbers):
    password += random.choice(symbols)
for i in range(0, nr_symbols):
    password += random.choice(numbers)
print(password)
random.shuffle(password)
print(password)
final_pass = ""

for char in password:
    final_pass += char

print(f"Your password is: {final_pass}")