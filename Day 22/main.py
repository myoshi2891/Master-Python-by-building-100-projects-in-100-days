
from time import sleep
from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard

screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Pong Game")
screen.tracer(0)

r_paddle: Paddle = Paddle((350, 0))
l_paddle: Paddle = Paddle((-350, 0))
ball: Ball = Ball()
scoreboard: Scoreboard = Scoreboard()

screen.listen()
screen.onkey(r_paddle.go_up, "Up")
screen.onkey(r_paddle.go_down, "Down")
screen.onkey(l_paddle.go_up, "w")
screen.onkey(l_paddle.go_down, "s")

game_is_on: bool = True
while game_is_on:
    sleep(ball.move_speed)
    screen.update()
    ball.move()

    # detect collision with top and bottom walls
    if ball.ycor() > 280 or ball.ycor() < -280:
        # need to reverse y direction
        ball.bounce_y()

    # detect collision with paddles
    if (
        (ball.distance(r_paddle) < 50 and ball.xcor() > 320)
        or (ball.distance(l_paddle) < 50 and ball.xcor() < -320)
    ):
        # need to reverse x direction
        ball.bounce_x()

    # detect collision with right paddle
    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.l_point()

    # detect collision with left paddle
    if ball.xcor() < -380:
        ball.reset_position()
        scoreboard.r_point()

screen.exitonclick()
