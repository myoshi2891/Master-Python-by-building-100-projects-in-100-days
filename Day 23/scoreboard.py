from turtle import Turtle
from typing import Tuple

FONT: Tuple[str, int, str] = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.level: int = 1
        self.hideturtle()
        self.penup()
        self.goto(-280, 250)
        self.update_scoreboard()

    def update_scoreboard(self) -> None:
        self.clear()
        self.write(f"Score: {self.level}", align="left", font=FONT)

    def increase_level(self) -> None:
        self.level += 1
        self.update_scoreboard()

    def game_over(self) -> None:
        self.goto(0, 0)
        self.write("Game Over!", align="center", font=FONT)