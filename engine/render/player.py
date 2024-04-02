from OpenGL.GL import *
from engine import hot
from engine.render import mesh
import numpy as np
from engine.cfg import player
from engine import texture

GRID_SIZE = 8
ONE_OVER_GS = 1 / GRID_SIZE

def get_pos(x, y):
    minx = x * ONE_OVER_GS
    maxx = x * ONE_OVER_GS + ONE_OVER_GS
    miny = y * ONE_OVER_GS
    maxy = y * ONE_OVER_GS + ONE_OVER_GS
    return ((minx, maxy), (maxx, miny))

def get_pos1x2(x, y):
    minx = x * ONE_OVER_GS
    maxx = x * ONE_OVER_GS + ONE_OVER_GS
    miny = y * ONE_OVER_GS
    maxy = y * ONE_OVER_GS + ONE_OVER_GS * 2
    return ((minx, maxy), (maxx, miny))

def render_players():
    to_gen_meshes = []
    for i in hot.other_players.copy().keys():
        glPushMatrix()
        glTranslatef(*hot.other_players[i]["pos"])

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        try:
            hot.other_players[i]["mesh"].display_mesh_vbo()
        except:
            to_gen_meshes.append(i)

        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)

        glPopMatrix()
    
    for i in to_gen_meshes:
        try:
            vertices = []
            colors = []
            texcoords = []

            cx, cy, cz = player.collider

                    #vertices.extend([x -0.5, y + 0.5, z + 0.5])
                    #vertices.extend([x -0.5, y + 0.5, z - 0.5])
                    #vertices.extend([x -0.5, y - 0.5, z - 0.5])
                    #vertices.extend([x -0.5, y - 0.5, z + 0.5])
    #
                    #tex_coords.extend([tex_left[1][0], tex_left[1][1]])
                    #tex_coords.extend([tex_left[0][0], tex_left[1][1]])
                    #tex_coords.extend([tex_left[0][0], tex_left[0][1]])
                    #tex_coords.extend([tex_left[1][0], tex_left[0][1]])

            btm = get_pos(3, 0)
            vertices.extend([cx / 2, -cy / 2, cz / 2, -cx / 2, -cy / 2, cz / 2, -cx / 2, -cy / 2, -cz / 2, cx / 2, -cy / 2, -cz / 2])
            colors.extend([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            texcoords.extend([btm[0][0], btm[0][1], btm[1][0], btm[0][1], btm[1][0], btm[1][1], btm[0][0], btm[1][1]])

            top = get_pos(4, 0)
            vertices.extend([cx / 2, cy / 2, cz / 2, cx / 2, cy / 2, -cz / 2, -cx / 2, cy / 2, -cz / 2, -cx / 2, cy / 2, cz / 2])
            colors.extend([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            texcoords.extend([top[0][0], top[0][1], top[1][0], top[0][1], top[1][0], top[1][1], top[0][0], top[1][1]])

            front = get_pos1x2(0, 0)
            vertices.extend([cx / 2, cy / 2, cz / 2, -cx / 2, cy / 2, cz / 2, -cx / 2, -cy / 2, cz / 2, cx / 2, -cy / 2, cz / 2])
            colors.extend([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            texcoords.extend([front[1][0], front[1][1], front[0][0], front[1][1], front[0][0], front[0][1], front[1][0], front[0][1]])

            back = get_pos1x2(2, 0)
            vertices.extend([cx / 2, cy / 2, -cz / 2, cx / 2, -cy / 2, -cz / 2, -cx / 2, -cy / 2, -cz / 2, -cx / 2, cy / 2, -cz / 2])
            colors.extend([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            texcoords.extend([back[0][0], back[1][1], back[0][0], back[0][1], back[1][0], back[0][1], back[1][0], back[1][1]])

            right = get_pos1x2(1, 0)
            vertices.extend([cx / 2, cy / 2, cz / 2, cx / 2, -cy / 2, cz / 2, cx / 2, -cy / 2, -cz / 2, cx / 2, cy / 2, -cz / 2])
            colors.extend([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            texcoords.extend([right[0][0], right[1][1], right[0][0], right[0][1], right[1][0], right[0][1], right[1][0], right[1][1]])

            left = get_pos1x2(1, 0)
            vertices.extend([-cx / 2, cy / 2, cz / 2, -cx / 2, cy / 2, -cz / 2, -cx / 2, -cy / 2, -cz / 2, -cx / 2, -cy / 2, cz / 2])
            colors.extend([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            texcoords.extend([left[1][0], left[1][1], left[0][0], left[1][1], left[0][0], left[0][1], left[1][0], left[0][1]])

            hot.other_players[i]["mesh"] = mesh.Mesh(np.array(vertices, np.float32), np.array(colors, np.float32), np.array(texcoords, np.float32), texture.player_atlas)
            hot.other_players[i]["mesh"].create_mesh_vbo()
        except:
            None