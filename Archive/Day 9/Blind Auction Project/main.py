from art import logo

all_bids = {}
# TODO-4: Compare bids in dictionary
def find_highest_bidder(all_bids):
    highest_bid = 0
    for name, bid in all_bids.items():
        if bid > highest_bid:
            highest_bid = bid
            winner = name

    print(f"The winner is {winner} with bid {highest_bid}")

continue_bidding = True
while continue_bidding:
    print(logo)
    # TODO-1: Ask the user for input
    name = input("What is your name?:  ")
    bid = int(input("What is your bid?: $"))

    # TODO-2: Save data into dictionary {name: price}

    all_bids[name] = bid

    print(all_bids)


    yes_or_no = input("Are there any bidder? Type 'yes' or 'no': ")
    if yes_or_no == "no":
        continue_bidding = False
        find_highest_bidder(all_bids)
    else:
        print("\n" * 100)

