import time

def delay_decorator(fn):
    def wrapper_function():
        time.sleep(1)
        fn()
    return wrapper_function

@delay_decorator
def say_hello():
    print("Hello, World!")

@delay_decorator
def say_goodbye():
    print("Goodbye, World!")

def say_greeting():
    print("Greetings, World!")

say_hello()

decorated_function = delay_decorator(say_greeting)
decorated_function()
