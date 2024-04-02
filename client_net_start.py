from engine.window import Window
from engine.net.networking import loop_recv, loop_send, connect, info_thread
from _thread import start_new_thread

Window.init()

connect()

start_new_thread(info_thread, ())
start_new_thread(loop_recv, ())
start_new_thread(loop_send, ())

Window.run()