# import pandas as pd

# # from typing import List
# # with open("weather_data.csv") as data_file:
# #     data = data_file.readlines()
# #     print(data)

# # import csv
# # with open("weather_data.csv") as data_file:
# #     data = csv.reader(data_file)
# #     temperatures: List[int] = []

# #     for row in data:
# #         if row[1] != "temp":
# #             temperatures.append(int(row[1]))
# #     print(temperatures)

# data: pd.DataFrame = pd.read_csv("weather_data.csv")  # type: ignore
# # print(type(data))
# # print(type(data["temp"]))

# data_dict = data.to_dict()  # type: ignore
# # print(data_dict)

# temp_list = data["temp"].tolist()  # type: ignore
# # print(temp_list)

# # average_temp = sum(temp_list) / len(temp_list)
# # print(f"The average temperature is {average_temp:.2f}°C.")

# # print(data["temp"].mean())
# # print(data["temp"].max())

# # Get Data in Columns
# # print(data["condition"])
# # print(data.condition)

# # Get Data in Rows
# # monday = data[data.day == "Monday"]
# # print(monday)

# # print(data[data.temp == data["temp"].max()])
# max_temp_row: pd.DataFrame = data[data.temp == data["temp"].max()]  # type: ignore
# # print(max_temp_row)  # type: ignore

# monday = data[data.day == "Monday"]
# # print(monday.condition)

# monday_temp = monday.temp[0]
# monday_temp_F = monday_temp * 9 / 5 + 32
# # print(f"On Monday, it was {monday_temp:.2f}°C, which is {monday_temp_F:.2f}°F.")

# # Create a dataframe from scratch
# data_dict = {  # type: ignore
#     "student_name": ["Alice", "Bob", "Charlie"],
#     "grade": [85, 92, 78],
# }

# data = pd.DataFrame(data_dict)
# data.to_csv("new_data.csv", index=False)

import pandas as pd

data = pd.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")  # type: ignore
gray_squirrel_count = len(data[data["Primary Fur Color"] == "Gray"])
red_squirrel_count = len(data[data["Primary Fur Color"] == "Cinnamon"])
black_squirrel_count = len(data[data["Primary Fur Color"] == "Black"])
print(gray_squirrel_count)
print(red_squirrel_count)
print(black_squirrel_count)

data = {
    "Fur Color": ["Gray", "Cinnamon", "Black"],
    "Count": [gray_squirrel_count, red_squirrel_count, black_squirrel_count],
}

fur_color_data = pd.DataFrame(data)
fur_color_data.to_csv("squirrel_fur_color_data.csv")