""" collection of utils """


def calculate_decimal_point(value: float) -> int:
    """ spit the number passed as a string
        get decimal points and calculate length
        return 0 if no decimal is available
        or length of the decimal part otherwise
    """
    dec_length = 0
    # split by a decimal point
    try:
        decimal_points = str(value).split('.')[1]
        dec_length = len(decimal_points)
    except Exception as ex:
        print(f'Was not able to get a decimal value from {value}\
              with the following error {ex}')

    return dec_length


if __name__ == "__main__":
    print('utils for handling numbers ')
    print(f'example calculate_decimal_point(25.62) -> \
          {calculate_decimal_point(25.62)}')
