from glfw import get_mouse_button, set_scroll_callback
from engine.window import instance
import keyboard

last_left_clicked = False
last_right_clicked = False

left_mouse_button_held = False
left_mouse_button_clicked = False

right_mouse_button_held = False
right_mouse_button_clicked = False

class MouseButton:
    LEFT = 0
    RIGHT = 1

keys = "abcdefghijklmnopqrstuvwxyz1234567890"
spec = ["shift", "ctrl"]

__keystates = {}
__keyslasttapped = {}
__keytaps = {}

for key in keys:
    __keyslasttapped[key] = False
    __keytaps[key] = False
    __keystates[key] = False

for key in spec:
    __keyslasttapped[key] = False
    __keytaps[key] = False
    __keystates[key] = False

def MouseButtonHeld(button : MouseButton | int):
    if button == MouseButton.LEFT:
        return left_mouse_button_held
    elif button == MouseButton.RIGHT:
        return right_mouse_button_held

def MouseButtonClick(button : MouseButton | int):
    if button == MouseButton.LEFT:
        return left_mouse_button_clicked
    elif button == MouseButton.RIGHT:
        return right_mouse_button_clicked

def IfKeyPress(key : str):
    return __keytaps[key]

def IfKeyHeld(key : str):
    return keyboard.is_pressed(key)

scroll_pos = 0

def GetScrollPos():
    global scroll_pos
    return scroll_pos

def scrollcallback(window, x, y):
    global scroll_pos
    scroll_pos = y

def handle_mousebased():
    global left_mouse_button_held, left_mouse_button_clicked, right_mouse_button_held, right_mouse_button_clicked, last_left_clicked, last_right_clicked

    left_mouse_button_held = get_mouse_button(instance, MouseButton.LEFT)
    right_mouse_button_held = get_mouse_button(instance, MouseButton.RIGHT)

    left_mouse_button_clicked = False
    right_mouse_button_clicked = False

    if left_mouse_button_held:
        if not last_left_clicked:
            last_left_clicked = True
            left_mouse_button_clicked = True
    else:
        last_left_clicked = False

    if right_mouse_button_held:
        if not last_right_clicked:
            last_right_clicked = True
            right_mouse_button_clicked = True
    else:
        last_right_clicked = False

def handle_scrollwheel():
    global scroll_pos

    if scroll_pos != 0:
        scroll_pos = 0

def handle_keyboard():
    for normal_key in keys:
        __keystates[normal_key] = keyboard.is_pressed(normal_key)
        __keytaps[normal_key] = False
    
    for special_key in spec:
        __keystates[special_key] = keyboard.is_pressed(special_key)
        __keytaps[special_key] = False
    
    for key in __keyslasttapped:
        if __keystates[key]:
            if not __keyslasttapped[key]:
                __keytaps[key] = True
                __keyslasttapped[key] = True
        else:
            __keyslasttapped[key] = False

__hasdone = False
def handle():
    global __hasdone
    if not __hasdone:
        set_scroll_callback(instance, scrollcallback)
        __hasdone = True
    handle_mousebased()
    handle_keyboard()
    handle_scrollwheel()