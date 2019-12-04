# in: 152085-670283


def run():
    small, big = map(int, input().split('-'))

    valid = 0

    for i in range(small, big + 1):
        i_ = str(i)
        if not len(i_) == 6:
            continue

        if not any(char * 2 in i_ for char in i_):
            continue

        if not all(int(i_[j]) >= int(i_[j - 1]) for j in range(1, 6)):
            continue

        valid += 1

    print(valid)


if __name__ == '__main__':
    run()
