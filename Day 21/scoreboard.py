from turtle import Turtle
from typing import Tuple
ALIGNMENT : str= "center"
FONT : Tuple[str, int, str]= ("Courier", 24, "normal")

class Scoreboard(Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.score: int = 0
        self.color("white")
        self.penup()
        self.goto(0, 270)
        self.hideturtle()
        self.update_score()

    def update_score(self) -> None:
        self.write(
            f"Score: {self.score}", align=ALIGNMENT, font=FONT
        )

    def increase_score(self) -> None:
        self.score += 1
        self.clear()
        self.update_score()

    def game_over(self) -> None:
        self.goto(0, 0)
        self.write(f"GAME OVER!!! Score: {self.score}", align=ALIGNMENT, font=FONT)

