total = 0


def fuelformass(mass):
    fuel = (int(mass) // 3) - 2
    if fuel > 0:
        return fuel + fuelformass(fuel)
    return 0


try:
    while mass := input():
        total += fuelformass(int(mass))
except EOFError:
    pass

print(total)
