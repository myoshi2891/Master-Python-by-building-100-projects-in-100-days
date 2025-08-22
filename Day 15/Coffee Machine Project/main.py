MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

change = 0
money = 0
users_sum = 0
is_Available = True
#TODO: 1. Print report of all coffee machine resources
users_order = input("What would you like? (espresso/latte/cappuccino): ")
if users_order == "report":
    print(f"Water: {resources["water"]}ml\nMilk: {resources["milk"]}ml\nCoffee: {resources["coffee"]}ml\nMoney: ${money}")

def is_enough_resources(order):
    global  is_Available
    for resource in resources:
        if order == "report":
            is_Available = False
        elif resources[resource] <= MENU[order]["ingredients"][resource]:
            print(f"Sorry there is not enough {resource}.")
            is_Available = False

while is_Available:
    def calculate_cost(user):
        cost = 0
        if user == "espresso":
            cost = users_sum - MENU[user]["cost"]
        elif user == "latte":
            cost = users_sum - MENU[user]["cost"]
        elif user == "cappuccino":
            cost = users_sum - MENU[user]["cost"]

        if cost >= 0:
            print(f"Here is ${round(cost, 2)} in change.")
            print(f"Here is your {user} ☕️. Enjoy!")
        else:
            print("Sorry that's not enough money. Money refunded.")
            return False

    def calculate_total(coin, numOfCoins, sum):
        if coin == "quarters":
            sum += numOfCoins * 0.25
        elif coin == "dimes":
            sum += numOfCoins * 0.10
        elif coin == "nickles":
            sum += numOfCoins * 0.05
        elif coin == "pennies":
            sum += numOfCoins * 0.01
        return sum

    def after_purchase(user):
        global money
        for resource in resources:
            resources[resource] -= MENU[user]["ingredients"][resource]
            money = MENU[user]["cost"]

    print("Please insert coins.")

    coin_type = ["quarters", "dimes", "nickles", "pennies"]

    for coin in coin_type:
        numOfCoins = int(input(f"how many {coin}?: "))
        users_sum += calculate_total(coin, numOfCoins, money)

    calculate_cost(users_order)
    after_purchase(users_order)


