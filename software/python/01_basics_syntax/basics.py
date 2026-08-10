"""Tour of core Python syntax: variables, control flow, functions, collections."""


def main():
    # Variables & f-strings
    name = "Aarav"
    age = 21
    print(f"Hello, {name}! You are {age} years old.")

    # Control flow
    for n in range(1, 6):
        if n % 2 == 0:
            print(f"{n} is even")
        else:
            print(f"{n} is odd")

    # Functions with default args and *args/**kwargs
    print(greet("Sam"))
    print(greet("Sam", greeting="Hi"))
    print(sum_all(1, 2, 3, 4))
    describe(city="Austin", state="TX")

    # Collections & comprehensions
    squares = [x * x for x in range(10)]
    evens = {x for x in squares if x % 2 == 0}
    lookup = {x: x * x for x in range(5)}
    print("squares:", squares)
    print("even squares:", evens)
    print("lookup table:", lookup)

    # Exception handling
    for value in ["10", "abc", "3"]:
        try:
            print("parsed:", int(value))
        except ValueError:
            print(f"'{value}' is not a valid integer")

    # Basic file I/O
    write_and_read_file()


def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


def sum_all(*args):
    return sum(args)


def describe(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")


def write_and_read_file():
    path = "scratch_output.txt"
    with open(path, "w") as f:
        f.write("Line 1\nLine 2\nLine 3\n")

    with open(path) as f:
        lines = f.readlines()
    print("file contents:", [line.strip() for line in lines])

    import os
    os.remove(path)


if __name__ == "__main__":
    main()
