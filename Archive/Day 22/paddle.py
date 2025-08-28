
from turtle import Turtle

class Paddle(Turtle):
    def __init__(self, position: tuple[float, float]) -> None:
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(5, 1)
        self.penup()
        self.goto(position)

    def go_up(self) -> None:
        new_y: float = self.ycor() + 20
        self.sety(new_y)

    def go_down(self) -> None:
        new_y: float = self.ycor() - 20
        self.sety(new_y)
