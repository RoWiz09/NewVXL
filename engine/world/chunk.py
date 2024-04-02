from engine.cfg.blocks import BLOCKS
import numpy as np
from engine.render.mesh import Mesh
from engine import texture
from engine.cfg.world import max_light_level, chunk_size, chunk_height

class Chunk():
    def __init__(self, data, pos):
        self.data = data
        self.pos = pos
    def gen_mesh_data(self, raw_chunks):
        vertices = []
        colors = []
        tex_coords = []

#        # first, get the chunk light data
#
#        block_lights = {}
#
#        for x in range(chunk_size):
#            for z in range(chunk_size):
#                block_lights[x, chunk_height, z] = (max_light_level, True)
#        
#        for block in self.data:
#            if BLOCKS[self.data[block]]["emits_light"]:
#                block_lights[block] = (BLOCKS[self.data[block]]["light_level"], False)
#        
#        to_light = {}
#        to_light = block_lights.copy()
#
#        def should_light(x, y, z, cur_light_level):
#            if (x, y, z) in block_lights:
#                if block_lights[(x, y, z)][0] < cur_light_level:
#                    return all((
#                        all((x > -1, x < chunk_size, y > -1, y < chunk_height, z > -1, z < chunk_size)),
#                    ))
#                else:
#                    return False
#            
#            if (x, y, z) in self.data:
#                if BLOCKS[self.data[(x, y, z)]]["is_transparent"]:
#                    return True
#                return False
#
#            return all((
#                all((x > -1, x < chunk_size, y > -1, y < chunk_height, z > -1, z < chunk_size)),
#            ))
#
        def should_mesh(x, y, z, cur_mesh_group):
            if not (x, y, z) in self.data:
                return True
            
            if not BLOCKS[self.data[(x, y, z)]]["mesh_group"] == cur_mesh_group:
                return True
            
            return False
