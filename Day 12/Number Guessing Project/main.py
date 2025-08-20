import random
from random import randint
from art import logo

print(logo)
EASY = 10
HARD = 5

def set_difficulty():
    choice = input("Type 'easy' or 'hard'.: ")
    if choice == 'easy':
        return EASY
    else:
        return HARD


def check_answer(user_guess, actual_guess, turns):

    if user_guess < actual_guess:
        print(f"Your guess is too low.")
        return turns - 1
    elif user_guess > actual_guess:
        print(f"Your guess is too high.")
        return turns - 1
    else:
        return print(f"You got it! The number was {actual_guess}.")

def game():
    print("Welcome to the Number Guessing Project !\nI'm thinking of a number between 1 and 100.\nChoose a difficulty level.")
    answer = randint(1, 100)
    turns = set_difficulty()

    guess = 0
    while guess != answer:
        print(f"You have {turns} turns left.")
        guess = int(input("Make a guess: "))
        turns = check_answer(guess, answer, turns)
        if turns == 0:
            print(f"You lost! The number was {answer}.")
            return
        else:
            print("Guess again.")

game()