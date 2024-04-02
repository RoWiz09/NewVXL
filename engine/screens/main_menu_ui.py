from engine.ui import Image
from engine.input import MouseButtonClick, MouseButtonHeld
from engine.texture import load_texture
from engine import states, hot
from engine.world import world
play_button_img = load_texture("assets/ui/playbtn.png")

elements = [
    Image(0, 0, 1, 1, (1, 0, 0), 0),
    Image(1, 1, 1, 1, (1, 1, 0), 0),
    Image(2, 2, 1, 1, (0, 1, 1), 0),
    Image(3, 3, 1, 1, (1, 0, 1), 0),
    Image(4, 4, 1, 1, (0, 0, 1), 0),
    Image(14, 0, 2, 1, (1, 1, 1), play_button_img)
]

# triggers
is_triggered = False
is_triggered2 = False

is_button_triggered = False

def render():
    global window, is_triggered, is_triggered2, is_button_triggered

    # render all of the time
    elements[0].render()

    # on hold
    if MouseButtonHeld(0):
        elements[1].render()
    if MouseButtonHeld(1):
        elements[2].render()
    
    # on left click, flip
    if MouseButtonClick(0):
        is_triggered = not is_triggered
    if is_triggered:
        elements[3].render()
    
    # on right click, flip
    if MouseButtonClick(1):
        is_triggered2 = not is_triggered2
    if is_triggered2:
        elements[4].render()
    
    # button
    elements[5].render()

    elements[5].color = (1, 1, 1)

    if elements[5].is_mouse_colliding():
        elements[5].color = (0.6, 0.6, 0.6)

        if MouseButtonClick(0):
            while not (0, 0, 0) in world.world_raw:
                pass

            is_button_triggered = not is_button_triggered
            states.window = states.WindowStates.IN_GAME
            hot.player_instance.reset_cursor()
    else:
        is_button_triggered = False