#
#        calculating = True
#        while calculating:
#            c = 0
#
#            for light in to_light.copy():
#                x, y, z = light
#                light_level = to_light[light][0]
#                is_skylight = to_light[light][1]
#
#                if light_level > 0:
#                    if should_light(x, y - 1, z, light_level):
#                        if is_skylight:
#                            block_lights[(x, y - 1, z)] = (light_level, True)
#                            to_light[(x, y - 1, z)] = (light_level, True)
#                        else:
#                            block_lights[(x, y - 1, z)] = (light_level - 1, False)
#                            to_light[(x, y - 1, z)] = (light_level - 1, False)
#                        c += 1
#                    if should_light(x + 1, y, z, light_level):
#                        block_lights[(x + 1, y, z)] = (light_level - 1, False)
#                        to_light[(x + 1, y, z)] = (light_level - 1, False)
#                        c += 1
#                    if should_light(x, y, z + 1, light_level):
#                        block_lights[(x, y, z + 1)] = (light_level - 1, False)
#                        to_light[(x, y, z + 1)] = (light_level - 1, False)
#                        c += 1
#                    if should_light(x, y + 1, z, light_level):
#                        block_lights[(x, y + 1, z)] = (light_level - 1, False)
#                        to_light[(x, y + 1, z)] = (light_level - 1, False)
#                        c += 1
#                    if should_light(x, y, z - 1, light_level):
#                        block_lights[(x, y, z - 1)] = (light_level - 1, False)
#                        to_light[(x, y, z - 1)] = (light_level - 1, False)
#                        c += 1
#                    if should_light(x - 1, y, z, light_level):
#                        block_lights[(x - 1, y, z)] = (light_level - 1, False)
#                        to_light[(x - 1, y, z)] = (light_level - 1, False)
#                        c += 1
#
#                to_light.pop(light, None)
#
#            if c == 0:
#                calculating = False
#
        # end getting chunk light data

        block_lights = {}

        for pos in self.data:
            x = pos[0]
            y = pos[1]
            z = pos[2]

            mesh_group = BLOCKS[self.data[pos]]["mesh_group"]

            if should_mesh(x, y + 1, z, mesh_group):
                tex_top = BLOCKS[self.data[pos]]["tex_yp"]
                _color = 0
                if (x, y + 1, z) in block_lights:
                    _color = block_lights[(x, y + 1, z)][0]
                else:
                    _color = max_light_level
                
                _color = ((1 / max_light_level) * _color, (1 / max_light_level) * _color, (1 / max_light_level) * _color)

                colors.extend(_color)
                colors.extend(_color)
                colors.extend(_color)
                colors.extend(_color)
            
                vertices.extend([x + 0.5, y + 0.5, z + 0.5])
                vertices.extend([x + 0.5, y + 0.5, z - 0.5])
                vertices.extend([x - 0.5, y + 0.5, z - 0.5])
                vertices.extend([x - 0.5, y + 0.5, z + 0.5])

                tex_coords.extend([tex_top[0][0], tex_top[0][1]])
                tex_coords.extend([tex_top[1][0], tex_top[0][1]])
                tex_coords.extend([tex_top[1][0], tex_top[1][1]])
                tex_coords.extend([tex_top[0][0], tex_top[1][1]])
            if should_mesh(x, y - 1, z, mesh_group):
                tex_bottom = BLOCKS[self.data[pos]]["tex_yn"]
                _color = 0
                if (x, y - 1, z) in block_lights:
                    _color = block_lights[(x, y - 1, z)][0]
                else:
                    _color = max_light_level

                _color = ((1 / max_light_level) * _color, (1 / max_light_level) * _color, (1 / max_light_level) * _color)

                colors.extend(_color)
                colors.extend(_color)
                colors.extend(_color)
                colors.extend(_color)
            
                vertices.extend([x + 0.5, y -0.5, z + 0.5])
                vertices.extend([x - 0.5, y -0.5, z + 0.5])
                vertices.extend([x - 0.5, y -0.5, z - 0.5])
                vertices.extend([x + 0.5, y -0.5, z - 0.5])

                tex_coords.extend([tex_bottom[0][0], tex_bottom[0][1]])
                tex_coords.extend([tex_bottom[1][0], tex_bottom[0][1]])
                tex_coords.extend([tex_bottom[1][0], tex_bottom[1][1]])
                tex_coords.extend([tex_bottom[0][0], tex_bottom[1][1]])
            if should_mesh(x + 1, y, z, mesh_group):
                tex_right = BLOCKS[self.data[pos]]["tex_xp"]
                _color = 0
                if (x + 1, y, z) in block_lights:
                    _color = block_lights[(x + 1, y, z)][0]
                else:
                    _color = max_light_level

                _color = ((1 / max_light_level) * _color, (1 / max_light_level) * _color, (1 / max_light_level) * _color)

                colors.extend(_color)
                colors.extend(_color)
                colors.extend(_color)
                colors.extend(_color)
            
                vertices.extend([x + 0.5, y + 0.5, z + 0.5])
                vertices.extend([x + 0.5, y - 0.5, z + 0.5])
                vertices.extend([x + 0.5, y - 0.5, z - 0.5])
                vertices.extend([x + 0.5, y + 0.5, z - 0.5])

                tex_coords.extend([tex_right[0][0], tex_right[1][1]])
                tex_coords.extend([tex_right[0][0], tex_right[0][1]])
                tex_coords.extend([tex_right[1][0], tex_right[0][1]])
                tex_coords.extend([tex_right[1][0], tex_right[1][1]])
            if should_mesh(x - 1, y, z, mesh_group):
                tex_left = BLOCKS[self.data[pos]]["tex_xn"]
                _color = 0
                if (x - 1, y, z) in block_lights:
                    _color = block_lights[(x - 1, y, z)][0]
                else:
                    _color = max_light_level

                _color = ((1 / max_light_level) * _color, (1 / max_light_level) * _color, (1 / max_light_level) * _color)

                colors.extend(_color)
                colors.extend(_color)
                colors.extend(_color)
                colors.extend(_color)
            
                vertices.extend([x -0.5, y + 0.5, z + 0.5])
                vertices.extend([x -0.5, y + 0.5, z - 0.5])
                vertices.extend([x -0.5, y - 0.5, z - 0.5])
                vertices.extend([x -0.5, y - 0.5, z + 0.5])

                tex_coords.extend([tex_left[1][0], tex_left[1][1]])
                tex_coords.extend([tex_left[0][0], tex_left[1][1]])
                tex_coords.extend([tex_left[0][0], tex_left[0][1]])
                tex_coords.extend([tex_left[1][0], tex_left[0][1]])
            if should_mesh(x, y, z + 1, mesh_group):
                tex_forward = BLOCKS[self.data[pos]]["tex_zp"]
                _color = 0
                if (x, y, z + 1) in block_lights:
                    _color = block_lights[(x, y, z + 1)][0]
                else:
                    _color = max_light_level
                
                _color = ((1 / max_light_level) * _color, (1 / max_light_level) * _color, (1 / max_light_level) * _color)

                colors.extend(_color)
                colors.extend(_color)
                colors.extend(_color)
                colors.extend(_color)
            
                vertices.extend([x+0.5, y+0.5, z+0.5])
                vertices.extend([x-0.5, y+0.5, z+0.5])
                vertices.extend([x-0.5, y-0.5, z+0.5])
                vertices.extend([x+0.5, y-0.5, z+0.5])

                tex_coords.extend([tex_forward[1][0], tex_forward[1][1]])
                tex_coords.extend([tex_forward[0][0], tex_forward[1][1]])
                tex_coords.extend([tex_forward[0][0], tex_forward[0][1]])
                tex_coords.extend([tex_forward[1][0], tex_forward[0][1]])
            if should_mesh(x, y, z - 1, mesh_group):
                tex_backward = BLOCKS[self.data[pos]]["tex_zn"]
                _color = 0
                if (x, y, z - 1) in block_lights:
                    _color = block_lights[(x, y, z - 1)][0]
                else:
                    _color = max_light_level

                _color = ((1 / max_light_level) * _color, (1 / max_light_level) * _color, (1 / max_light_level) * _color)

                colors.extend(_color)
                colors.extend(_color)
                colors.extend(_color)
                colors.extend(_color)
            
                vertices.extend([x+0.5, y+0.5, z-0.5])
                vertices.extend([x+0.5, y-0.5, z-0.5])
                vertices.extend([x-0.5, y-0.5, z-0.5])
                vertices.extend([x-0.5, y+0.5, z-0.5])

                tex_coords.extend([tex_backward[0][0], tex_backward[1][1]])
                tex_coords.extend([tex_backward[0][0], tex_backward[0][1]])
                tex_coords.extend([tex_backward[1][0], tex_backward[0][1]])
                tex_coords.extend([tex_backward[1][0], tex_backward[1][1]])

        self.vertices = vertices
        self.colors = colors
        self.tex_coords = tex_coords
    def gen_mesh(self):
        self.mesh = Mesh(np.array(self.vertices, np.float32), np.array(self.colors, np.float32), np.array(self.tex_coords, np.float32), texture.atlas)
        self.mesh.create_mesh_vbo()
    def render(self):
        self.mesh.display_mesh_vbo()