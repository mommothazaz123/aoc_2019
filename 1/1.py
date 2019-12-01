total = 0

try:
    while mass := input():
        fuel = (int(mass) // 3) - 2
        total += fuel
except EOFError:
    pass

print(total)
