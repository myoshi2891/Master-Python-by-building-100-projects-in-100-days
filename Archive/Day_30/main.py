# # FileNotFound

# try:
#     file = open("non_existent_file.txt")
#     a_dictionary = {"key": "value"}
#     print(a_dictionary["key"])
# except FileNotFoundError:
#     file = open("non_existent_file.txt", "w")
#     file.write("This file was created because the original file was not found.")
# except KeyError as error_message:
#     print(f"The key {error_message} does not exist.")
# else:
#     content = file.read()
#     print(content)
# finally:
#     raise Exception("This is a test exception.")
#     file.close()
#     print("Execution completed.")

height = float(input("Height: "))
weight = int(input("Weight: "))

if height > 3:
    raise ValueError("Human height should not be over 3 meters.")

bmi = weight / (height ** 2)
print(f"BMI: {bmi}")
