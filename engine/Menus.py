from engine.ui import *
from engine.texture import load_texture
from engine import states

BG = load_texture("assets/ui/bg.png")
START_IMAGE = load_texture("assets/ui/playbtn.png")

def StartGame():
    states.window = states.WindowStates.IN_GAME

Menus = [
    [
        Image(14, 8, 2, 1, (1, 1, 1), START_IMAGE, StartGame)
    ],
    [
        Image(0, 0, 16, 9, (1, 1, 1), BG, None)
    ]
]