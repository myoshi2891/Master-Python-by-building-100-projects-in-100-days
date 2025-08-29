from turtle import Turtle
from typing import List, Tuple

STARTING_POSITIONS: List[Tuple[int, int]] = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE: int = 20
UP: int = 90
DOWN: int = 270
LEFT: int = 180
RIGHT: int = 0


class Snake:
    def __init__(self) -> None:
        self.segments: List[Turtle] = []
        self.create_snake()
        self.head: Turtle = self.segments[0]

    def create_snake(self) -> None:
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position: Tuple[float, float]) -> None:
        new_segment: Turtle = Turtle("square")
        new_segment.color("white")
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)

    def reset(self) -> None:
        for seg in self.segments:
            seg.goto(1000, 1000)  # Place the segment off-screen
        self.segments.clear()
        self.create_snake()
        self.head: Turtle = self.segments[0]

    def extend(self) -> None:
        """
        Extends the snake by adding a new segment at the position of the last segment.

        This method is typically called when the snake eats food and needs to grow longer.
        The new segment is added at the same position as the tail (last segment), so it will
        become visible when the snake moves forward.

        Returns:
            None
        """
        self.add_segment(self.segments[-1].position())

    def move(self) -> None:
        """
        Moves the snake forward by one step in its current direction.

        This method implements the snake's movement by moving each segment to the position
        of the segment in front of it, starting from the tail and working towards the head.
        The head then moves forward by MOVE_DISTANCE pixels in its current heading direction.
        This creates the characteristic snake-like movement where the body follows the head.

        Returns:
            None
        """
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x: float = self.segments[seg_num - 1].xcor()
            new_y: float = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)

    def up(self) -> None:
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self) -> None:
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self) -> None:
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self) -> None:
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)
