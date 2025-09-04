def add(*arg: int) -> int:
    print(arg[1])
    result = 0
    for num in arg:
        result += num
    return result

print(add(1, 2, 3, 4, 5))  # Output: 15


def calculate_sum(n: int, **kwargs: int):
    print(kwargs)  # Output: {'a': 1, 'b': 2, 'c': 3}
    # result = 0
    # for _, value in kwargs.items():
    #     result += value
    # return result
    n += kwargs["add"]
    n *= kwargs["multiply"]
    print(n)  # Output: 6

print(calculate_sum(2, add=1, multiply=2))  # Output: 6

class Car:
    def __init__(self, **kw: str):
        self.make = kw.get("make")  # Output: Toyota
        self.model = kw.get("model")  # Output: Camry
        self.year = kw.get("year")  # Output: 2020

        print("Car object created.")

my_car = Car(make="Toyota")
print(my_car.model)  # Output: Toyota