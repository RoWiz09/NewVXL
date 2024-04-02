from socket import socket
from engine.cfg import net, reader
from engine import hot
from engine.net.packing import VarInt, String, Float
from engine.world import world
from engine.world.chunk import Chunk
from time import sleep
from json import loads
import time, pygame

chunk_queue = []

for x in range(-2, 3):
    for y in range(-2, 3):
        for z in range(-2, 3):
            chunk_queue.append((x, y, z))

block_change_queue = [

]

clock = None

send_per_sec = 0
recv_per_sec = 0

def connect():
    global clock

    clock = pygame.time.Clock()

    hot.network_instance = socket()
    hot.network_instance.connect((reader.IP, reader.PORT))

def info_thread():
    global send_per_sec, recv_per_sec
    _clock = pygame.time.Clock()

    while True:
        _clock.tick(1)

        #print(f"[Network] Recieving {recv_per_sec / 1000} kb/sec, Sending {recv_per_sec / 1000} kb/sec.")

        send_per_sec = 0
        recv_per_sec = 0

def loop_send():
    global clock, send_per_sec
    sleep(0.1)
    while True:
        clock.tick(60)
        #sleep(net.net_thread_loop_wait)

        if len(chunk_queue) > 0:
            _packet = VarInt.Write(0)
            _packet += VarInt.Write(chunk_queue[0][0])
            _packet += VarInt.Write(chunk_queue[0][1])
            _packet += VarInt.Write(chunk_queue[0][2])

            chunk_queue.remove(chunk_queue[0])

            _final = VarInt.Write(len(_packet))
            _final += _packet

            send_per_sec += len(_final)

            hot.network_instance.sendall(_final)

        _packet = VarInt.Write(1)
        _packet += Float.Write(hot.player_instance.pos[0])
        _packet += Float.Write(hot.player_instance.pos[1])
        _packet += Float.Write(hot.player_instance.pos[2])

        _final = VarInt.Write(len(_packet))
        _final += _packet

        send_per_sec += len(_final)

        hot.network_instance.sendall(_final)

        if len(block_change_queue) > 0:
            _data = block_change_queue[0]
            block_change_queue.remove(block_change_queue[0])

            cx, cy, cz, x, y, z, _id = _data

            _packet = VarInt.Write(3)
            _packet += VarInt.Write(cx)
            _packet += VarInt.Write(cy)
            _packet += VarInt.Write(cz)
            _packet += VarInt.Write(x)
            _packet += VarInt.Write(y)
            _packet += VarInt.Write(z)
            _packet += VarInt.Write(_id)

            _final = VarInt.Write(len(_packet))
            _final += _packet

            send_per_sec += len(_final)

            hot.network_instance.send(_final)

def loop_recv():
    global recv_per_sec

    while True:
        packet_len = VarInt.ReadFromStream(hot.network_instance)

        recv_per_sec += packet_len + len(VarInt.Write(packet_len))

        packet_data = b""
        while len(packet_data) < packet_len:
            packet_data += hot.network_instance.recv(packet_len - len(packet_data))
        
        packet_data, packet_id = VarInt.Read(packet_data)

        if packet_id == 0: # got a chunk
            packet_data, chunk_x = VarInt.Read(packet_data)
            packet_data, chunk_y = VarInt.Read(packet_data)
            packet_data, chunk_z = VarInt.Read(packet_data)
            packet_data, chunk_data = String.Read(packet_data)

            chunk_data = loads(chunk_data)
            new_data = {}

            for k in chunk_data:
                _data = chunk_data[k]
                _npos = k.split(",")
                new_data[(int(_npos[0]), int(_npos[1]), int(_npos[2]))] = _data

            world.world_raw[(chunk_x, chunk_y, chunk_z)] = new_data
            nchunk = Chunk(world.world_raw[(chunk_x, chunk_y, chunk_z)], (chunk_x, chunk_y, chunk_z))
            nchunk.gen_mesh_data(world.world_raw)

            world.load_queue.append((chunk_x, chunk_y, chunk_z, nchunk))
        elif packet_id == 1: # keepalive return
            None
        elif packet_id == 2: # player data
            packet_data, player_data = String.Read(packet_data)
            player_data = loads(player_data)

            for i in player_data:
                if not i in hot.other_players:
                    hot.other_players[i] = player_data[i]
                else:
                    hot.other_players[i]["pos"] = player_data[i]["pos"]
            
            for i in hot.other_players.copy():
                if i not in player_data:
                    hot.other_players.pop(i, None)
        elif packet_id == 3: 
            packet_data, chunk_x = VarInt.Read(packet_data)
            packet_data, chunk_y = VarInt.Read(packet_data)
            packet_data, chunk_z = VarInt.Read(packet_data)
            packet_data, x = VarInt.Read(packet_data)
            packet_data, y = VarInt.Read(packet_data)
            packet_data, z = VarInt.Read(packet_data)
            packet_data, new_id = VarInt.Read(packet_data)

            if (chunk_x, chunk_y, chunk_z) in world.world_raw:
                if new_id == -1:
                    world.world_raw[(chunk_x, chunk_y, chunk_z)].pop((x, y, z), None)
                else:
                    world.world_raw[(chunk_x, chunk_y, chunk_z)][(x, y, z)] = new_id

                nchunk = Chunk(world.world_raw[(chunk_x, chunk_y, chunk_z)], (chunk_x, chunk_y, chunk_z))
                nchunk.gen_mesh_data(world.world_raw)

                world.load_queue.append((chunk_x, chunk_y, chunk_z, nchunk))