from cs50 import get_float


def main():
    # Ask how many cents the customer is owed
    while True:
        cents = get_float("Cents: ")
        if cents > 0:
            break

    cents = cents * 100

    # Calculate the number of quarters to give the customer
    quarters = calculate_quarters(cents)
    cents = cents - quarters * 25
    print(quarters)

    # Calculate the number of dimes to give the customer
    dimes = calculate_dimes(cents)
    cents = cents - dimes * 10
    print(dimes)

    # Calculate the number of nickels to give the customer
    nickels = calculate_nickels(cents)
    cents = cents - nickels * 5

    # Calculate the number of pennies to give the customer
    pennies = calculate_pennies(cents)
    cents = cents - pennies * 1

    # Sum coins
    coins = quarters + dimes + nickels + pennies

    # Print total number of coins to give the customer
    print(coins)


def calculate_quarters(cents):
    return int(cents / 25)


def calculate_dimes(cents):
    return int(cents / 10)


def calculate_nickels(cents):
    return int(cents / 5)


def calculate_pennies(cents):
    return int(cents / 1)


main()
