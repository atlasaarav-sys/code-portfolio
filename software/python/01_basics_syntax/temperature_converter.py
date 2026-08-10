"""Small function-based exercise: temperature conversion with basic CLI."""


def celsius_to_fahrenheit(c: float) -> float:
    return c * 9 / 5 + 32


def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32) * 5 / 9


def main():
    print("Temperature Converter")
    print("1) Celsius -> Fahrenheit")
    print("2) Fahrenheit -> Celsius")

    choice = input("Choose 1 or 2: ").strip()
    value = float(input("Enter temperature: ").strip())

    if choice == "1":
        print(f"{value}C = {celsius_to_fahrenheit(value):.2f}F")
    elif choice == "2":
        print(f"{value}F = {fahrenheit_to_celsius(value):.2f}C")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
