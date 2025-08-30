with open("Archive/Day 23/new_file.txt") as file:
    contents = file.read()
    print(contents)

with open("Archive/Day 23/new_file.txt", "a") as file:
    file.write("\nHello, New WorldII!")

# import os

# # Check current directory
# print("Current directory:", os.getcwd())

# # Check what's in the parent directory
# print("\nContents of parent directory:")
# try:
#     for item in os.listdir("../"):
#         print(f"  {item}")
# except FileNotFoundError:
#     print("  Parent directory not found")

# # Check if Archive directory exists
# print("\nChecking for Archive directory:")
# if os.path.exists("../Archive"):
#     print("  Archive directory exists")

#     # Check contents of Archive
#     print("\nContents of Archive directory:")
#     for item in os.listdir("../Archive"):
#         print(f"  {item}")

#     # Check if Day 23 exists in Archive
#     if os.path.exists("../Archive/Day 23"):
#         print("\nDay 23 directory exists")
#         print("Contents of Day 23:")
#         for item in os.listdir("../Archive/Day 23"):
#             print(f"  {item}")
#     else:
#         print("\nDay 23 directory does not exist in Archive")
# else:
#     print("  Archive directory does not exist")

# # Try to find new_file.txt anywhere
# print("\nSearching for new_file.txt:")
# for root, dirs, files in os.walk("../"):
#     for file in files:
#         if file == "new_file.txt":
#             full_path = os.path.join(root, file)
#             print(f"  Found: {full_path}")
