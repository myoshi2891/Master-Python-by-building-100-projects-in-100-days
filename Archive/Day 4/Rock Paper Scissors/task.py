import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

user_choice = int(input("What do you choose? Type 0 for 'rock', 1 for 'paper' or 2 for 'scissors'.\n"))

listOfChoice: list[str] = [rock, paper, scissors]
if user_choice >= 0 and user_choice <= 2:
    print(listOfChoice[user_choice])
computer_choice = random.randint(0, 2)

if user_choice == computer_choice:
    print("Computer chose " + listOfChoice[computer_choice])
    print("It's a tie!")
elif user_choice == 0:
    if computer_choice == 1:
        print("Computer chose " + listOfChoice[computer_choice])
        print("You lose!")
    elif computer_choice == 2:
        print("Computer chose " + listOfChoice[computer_choice])
        print("You win!")
elif user_choice == 1:
    if computer_choice == 0:
        print("Computer chose " + listOfChoice[computer_choice])
        print("You win!")
    elif computer_choice == 2:
        print("Computer chose " + listOfChoice[computer_choice])
        print("You lose!")
elif user_choice == 2:
    if computer_choice == 0:
        print("Computer chose " + listOfChoice[computer_choice])
        print("You win!")
    elif computer_choice == 1:
        print("Computer chose " + listOfChoice[computer_choice])
        print("You lose!")



