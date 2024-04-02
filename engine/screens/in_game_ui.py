from engine.ui import Image, ImageCustom
from engine.texture import load_texture
from engine import hot
from engine.cfg.blocks import BLOCKS

bg = load_texture("assets/ui/bg.png")
test = load_texture("assets/ui/Inventory_Window.png")
blocks = load_texture("assets/atlas.png")

elements = [
    Image(0, 0, 16, 9, (1, 1, 1), bg),
    Image(1, 1, 14, 7, (1, 1, 1), test),

    ImageCustom(0, 0, 1, 1, (1, 1, 1), blocks, 0, 1, 0, 1)
]

inventory_open = True

def render():
    global inventory_open

    if hot.player_instance != None:
        _block = BLOCKS[hot.player_instance.selected_block_id]

        _texs = _block["tex_zp"]
        elements[2].minxt = _texs[0][0]
        elements[2].maxxt = _texs[1][0]
        elements[2].minyt = _texs[1][1]
        elements[2].maxyt = _texs[0][1]
        elements[2].render()


    # on left click, flip
    #if MouseButtonClick(0):
    #    inventory_open = not inventory_open
    #if inventory_open:
    #    elements[1].render()
    #    elements[0].render()