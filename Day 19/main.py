
from turtle import Turtle, Screen
from typing import List, Optional
import random

screen = Screen()
screen.setup(width=500, height=400)

user_input: Optional[str] = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter the color: ")
user_bet: str = (user_input or "").lower()
print(f"You chose {user_bet}.")

colors: List[str] = ["red", "orange", "green", "blue", "indigo", "violet"]
y_positions: List[int] = [-70, -40, -10, 20, 50, 80]
all_turtles: List[Turtle] = []

for turtle_index in range(0, 6):
    new_turtle: Turtle = Turtle(shape="turtle")
    new_turtle.color(colors[turtle_index])
    new_turtle.penup()
    new_turtle.goto(x=-230, y=y_positions[turtle_index])  # Fixed: removed negative sign
    all_turtles.append(new_turtle)

is_race_on: bool = bool(user_bet)

while is_race_on:
    for turtle in all_turtles:
        if turtle.xcor() > 230:
            is_race_on = False
            winning_color: str = turtle.pencolor()
            if winning_color == user_bet:
                print(f"You've won! The {winning_color} turtle is the winner!")
            else:
                print(f"You've lost! The {winning_color} turtle is the winner!")
            break  # Exit the loop once we have a winner
        
        rand_distance: int = random.randint(0, 10)
        turtle.forward(rand_distance)

screen.exitonclick()
