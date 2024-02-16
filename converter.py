from math import sin, log, pi, tan

e = 0.0818191908426
Z = 32


def lonlat_to_xy(z, long, lat):
    b = pi * lat / 180
    phi = (1 - e * sin(b)) / (1 + e * sin(b))
    te = tan(pi / 4 + b / 2) * phi ** (e / 2)
    p = 2 ** (z + 8) / 2

    x = p * (1 + long / 180)
    y = p * (1 - log(te) / pi)

    return x, y


def xy_to_lonlat(z, x, y):
    bl, br = -180, 180
    for i in range(Z + z):
        m = (bl + br) / 2
        mx, _ = lonlat_to_xy(z, m, 0)

        if mx <= x:
            bl = m
        else:
            br = m
    long = bl

    bl, br = -85, 85
    for i in range(Z + z):
        m = (bl + br) / 2
        _, my = lonlat_to_xy(z, 0, m)

        if my >= y:
            bl = m
        else:
            br = m
    lat = br

    return long, lat
