def lettergetter(score, limit) -> str:
    if score / limit < .6:
        return 'F'
    elif score / limit < .63:
        return 'D-'
    elif score / limit < .67:
        return 'D'
    elif score / limit < .7:
        return 'D+'
    elif score / limit < .73:
        return 'C-'
    elif score / limit < .77:
        return 'C'
    elif score / limit < .8:
        return 'C+'
    elif score / limit < .83:
        return 'B-'
    elif score / limit < .87:
        return 'B'
    elif score / limit < .9:
        return 'B+'
    elif score / limit < .93:
        return 'A-'
    elif score / limit < .97:
        return 'A'
    elif score / limit < 1:
        return 'A+'
    else:
        return 'A++'
