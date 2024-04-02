from PIL import Image
import numpy as np
from OpenGL.GL import *

def load_texture(path):
    # Load the image using PIL
    texture_image = Image.open(path).convert("RGBA")
    width, height = texture_image.size

    # Convert the PIL Image to a NumPy array
    texture_data = np.array(texture_image)

    # Generate and bind the OpenGL texture
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    # Set texture parameters and upload data
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return texture

atlas_path = "assets/atlas.png"
player_atlas_path = "assets/player_atlas.png"
player_atlas = None
atlas = None

def init():
    global atlas, player_atlas
    # load the texture atlas in

    atlas = load_texture(atlas_path)
    player_atlas = load_texture(player_atlas_path)