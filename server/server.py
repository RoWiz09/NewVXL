from server import hot
from server.cfg import server as s_cfg
from server.world import gen_world
from _thread import start_new_thread
from server.client import recv_thread, send_thread

from uuid import uuid4

def start():
    print("Starting server...")
    hot.network_instance.bind((s_cfg.ip, s_cfg.port))

    print("Generating world...")
    gen_world()
    print("Generated!")

    print("Started server!")
    while True:
        hot.network_instance.listen(2)
        conn, addr = hot.network_instance.accept()
        _id = uuid4().hex
        print("Player connected from", addr, "with id", _id)

        start_new_thread(recv_thread, (conn, _id))
        start_new_thread(send_thread, (conn, _id))