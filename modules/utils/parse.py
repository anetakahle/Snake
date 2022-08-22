def tryParseInt(value):
    try:
        return int(value), True
    except ValueError:
        return value, False