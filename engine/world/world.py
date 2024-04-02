from engine.world import chunk
import opensimplex, math

from engine.cfg.world import chunk_height, chunk_size, seed

TEST_world_size = 1

def get_block(x, y, z):
    if y == 0:
        return 1

    base = opensimplex.noise2(x / 25 + seed, z / 25 + seed) * 10 + 15

    is_tree = opensimplex.noise2(x, z)

    if is_tree > 0.6 and y < round(base) + 5 and y > round(base):
        return 3

    if is_tree > 0.6 and y < round(base) + 6 and y > round(base):
        return 4

    if is_tree > 0.6 and y == round(base):
        return 2

    if y == round(base):
        return 0
    
    if y >= round(base) - 3 and y < round(base):
        return 2
    
    if y == round(base) - 4:
        return 1
    
    if y < round(base) - 4:
        cave_noise = opensimplex.noise3(x / 25 + seed, y / 25 + seed, z / 25 + seed)

        if cave_noise < 0:
            return False

        return 1

    return False

# the currently loaded world
world = {}
world_raw = {}

load_queue = []

def find_highest_block(x, z):
    cx = math.floor(x / chunk_size)
    cz = math.floor(z / chunk_size)

    if (cx, cz) in world_raw:
        nx = x % chunk_size
        nz = z % chunk_size

        c = chunk_height - 1
        for y in range(chunk_height):
            if (nx, c - y, nz) in world_raw[(cx, cz)]:
                return [nx, c - y, nz]
    
    return (0, 0, 0)


def gen_chunk(chunk_x, chunk_z):
    data = {}

    for x in range(chunk_size):
        for y in range(chunk_height):
            for z in range(chunk_size):
                block = get_block(x + chunk_x * chunk_size, y, z + chunk_z * chunk_size)
                if block is not False:
                    data[(x, y, z)] = block

    return data

def gen_fake_world():    
    _data = gen_chunk(0, 0)
    world_raw[(0, 0)] = _data
    world[(0, 0)] = chunk.Chunk(world_raw[(0, 0)], (0, 0))
    world[(0, 0)].gen_mesh_data(world_raw)
    world[(0, 0)].gen_mesh()