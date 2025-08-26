import random
from turtle import Turtle, Screen
from typing import Tuple

# import heroes  # type: ignore
# import turtle as t
# from turtle import *

tim = Turtle()
screen = Screen()
screen.colormode(255)

def random_color() -> Tuple[int, int, int]: 
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color = (r, g, b)
    return color

# tom = t
tim.shape("turtle")
tim.color("coral")

colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown"]
# directions = [0, 90, 180, 270]
# tim.pensize(15)
tim.speed("fastest")

def draw_spirograph(size_of_gap: int) -> None:
    for _ in range(int(360 / size_of_gap)):
        tim.color(random_color())
        tim.circle(100)
        tim.setheading(tim.heading() + size_of_gap)

draw_spirograph(3)
# for _ in range(200):
#     tim.color(random_color())
#     tim.forward(30)
#     tim.setheading(random.choice(directions))


# def draw_shape(num_sides: int) -> None:
#     # Draw a square
#     for _ in range(num_sides):
#         angle = 360 / num_sides
#         tim.forward(100)
#         tim.right(angle)

# for shape_side_n in range(3, 11):
#     tim.color(random.choice(colors))
#     draw_shape(shape_side_n)


screen.exitonclick()


# print(heroes.gen())  # type: ignore
