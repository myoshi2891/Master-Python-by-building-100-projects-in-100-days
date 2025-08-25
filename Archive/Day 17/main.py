class User:
    def __init__(self, user_id: str, username: str, followers: int = 0):
        self.id: str = user_id
        self.username: str = username
        self.followers: int = followers
        self.following: int = 0
        # print("User object created.")
    def follow(self, user: 'User') -> None:
        user.followers += 1
        self.following += 1


user_1 = User("001","Joel Doe")
user_2 = User("002","Jack Doe")
# user_1.id = "001"
# user_1.username = "John Doe"
user_1.follow(user_2)
print(user_1.followers)  
print(user_1.following) 
print(user_2.followers)  
print(user_2.following) 

# user_2 = User("","")
# user_2.id = "002"
# user_2.username = "Jane Doe"

# print(user_2.username)  # Output: 001

# def function():
#     pass

class Car:
    def __init__(self, make: str, model: str, year: int):
        self.make: str = make
        self.model: str = model
        self.year: int = year

