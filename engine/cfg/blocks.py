GRID_SIZE = 16
ONE_OVER_GS = 1 / GRID_SIZE

def block_pos(x, y): # starting from top-left
    minx = x * ONE_OVER_GS
    maxx = x * ONE_OVER_GS + ONE_OVER_GS
    miny = y * ONE_OVER_GS
    maxy = y * ONE_OVER_GS + ONE_OVER_GS
    return ((minx, maxy), (maxx, miny))

BLOCKS = [
    {
        "name" : "grass_block",
        "tex_xp" : block_pos(2, 0),
        "tex_xn" : block_pos(2, 0),
        "tex_yp" : block_pos(3, 0),
        "tex_yn" : block_pos(0, 0),
        "tex_zp" : block_pos(2, 0),
        "tex_zn" : block_pos(2, 0),
        "mesh_group" : 1,
        "is_transparent" : False,
        "emits_light" : False,
        "light_level" : 0
    },
    {
        "name" : "stone",
        "tex_xp" : block_pos(1, 0),
        "tex_xn" : block_pos(1, 0),
        "tex_yp" : block_pos(1, 0),
        "tex_yn" : block_pos(1, 0),
        "tex_zp" : block_pos(1, 0),
        "tex_zn" : block_pos(1, 0),
        "mesh_group" : 1,
        "is_transparent" : False,
        "emits_light" : False
    },
    {
        "name" : "dirt",
        "tex_xp" : block_pos(0, 0),
        "tex_xn" : block_pos(0, 0),
        "tex_yp" : block_pos(0, 0),
        "tex_yn" : block_pos(0, 0),
        "tex_zp" : block_pos(0, 0),
        "tex_zn" : block_pos(0, 0),
        "mesh_group" : 1,
        "is_transparent" : False,
        "emits_light" : False
    },
    {
        "name" : "oak_log",
        "tex_xp" : block_pos(0, 1),
        "tex_xn" : block_pos(0, 1),
        "tex_yp" : block_pos(1, 1),
        "tex_yn" : block_pos(1, 1),
        "tex_zp" : block_pos(0, 1),
        "tex_zn" : block_pos(0, 1),
        "mesh_group" : 1,
        "is_transparent" : False,
        "emits_light" : False
    },
    {
        "name" : "oak_leaves",
        "tex_xp" : block_pos(2, 1),
        "tex_xn" : block_pos(2, 1),
        "tex_yp" : block_pos(2, 1),
        "tex_yn" : block_pos(2, 1),
        "tex_zp" : block_pos(2, 1),
        "tex_zn" : block_pos(2, 1),
        "mesh_group" : 2,
        "is_transparent" : True,
        "emits_light" : False
    },
    {
        "name" : "oak_planks",
        "tex_xp" : block_pos(3, 1),
        "tex_xn" : block_pos(3, 1),
        "tex_yp" : block_pos(3, 1),
        "tex_yn" : block_pos(3, 1),
        "tex_zp" : block_pos(3, 1),
        "tex_zn" : block_pos(3, 1),
        "mesh_group" : 1,
        "is_transparent" : False,
        "emits_light" : False
    }
]