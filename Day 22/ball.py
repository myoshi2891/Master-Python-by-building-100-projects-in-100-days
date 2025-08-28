
from turtle import Turtle

class Ball(Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move: int = 10
        self.y_move: int = 10
        self.move_speed: float = 0.1

    def move(self) -> None:
        new_x: float = self.xcor() + self.x_move
        new_y: float = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self) -> None:
        self.y_move *= -1

    def bounce_x(self) -> None:
        self.x_move *= -1
        self.move_speed *= 0.9

    def reset_position(self) -> None:
        self.goto(0, 0)
        self.move_speed = 0.1
        self.bounce_x()
