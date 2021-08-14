import bpy

def hsv2rgb(h, s, v):
    c = v * s
    h2 = h * 360 / 60
    x = c * (1.0 - abs(h2 % 2 - 1))
    r = v - c
    g = v - c
    b = v - c
    h2_int = h * 360 // 60
    if h2_int == 0:
        return r + c, g + x, b
    elif h2_int == 1:
        return r + x, g + c, b
    elif h2_int == 2:
        return r, g + c, b + x
    elif h2_int == 3:
        return r, g + x, b + c
    elif h2_int == 4:
        return r + x, g, b + c
    elif h2_int == 5:
        return r + c, g, b + x
    elif h2_int == 6:
        return r + c, g + x, b
