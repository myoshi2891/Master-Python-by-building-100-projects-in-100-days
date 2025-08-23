capital = {
    "France": "Paris",
    "Germany": "Berlin"
}

# travel_log = {
#     "France" : ["Paris", "Lille", "Doijon"]
# }

# print(travel_log["France"][1])

travel_log = {
    "France" : {
        "num_times_visited" : 1,
        "cities_visited" :  ["Paris", "Lille", "Doijon"]
    }
}

print(travel_log["France"]["cities_visited"][2])