def run():
    width = int(input("Width: "))
    height = int(input("Height: "))
    size = width * height
    pic = input("Picture: ")

    layers = [pic[i:i + size] for i in range(0, len(pic), size)]

    least_0 = sorted(layers, key=lambda lay: lay.count('0'))[0]
    print(least_0.count('1') * least_0.count('2'))

    out = ""
    for index in range(size):
        out += next(l[index] for l in layers if l[index] != '2')
    strout = '\n'.join([out[i:i + width] for i in range(0, len(out), width)])
    print(strout.replace('0', ' '))


if __name__ == '__main__':
    run()
