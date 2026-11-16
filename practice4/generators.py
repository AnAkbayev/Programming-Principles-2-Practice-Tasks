# Practice 04 - Iterators and Generators

# 1. Using iter() and next()
numbers = [10, 20, 30, 40, 50]
iterator = iter(numbers)

print("Iterator:")
print(next(iterator))
print(next(iterator))
print(next(iterator))

# 2. Loop through an iterator
print("\nLoop through iterator:")
for number in iter(numbers):
    print(number)

# 3. Create a custom iterator
class CountUp:
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.end:
            value = self.current
            self.current += 1
            return value
        raise StopIteration

print("\nCustom iterator:")
for number in CountUp(1, 5):
    print(number)

# 4. Generator function using yield
def square_numbers(limit):
    for number in range(1, limit + 1):
        yield number ** 2

print("\nGenerator function:")
for square in square_numbers(5):
    print(square)

# 5. Generator expression
squares = (number ** 2 for number in range(1, 6))

print("\nGenerator expression:")
for square in squares:
    print(square)
