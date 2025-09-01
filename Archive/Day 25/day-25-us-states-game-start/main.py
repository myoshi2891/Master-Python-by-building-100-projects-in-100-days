# import turtle
# import pandas as pd
# from typing import List

# screen = turtle.Screen()
# screen.title("U.S. States Game")

# image = "blank_states_img.gif"
# screen.addshape(image)
# turtle.shape(image)

# # def get_mouse_click_coord(x: float, y:float) -> None:
# #     print(f"Mouse clicked at coordinates: ({x}, {y})")

# # turtle.onscreenclick(get_mouse_click_coord)
# # turtle.mainloop()

# data = pd.read_csv("50_states.csv")  # type: ignore
# all_states = data.state.to_list()
# guessed_states: List[str] = []

# while len(guessed_states) < 50:
#     answer_state = screen.textinput(title=f"{len(guessed_states)}/50 States Correct!", prompt="What's another state's name?")
#     # Check if user cancelled the dialog
#     if answer_state is None:
#         break

#     if answer_state.lower() == "exit":
#         missing_states = [state for state in all_states if state not in guessed_states]
#         new_data = pd.DataFrame(missing_states)
#         new_data.to_csv("missing_states.csv")
#         break

#     answer_state = answer_state.title()

#     # TODO: Add logic to check if the user's guess is correct and update the data accordingly
#     # Check if the user's guess is correct and not already guessed
#     if answer_state in all_states and answer_state not in guessed_states:
#         # Add the correct guess to the list
#         guessed_states.append(answer_state)
#         t = turtle.Turtle()
#         t.hideturtle()
#         t.penup()
#         state_data = data[data.state == answer_state]
#         t.goto(state_data.x.item(), state_data.y.item())  # type: ignore
#         t.write(answer_state)  # type: ignore
#     elif answer_state in guessed_states:
#         # Optional: Provide feedback for already guessed states
#         print(f"You already guessed {answer_state}!")

#     # If the user's guess is incorrect, do nothing
# # Show completion message
# if len(guessed_states) == 50:
#     completion_turtle = turtle.Turtle()
#     completion_turtle.hideturtle()
#     completion_turtle.penup()
#     completion_turtle.goto(0, 0)
#     completion_turtle.color("green")
#     completion_turtle.write(
#         "Congratulations! You got all 50 states!",
#         align="center",
#         font=("Arial", 16, "bold"),
#     )

# screen.exitonclick()

import turtle
import pandas as pd
from typing import List, Optional

# Constants
FONT_SIZE = 8
COMPLETION_FONT_SIZE = 16
TEXT_COLOR = "black"
COMPLETION_COLOR = "green"
TOTAL_STATES = 50


def setup_screen() -> turtle.Screen:
    """Set up the game screen with the map image."""
    screen = turtle.Screen()
    screen.title("U.S. States Game")

    image = "blank_states_img.gif"
    screen.addshape(image)
    turtle.shape(image)

    return screen


def load_states_data() -> tuple[pd.DataFrame, List[str]]:
    """Load states data from CSV file."""
    data = pd.read_csv("50_states.csv")
    all_states = data.state.to_list()
    return data, all_states


def get_user_input(guessed_count: int) -> Optional[str]:
    """Get user input for state guess."""
    return turtle.textinput(
        title=f"{guessed_count}/{TOTAL_STATES} States Correct!",
        prompt="What's another state's name?",
    )


def create_text_turtle() -> turtle.Turtle:
    """Create a turtle for writing text on screen."""
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    t.color(TEXT_COLOR)
    return t


def display_state_on_map(data: pd.DataFrame, state_name: str) -> None:
    """Display the correctly guessed state name on the map."""
    t = create_text_turtle()
    state_data = data[data.state == state_name]

    if not state_data.empty:
        x_coord: float = float(state_data.x.iloc[0])
        y_coord: float = float(state_data.y.iloc[0])
        t.goto(x_coord, y_coord)
        t.write(state_name, align="center", font=("Arial", FONT_SIZE, "normal"))


def save_missing_states(all_states: List[str], guessed_states: List[str]) -> None:
    """Save the list of missing states to a CSV file."""
    missing_states = [state for state in all_states if state not in guessed_states]
    new_data = pd.DataFrame({"Missing States": missing_states})
    new_data.to_csv("missing_states.csv", index=False)


def show_completion_message() -> None:
    """Display completion message when all states are guessed."""
    completion_turtle = turtle.Turtle()
    completion_turtle.hideturtle()
    completion_turtle.penup()
    completion_turtle.goto(0, 0)
    completion_turtle.color(COMPLETION_COLOR)
    completion_turtle.write(
        "Congratulations! You got all 50 states!",
        align="center",
        font=("Arial", COMPLETION_FONT_SIZE, "bold"),
    )


def main() -> None:
    """Main game function."""
    screen = setup_screen()
    data, all_states = load_states_data()
    guessed_states: List[str] = []

    # Convert to set for O(1) lookup performance
    all_states_set = set(all_states)
    guessed_states_set: set[str] = set()

    while len(guessed_states) < TOTAL_STATES:
        answer_state = get_user_input(len(guessed_states))

        # Check if user cancelled the dialog
        if answer_state is None:
            break

        # Handle exit command
        if answer_state.lower() == "exit":
            save_missing_states(all_states, guessed_states)
            break

        # Normalize the input
        answer_state = answer_state.title()

        # Check if the guess is correct and not already guessed
        if answer_state in all_states_set and answer_state not in guessed_states_set:
            guessed_states.append(answer_state)
            guessed_states_set.add(answer_state)
            display_state_on_map(data, answer_state)
        elif answer_state in guessed_states_set:
            print(f"You already guessed {answer_state}!")
        else:
            print(f"'{answer_state}' is not a valid state name. Try again!")

    # Show completion message if all states were guessed
    if len(guessed_states) == TOTAL_STATES:
        show_completion_message()

    screen.exitonclick()


if __name__ == "__main__":
    main()
