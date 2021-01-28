def _normalize_scratch_rotation(degree):
    while degree <= -180:
        degree += 360
    
    while degree > 180:
        degree -= 360

    return degree

def _convert_scratch_to_pygame_rotation(degree):

    deg = _normalize_scratch_rotation(degree)

    if deg == 0:
        return 90
    elif deg == 90:
        return 0
    elif deg == -90:
        return 180
    elif deg == 180:
        return 270
    elif deg > 0 and deg < 90:
        return 90 - deg
    elif deg > 90 and deg < 180:
        return 360 - (deg - 90)
    elif deg < 0 and deg > -90:
        return 90 - deg
    elif deg < -90 and deg > -180:
        return 270 - (180 + deg)

def _normalize_pygame_rotation(degree):
    while degree < 0:
        degree += 360
    
    while degree >= 360:
        degree -= 360

    return degree


def _convert_pygame_to_scratch_rotation(degree):

    deg = _normalize_pygame_rotation(degree)

    if deg == 0:
        return 90
    elif deg == 90:
        return 0
    elif deg == 180:
        return -90
    elif deg == 270:
        return 180
    elif deg > 0 and deg < 90:
        return 90 - deg
    elif deg > 90 and deg < 180:
        return 90 - deg
    elif deg > 180 and deg < 270:
        return 90 - deg
    elif deg > 270 and deg < 360:
        return 90 + (360 - deg)