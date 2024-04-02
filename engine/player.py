import glfw, math
from OpenGL.GL import *
from OpenGL.GLU import gluLookAt

from engine.cfg.reader import MID
from engine.window import instance
from engine import hot
from engine.cfg.world import chunk_size, chunk_height
from engine.world import world
from engine.physics import aabb
from engine.cfg import player
from time import time
from engine.input import MouseButtonClick, IfKeyHeld, GetScrollPos
from engine.ray import ray_step
from engine.cfg.blocks import BLOCKS
from engine.net import networking

class Player():
    def __init__(self):
        self.mouse_sensitivity = 0.002
        self.pos = [0, 0, 0]
        self.rot = [0, math.pi / 2]
        self.vel = [0, 0, 0]

        self.can_turn = True
        self.can_move = True
        self.is_grounded = False
        self.last_jump = time()
        self.selected_block_id = 0
    def handle_movement(self):
        if GetScrollPos() > 0:
            self.selected_block_id += 1
        elif GetScrollPos() < 0:
            self.selected_block_id -= 1
        
        if self.selected_block_id > len(BLOCKS) - 1:
            self.selected_block_id -= len(BLOCKS)
        elif self.selected_block_id < 0:
            self.selected_block_id += len(BLOCKS)

        if self.can_move:
            if IfKeyHeld("w"):
                self.pos[0] += math.sin(self.rot[0]) * player.move_speed * hot.deltatime
                self.pos[2] += math.cos(self.rot[0]) * player.move_speed * hot.deltatime
            if IfKeyHeld("s"):
                self.pos[0] -= math.sin(self.rot[0]) * player.move_speed * hot.deltatime
                self.pos[2] -= math.cos(self.rot[0]) * player.move_speed * hot.deltatime
            if IfKeyHeld("a"):
                self.pos[0] += math.sin(self.rot[0]+math.pi/2) * player.move_speed * hot.deltatime
                self.pos[2] += math.cos(self.rot[0]+math.pi/2) * player.move_speed * hot.deltatime
            if IfKeyHeld("d"):
                self.pos[0] += math.sin(self.rot[0]-math.pi/2) * player.move_speed * hot.deltatime
                self.pos[2] += math.cos(self.rot[0]-math.pi/2) * player.move_speed * hot.deltatime
            if IfKeyHeld("space"):
                if self.is_grounded and self.vel[1] <= 0:
                    self.vel[1] = player.jump_force
                    self.is_grounded = False
                    self.pos[1] += 0.01
                    self.last_jump = time()
    def handle_mousemove(self):
        if self.can_turn:
            mx,my = glfw.get_cursor_pos(instance)
            
            self.rot[0] += (MID[0] - mx) * self.mouse_sensitivity
            self.rot[1] -= (MID[1] - my) * self.mouse_sensitivity
            self.rot[1] = min(3.13, self.rot[1])
            self.rot[1] = max(0.01, self.rot[1])

            glfw.set_cursor_pos(instance, MID[0], MID[1])
    def reset_cursor(self):
        glfw.set_cursor_pos(instance, MID[0], MID[1])
    def handle_physics(self):
        cx = math.floor((self.pos[0] + 0.5) / chunk_size)
        cy = math.floor((self.pos[1] + 0.5) / chunk_size)
        cz = math.floor((self.pos[2] + 0.5) / chunk_size)

        self.vel[1] -= player.gravity * hot.deltatime
        self.vel[1] = max(-0.45, self.vel[1])

        if self.vel[0] != 0:
            if self.vel[0] > player.min_friction:
                self.vel[0] *= player.friction_mult
            elif self.vel[0] < -player.min_friction:
                self.vel[0] *= player.friction_mult
            else:
                self.vel[0] = 0

        if self.vel[2] != 0:
            if self.vel[2] > player.min_friction:
                self.vel[2] *= player.friction_mult
            elif self.vel[2] < -player.min_friction:
                self.vel[2] *= player.friction_mult
            else:
                self.vel[2] = 0


        self.vel[1] = min(max(self.vel[1], -player.max_y_velocity), player.max_y_velocity)
        self.pos[1] += self.vel[1]

        self.vel[0] = min(max(self.vel[0], -player.max_move_velocity), player.max_move_velocity)
        self.pos[0] += self.vel[0]

        self.vel[2] = min(max(self.vel[2], -player.max_move_velocity), player.max_move_velocity)
        self.pos[2] += self.vel[2]

        is_on_ground_tmp = False

        if (cx, cy, cz) in world.world_raw:

            colls = [
                # y collisions
                (0, -0.95, 0),
                (0, 0.95, 0),

                # interior collisions, just in case
                (0, -0.45, 0),
                (0, 0.45, 0),

                # x collisions
                (0.75, -0.45, 0),
                (0.75, 0.45, 0),
                (0.75, -0.95, 0),
                (0.75, 0.95, 0),
                (-0.75, -0.45, 0),
                (-0.75, 0.45, 0),
                (-0.75, -0.95, 0),
                (-0.75, 0.95, 0),

                # z collisions
                (0, -0.45, -0.75),
                (0, 0.45, -0.75),
                (0, -0.95, -0.75),
                (0, 0.95, -0.75),
                (0, -0.45, 0.75),
                (0, 0.45, 0.75),
                (0, -0.95, 0.75),
                (0, 0.95, 0.75),
                
                # corners ( to prevent the small clipping )
                (0.75, -0.45, -0.75),
                (0.75, 0.45, -0.75),
                (0.75, -0.95, -0.75),
                (0.75, 0.95, -0.75),
                (0.75, -0.45, 0.75),
                (0.75, 0.45, 0.75),
                (0.75, -0.95, 0.75),
                (0.75, 0.95, 0.75),
                (-0.75, -0.45, -0.75),
                (-0.75, 0.45, -0.75),
                (-0.75, -0.95, -0.75),
                (-0.75, 0.95, -0.75),
                (-0.75, -0.45, 0.75),
                (-0.75, 0.45, 0.75),
                (-0.75, -0.95, 0.75),
                (-0.75, 0.95, 0.75),
                (0.75, -0.45, -0.75),
                (0.75, 0.45, -0.75),
                (0.75, -0.95, -0.75),
                (0.75, 0.95, -0.75),
                (-0.75, -0.45, -0.75),
                (-0.75, 0.45, -0.75),
                (-0.75, -0.95, -0.75),
                (-0.75, 0.95, -0.75),
                (0.75, -0.45, 0.75),
                (0.75, 0.45, 0.75),
                (0.75, -0.95, 0.75),
                (0.75, 0.95, 0.75),
                (-0.75, -0.45, 0.75),
                (-0.75, 0.45, 0.75),
                (-0.75, -0.95, 0.75),
                (-0.75, 0.95, 0.75),
            ]

            for x, y, z in colls:
                pos = (round(self.pos[0] + x), round(self.pos[1] + y), round(self.pos[2] + z))
                _chunkpos = (math.floor((pos[0] + 0.5) / chunk_size), math.floor((pos[1] + 0.5) / chunk_size), math.floor((pos[2] + 0.5) / chunk_size))
                
                if _chunkpos in world.world_raw:
                    to_check_chunk = world.world_raw[_chunkpos]

                    _posmin = (round(self.pos[0] + x) % chunk_size, round(self.pos[1] + y) % chunk_size, round(self.pos[2] + z) % chunk_size)

                    if _posmin in to_check_chunk:
                        corr = aabb.correct_aabb(self.pos, player.collider, (
                            round(self.pos[0] + x),
                            round(self.pos[1] + y),
                            round(self.pos[2] + z)),
                            [1, 1, 1])

                        if corr[1] > 0 and self.vel[1] <= 0:
                            self.vel[1] = 0
                            is_on_ground_tmp = True
                        elif corr[1] < 0:
                            self.vel[1] = 0
                        
                        if corr[0] != 0:
                            self.vel[0] = 0
                        
                        if corr[2] != 0:
                            self.vel[2] = 0

                        self.pos[0] += corr[0]
                        self.pos[1] += corr[1]
                        self.pos[2] += corr[2]
                else:
                    corr = aabb.correct_aabb(self.pos, player.collider, (
                        round(self.pos[0] + x),
                        round(self.pos[1] + y),
                        round(self.pos[2] + z)),
                        [1, 1, 1])

                    if corr[1] > 0:
                        self.vel[1] = 0
                        is_on_ground_tmp = True
                    elif corr[1] < 0:
                        self.vel[1] = 0
                        
                    if corr[0] != 0:
                        self.vel[0] = 0
                    
                    if corr[2] != 0:
                        self.vel[2] = 0

                    self.pos[0] += corr[0]
                    self.pos[1] += corr[1]
                    self.pos[2] += corr[2]

        if is_on_ground_tmp:
            self.is_grounded = True
        else:
            self.is_grounded = False
        
        if self.pos[1] < -100:
            self.pos[1] = 100
            self.vel[1] = 0
    def handle_mousedown(self):
        if MouseButtonClick(0):
            for i in range(int(player.max_reach * (1 / player.ray_reach_step_len))):
                pos = ray_step(self.pos[0], self.pos[1] + player.y_offset, self.pos[2], self.rot[0], self.rot[1], player.ray_reach_step_len * i)
                new_pos = (round(pos[0]) % chunk_size, round(pos[1]) % chunk_size, round(pos[2]) % chunk_size)
                _chunkpos = (math.floor((pos[0] + 0.5) / chunk_size), math.floor((pos[1] + 0.5) / chunk_size), math.floor((pos[2] + 0.5) / chunk_size))

                if _chunkpos in world.world_raw:
                    if new_pos in world.world_raw[_chunkpos]:
                        networking.block_change_queue.append((*_chunkpos, *new_pos, -1))

                        #world.world_raw[_chunkpos].pop(new_pos, None)
                        #world.world[_chunkpos].data.pop(new_pos, None)
                        #world.world[_chunkpos].gen_mesh_data(world.world)
                        #world.world[_chunkpos].gen_mesh()
                        return
                        
        elif MouseButtonClick(1):
            last_known_position = (0, 0, 0)
            last_known_position_chunkified = (0, 0, 0)
            last_known_chunk = (0, 0, 0)

            for i in range(int(player.max_reach * (1 / player.ray_reach_step_len))):
                new_known_position = ray_step(self.pos[0], self.pos[1] + player.y_offset, self.pos[2], *self.rot, player.ray_reach_step_len * i)
                new_known_chunk = (math.floor((new_known_position[0] + 0.5) / chunk_size), math.floor((new_known_position[1] + 0.5) / chunk_size), math.floor((new_known_position[2] + 0.5) / chunk_size))

                new_known_position_chunkified = (math.floor((new_known_position[0] + 0.5) % 16), math.floor((new_known_position[1] + 0.5) % 16), math.floor((new_known_position[2] + 0.5) % 16))

                if new_known_chunk in world.world_raw:
                    if new_known_position_chunkified in world.world_raw[new_known_chunk]:

                        if i == 0:
                            return
                        
                        if aabb.correct_aabb(self.pos, player.collider, (
                            last_known_position_chunkified[0] + last_known_chunk[0] * chunk_size,
                            last_known_position_chunkified[1] + last_known_chunk[1] * chunk_size,
                            last_known_position_chunkified[2] + last_known_chunk[2] * chunk_size
                        ), [1, 1, 1]) == (0, 0, 0):
                            if last_known_chunk in world.world_raw:
                                if not last_known_position_chunkified in world.world_raw[last_known_chunk]:
                                    networking.block_change_queue.append((*last_known_chunk, *last_known_position_chunkified, self.selected_block_id))
                        return
                
                last_known_chunk = new_known_chunk
                last_known_position = new_known_position
                last_known_position_chunkified = new_known_position_chunkified
            return
    def update(self):
        self.handle_movement()
        self.handle_physics()
        self.handle_mousemove()
        self.handle_mousedown()
        
        gluLookAt(self.pos[0], self.pos[1] + player.y_offset, self.pos[2],
            self.pos[0] + math.sin(self.rot[0]) * math.sin(self.rot[1]),
            self.pos[1] + player.y_offset + math.cos(self.rot[1]),
            self.pos[2] + math.cos(self.rot[0]) * math.sin(self.rot[1]),
            0, 1, 0)