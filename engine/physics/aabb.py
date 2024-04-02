def check_aabb(pos1, size1, pos2, size2):
    AminX = pos1[0] - size1[0] / 2
    AminY = pos1[1] - size1[1] / 2
    AminZ = pos1[2] - size1[2] / 2
    AmaxX = pos1[0] + size1[0] / 2
    AmaxY = pos1[1] + size1[1] / 2
    AmaxZ = pos1[2] + size1[2] / 2

    BminX = pos1[0] - size1[0] / 2
    BminY = pos1[1] - size1[1] / 2
    BminZ = pos1[2] - size1[2] / 2
    BmaxX = pos1[0] + size1[0] / 2
    BmaxY = pos1[1] + size1[1] / 2
    BmaxZ = pos1[2] + size1[2] / 2

    return all((AminX <= BmaxX, AmaxX >= BminX, AminY <= BmaxY, AmaxY >= BminY, AminZ <= BmaxZ, AmaxZ >= BminZ))

def correct_aabb(d_pos, d_size, s_pos, s_size):
    # correcting a collision between two aabbs, one static and one dynamic ( to move )

    AminX = d_pos[0] - d_size[0] / 2
    AminY = d_pos[1] - d_size[1] / 2
    AminZ = d_pos[2] - d_size[2] / 2
    AmaxX = d_pos[0] + d_size[0] / 2
    AmaxY = d_pos[1] + d_size[1] / 2
    AmaxZ = d_pos[2] + d_size[2] / 2

    BminX = s_pos[0] - s_size[0] / 2
    BminY = s_pos[1] - s_size[1] / 2
    BminZ = s_pos[2] - s_size[2] / 2
    BmaxX = s_pos[0] + s_size[0] / 2
    BmaxY = s_pos[1] + s_size[1] / 2
    BmaxZ = s_pos[2] + s_size[2] / 2

    if not all((AminX <= BmaxX, AmaxX >= BminX, AminY <= BmaxY, AmaxY >= BminY, AminZ <= BmaxZ, AmaxZ >= BminZ)):
        return (0, 0, 0)
    
    if d_pos[1] > s_pos[1]:
        ydist = BmaxY - AminY
    elif d_pos[1] < s_pos[1]:
        ydist = BminY - AmaxY
    else:
        ydist = 0
    
    if d_pos[0] > s_pos[0]:
        xdist = BmaxX - AminX
    elif d_pos[0] < s_pos[0]:
        xdist = BminX - AmaxX
    else:
        xdist = 0
    
    if d_pos[2] > s_pos[2]:
        zdist = BmaxZ - AminZ
    elif d_pos[2] < s_pos[2]:
        zdist = BminZ - AmaxZ
    else:
        zdist = 0
    
    if abs(xdist) < abs(ydist):
        if abs(zdist) < abs(xdist):
            return (0, 0, zdist)
        return (xdist, 0, 0)
    else:
        if abs(zdist) < abs(ydist):
            return (0, 0, zdist)
        return (0, ydist, 0)
    
    return (0, ydist, 0)