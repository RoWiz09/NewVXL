import math

def ray_step(x, y, z, xr, yr, length):
    return (
        x + math.sin(xr) * math.sin(yr) * length,
        y + math.cos(yr) * length,
        z + math.cos(xr) * math.sin(yr) * length
    )