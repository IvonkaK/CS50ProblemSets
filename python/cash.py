from cs50 import get_float

money = 0

#user input must be correct ( < 0 )
while (money <= 0):
    money = get_float("Change owed: ")

    coins = 0
    cents = round(money * 100, 0)

#calculate correct change until there is no change
while (cents > 0):
    if (cents >= 25):
        cents -= 25
        coins += 1
    elif (cents >= 10):
        cents -= 10
        coins += 1
    elif (cents >= 5):
        cents -= 5
        coins += 1
    else:
        cents -= 1
        coins += 1

#print the number of coins
print(coins)
