def isdate(s):
    for c in s:
        if c != '-' and not c.isdigit():
            return False
    return True