#Display art
from art import logo,vs
from game_data import data
import random
print(logo)
score = 0
account_b = random.choice(data)
def format_data(account):
    # Format the account data into printable format
    account_name = account['name']
    account_desc = account['description']
    account_country = account['country']
    return f"{account_name}, a {account_desc}, from {account_country}"

def check_answer(user_guess, a_followers, b_followers):
    """Take a user's guess and the follower counts and returns i they got it right."""
    if a_followers > b_followers:
        return user_guess == "a"
    else:
        return user_guess == "b"
game_should_continue = True

while game_should_continue:
    #Generate a random account from the game data
    account_a = account_b
    account_b = random.choice(data)
    if account_a == account_b:
        account_b = random.choice(data)

    print(f"Compare A: {format_data(account_a)}")
    print(vs)
    print(f"Against B: {format_data(account_b)}")

    #Ask user for a guess.
    guess = input("Who has more followers? Type 'A' or 'B': ").lower()

    # Clear the screen
    print("\n" * 20)
    print(logo)

    #Check if user is correct
    ## Get follower count of each account
    a_follower_count = account_a['follower_count']
    b_follower_count = account_b['follower_count']

    is_correct = check_answer(guess, a_follower_count, b_follower_count)

    # Give user feedback on their guess
    if is_correct:
        score += 1
        print(f"Correct! You got it right. Current score {score}.")
    else:
        print(f"Sorry! You got it wrong. Final score: {score}.")
        game_should_continue = False

    # score keeping

    # Make the game repeatable

    #Making account at position B become the next account at position A.