def sjekk_float(x):
    x.replace(',', '.')
    try:
        float(x)
        return True
    except ValueError:
        return False