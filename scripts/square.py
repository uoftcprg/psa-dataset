def square(value):
    return value ** 2


def main():
    status = True

    while status:
        try:
            s = input()
        except EOFError:
            status = False
        else:
            print(
                '\t'.join(
                    map('{:.6f}'.format, map(square, map(float, s.split()))),
                ),
            )


if __name__ == '__main__':
    main()
