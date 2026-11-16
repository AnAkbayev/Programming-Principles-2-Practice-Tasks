# Practice 04 - Math and Random Operations

import math
import random

# Built-in mathematical functions
numbers = [12, -5, 8, 23, 4]

print("Numbers:", numbers)
print("Minimum:", min(numbers))
print("Maximum:", max(numbers))
print("Absolute value of -15:", abs(-15))
print("Rounded value:", round(3.14159, 2))
print("2 to the power of 5:", pow(2, 5))

# math module
print("\nMath module:")
print("Square root of 81:", math.sqrt(81))
print("Ceiling of 4.2:", math.ceil(4.2))
print("Floor of 4.8:", math.floor(4.8))
print("sin(pi / 2):", math.sin(math.pi / 2))
print("cos(0):", math.cos(0))
print("Pi:", math.pi)
print("Euler's number:", math.e)

# random module
print("\nRandom operations:")
print("Random float:", random.random())
print("Random integer:", random.randint(1, 100))

fruits = ["apple", "banana", "orange", "kiwi"]
print("Random fruit:", random.choice(fruits))

cards = ["Ace", "King", "Queen", "Jack", "10"]
random.shuffle(cards)
print("Shuffled cards:", cards)

# Circle example
radius = 5
area = math.pi * radius ** 2
circumference = 2 * math.pi * radius

print("\nCircle example:")
print("Radius:", radius)
print("Area:", round(area, 2))
print("Circumference:", round(circumference, 2))
