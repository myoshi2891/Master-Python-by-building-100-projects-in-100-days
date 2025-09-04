# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# new_list = [n + 1 for n in numbers]
# print(new_list)

# name = "John"
# letters = [letter for letter in name]
# print(letters)

# range_list = [num * 2 for num in list(range(1, 11))]
# print(range_list)

# names = ["John", "Alice", "Bob", "Charlie", "David"]
# filtered_names = [name.upper() for name in names if len(name) > 4]
# print(filtered_names)
# import random

# names = ["John", "Alice", "Bob", "Charlie", "David", "Alex"]
# student_grades = {name: random.randint(30, 100) for name in names}
# passed_students = {name: grade for name, grade in student_grades.items() if grade >= 80}
# print(student_grades)
# print(passed_students)
import pandas

from typing import List, Dict, Union

student_dict: Dict[str, List[Union[str, int]]] = {
    "student": ["John", "Alice", "Bob", "Charlie", "David"],
    "grade": [85, 92, 78, 95, 88]
}

student_data_frame = pandas.DataFrame(student_dict)
# for key, value in student_data_frame.items():
#     print(f"{key}: {value}")

# for (index, row) in student_data_frame.iterrows():
#     print(row.student)
#     print(f"Student: {row['student']}, Grade: {row['grade']}")