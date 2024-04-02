from socket import socket
from server.packing import VarInt, String, Float
from server import hot
from json import dumps
import pygame
from server import world

def recv_thread(conn : socket, player_id : str):
    hot.players[player_id] = {}
    hot.players[player_id]["pos"] = (0, 0, 0)
    index = len(hot.changes)
    try:
        while True:
            packet_len = VarInt.ReadFromStream(conn)

            packet_data = b""
            while len(packet_data) < packet_len:
                packet_data += conn.recv(packet_len - len(packet_data))
            
            packet_data, packet_id = VarInt.Read(packet_data)

            if packet_id == 0: # get chunk
                packet_data, x_pos = VarInt.Read(packet_data)
                packet_data, y_pos = VarInt.Read(packet_data)
                packet_data, z_pos = VarInt.Read(packet_data)

                _packet = VarInt.Write(0)
                _packet += VarInt.Write(x_pos)
                _packet += VarInt.Write(y_pos)
                _packet += VarInt.Write(z_pos)

                if not (x_pos, y_pos, z_pos) in hot.world:
                    hot.world[(x_pos, y_pos, z_pos)] = world.gen_chunk(x_pos, y_pos, z_pos)

                _packet += String.Write(dumps(hot.world[(x_pos, y_pos, z_pos)]))

                _final = VarInt.Write(len(_packet))
                _final += _packet

                conn.sendall(_final)
            elif packet_id == 1: # give player pos
                packet_data, x_pos = Float.Read(packet_data)
                packet_data, y_pos = Float.Read(packet_data)
                packet_data, z_pos = Float.Read(packet_data)

                hot.players[player_id]["pos"] = (x_pos, y_pos, z_pos)
            elif packet_id == 2: # keepalive
                _packet = VarInt.Write(1)

                _final = VarInt.Write(len(_packet))
                _final += _packet
                conn.sendall(_final)
            elif packet_id == 3: # block update
                packet_data, cx_pos = VarInt.Read(packet_data)
                packet_data, cy_pos = VarInt.Read(packet_data)
                packet_data, cz_pos = VarInt.Read(packet_data)
                packet_data, x_pos = VarInt.Read(packet_data)
                packet_data, y_pos = VarInt.Read(packet_data)
                packet_data, z_pos = VarInt.Read(packet_data)
                packet_data, new_id = VarInt.Read(packet_data)

                if (cx_pos, cy_pos, cz_pos) in hot.world:
                    if new_id == -1:
                        hot.world[(cx_pos, cy_pos, cz_pos)].pop((f"{x_pos},{y_pos},{z_pos}"), None)
                    else:
                        hot.world[(cx_pos, cy_pos, cz_pos)][f"{x_pos},{y_pos},{z_pos}"] = new_id

                    hot.changes.append((cx_pos, cy_pos, cz_pos, x_pos, y_pos, z_pos, new_id))

            if index < len(hot.changes):
                cx, cy, cz, x, y, z, _id = hot.changes[index]
                index += 1

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

                conn.sendall(_final)
    except Exception as e:
        print("Player with id", player_id, "lost connection.", e)
        hot.players.pop(player_id, None)

def send_thread(conn : socket, player_id : str):
    _clock = pygame.time.Clock()

    while True:
        _clock.tick(60)

        player_data = {}

        for i in hot.players.copy():
            if not i == player_id:
                player_data[i] = {}
                player_data[i]["pos"] = hot.players[i]["pos"]

        _packet = VarInt.Write(2)
        _packet += String.Write(dumps(player_data))

        _final = VarInt.Write(len(_packet))
        _final += _packet
            
        conn.sendall(_final)