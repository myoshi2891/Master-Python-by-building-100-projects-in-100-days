import random

from art import logo, vs
from game_data import data

score = 0
print(logo)

compare_A = random.randint(0,49)
against_B = random.randint(0,49)

def play():
    global score
    global compare_A
    global against_B
    game_over = False
    while not game_over:
        print(f"Compare A: {data[compare_A]["name"]}, a {data[compare_A]["description"]}, from {data[compare_A]["country"]}.")
        print(vs)
        print(f"Against B:  {data[against_B]["name"]}, a {data[against_B]["description"]}, from {data[against_B]["country"]}.")
        choice = input("Who has more followers? Type 'A' or 'B': ")
        if choice == 'A':
            if data[compare_A]["follower_count"] > data[against_B]["follower_count"]:
                score += 1
                print(f"You're right! Current score {score}")
                against_B = random.randint(0, 49)
            else:
                print(f"Sorry, that's wrong. Final score: {score}.")
                game_over = True
        else:
            if data[compare_A]["follower_count"] < data[against_B]["follower_count"]:
                score += 1
                print(f"You're right! Current score {score}")
                compare_A = against_B
                against_B = random.randint(0, 49)
            else:
                print(f"Sorry, that's wrong. Final score: {score}.")
                game_over = True
play()







# print(logo)
