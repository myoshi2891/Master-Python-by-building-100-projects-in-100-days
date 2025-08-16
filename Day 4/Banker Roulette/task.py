import random

friends = ["Alice", "Bob", "Charlie", "David", "Emanuel"]

who_is_gonna_pay1 = friends[random.randint(0, len(friends)-1)]
who_is_gonna_pay2 = random.choice(friends)

print(who_is_gonna_pay1, who_is_gonna_pay2)