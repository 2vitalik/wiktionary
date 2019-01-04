

def get_plural(number, case1, case2, case5):
    if 11 <= number % 100 <= 19:
        return case5
    if number % 10 == 1:
        return case1
    if 2 <= number % 10 <= 4:
        return case2
    return case5
