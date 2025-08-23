# Local Scope

# def drink_potion():
#     potion_strength = 2
#     print(potion_strength)

# drink_potion()
# print(potion_strength)

#Global Scope
player_health = 10

# def game:
#     def drink_potion():
#         potion_strength = 2
#         print(player_health)
#
#     drink_potion()
#
# print(player_health)

game_level = 3
enemies = ["Skeleton", "Zombie", "Alien"]

def create_enemy():
    new_enemy = ""
    if game_level < 5:
        new_enemy = enemies[0]

    print(new_enemy)

create_enemy()