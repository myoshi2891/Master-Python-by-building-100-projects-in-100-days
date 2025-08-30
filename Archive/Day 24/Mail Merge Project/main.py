import os
from typing import List

# TODO: Create a letter using starting_letter.txt
# for each name in invited_names.txt
# Replace the [name] placeholder with the actual name.
# Save the letters in the folder "ReadyToSend".

PLACEHOLDER: str = "[name]"

# Ensure output directory exists
os.makedirs("Output/ReadyToSend", exist_ok=True)

try:
    with open("Input/Names/invited_names.txt", "r", encoding="utf-8") as names_file:
        names: List[str] = names_file.readlines()

    with open("Input/Letters/starting_letter.txt", "r", encoding="utf-8") as letter_file:
        letter_contents: str = letter_file.read()
        
        for name in names:
            stripped_name: str = name.strip()
            if stripped_name:  # Skip empty lines
                new_letter: str = letter_contents.replace(PLACEHOLDER, stripped_name)
                output_filename: str = f"Output/ReadyToSend/letter_for_{stripped_name}.txt"
                
                with open(output_filename, "w", encoding="utf-8") as new_letter_file:
                    new_letter_file.write(new_letter)
                    
        print("Mail merge completed successfully!")
        
except FileNotFoundError as e:
    print(f"Error: Required file not found - {e}")
except Exception as e:
    print(f"An error occurred: {e}")
