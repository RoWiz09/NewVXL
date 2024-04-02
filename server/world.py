import opensimplex
from server.cfg import world
from server import hot

def get_block(x, y, z):
    cave_noise = opensimplex.noise3(x / 15 + world.seed, y / 15 + world.seed, z / 15 + world.seed)

    if cave_noise < -0.4:
        return False

    small_caves = opensimplex.noise3(x / 2 + world.seed, y / 2 + world.seed, z / 2 + world.seed)

    if small_caves > 0.6:
        return False

    return 1

def gen_chunk(chunk_x, chunk_y, chunk_z):
    data = {}

    for x in range(world.chunk_size):
        for y in range(world.chunk_height):
            for z in range(world.chunk_size):
                block = get_block(x + chunk_x * world.chunk_size, y + chunk_y * world.chunk_size, z + chunk_z * world.chunk_size)

                if block is not False:
                    data[f"{x},{y},{z}"] = block

    # Spawn area
    if chunk_x == 0 and chunk_y == 0 and chunk_z == 0:
        if "0,0,0" in data:
            data.pop("0,0,0", None)
        if "0,1,0" in data:
            data.pop("0,1,0", None)

    return data

def gen_world():
    hot.world[(0, 0, 0)] = gen_chunk(0, 0, 0)