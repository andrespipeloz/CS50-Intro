import cs50

while True:
    height = cs50.get_int("Height: ")
    if height > 0 and height < 9:
        break

for i in range(0, height, 1):
    for e in range(0, height - i - 1):
        print(" ", end="")
    for h in range(0, i + 1):
        print("#", end="")
    for m in range(0, 2):
        print(" ", end="")
    for ha in range(0, i + 1):
        print("#", end="")
    print("\n", end="")
