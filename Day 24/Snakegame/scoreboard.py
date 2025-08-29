from turtle import Turtle
from typing import Tuple
ALIGNMENT : str= "center"
FONT : Tuple[str, int, str]= ("Courier", 24, "normal")

class Scoreboard(Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.score: int = 0
        with open("data.txt", "r") as data:
            self.high_score = int(data.read())
        self.color("white")
        self.penup()
        self.goto(0, 270)
        self.hideturtle()
        self.update_score()

    def update_score(self) -> None:
        self.clear()
        self.write(
            f"Score: {self.score} High Score: {self.high_score}", align=ALIGNMENT, font=FONT
        )

    def increase_score(self) -> None:
        self.score += 1
        self.update_score()

    # def game_over(self) -> None:
    #     self.goto(0, 0)
    #     self.write(f"GAME OVER!!! Score: {self.score}", align=ALIGNMENT, font=FONT)

    def reset(self) -> None:
        if self.score > self.high_score:
            self.high_score = self.score
            with open("data.txt", "w") as data:
                data.write(str(self.high_score))
        self.score = 0
        self.update_score()
