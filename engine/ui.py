from OpenGL.GL import *
from engine.cfg.reader import RESOLUTION
import glfw
from engine.window import instance

ONE_SIXTEENTH = 1 / 16
ONE_NINTH = 1 / 9

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

class ImageCustom:
    def __init__(self, x, y, xsize, ysize, color, texture_id, minxt, maxxt, minyt, maxyt):
        self.x = x
        self.y = y
        self.xsize = xsize
        self.ysize = ysize
        self.color = color
        self.texture_id = texture_id
        self.minxt = minxt
        self.maxxt = maxxt
        self.minyt = minyt
        self.maxyt = maxyt
    def render(self):
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glBegin(GL_QUADS)
        glColor3f(*self.color)

        glTexCoord2f(self.minxt, self.minyt)
        glVertex2f(self.x * ONE_SIXTEENTH, self.y * ONE_NINTH)
        glTexCoord2f(self.minxt, self.maxyt)
        glVertex2f(self.x * ONE_SIXTEENTH, self.y * ONE_NINTH + self.ysize * ONE_NINTH)
        glTexCoord2f(self.maxxt, self.maxyt)
        glVertex2f(self.x * ONE_SIXTEENTH + self.xsize * ONE_SIXTEENTH, self.y * ONE_NINTH + self.ysize * ONE_NINTH)
        glTexCoord2f(self.maxxt, self.minyt)
        glVertex2f(self.x * ONE_SIXTEENTH + self.xsize * ONE_SIXTEENTH, self.y * ONE_NINTH)

        glEnd()
    def is_mouse_colliding(self):
        mx, my = glfw.get_cursor_pos(instance)

        minx = (self.x * ONE_SIXTEENTH) * RESOLUTION[0]
        maxx = (self.x * ONE_SIXTEENTH + self.xsize * ONE_SIXTEENTH) * RESOLUTION[0]

        miny = (self.y * ONE_NINTH) * RESOLUTION[1] 
        maxy = (self.y * ONE_NINTH + self.ysize * ONE_NINTH) * RESOLUTION[1]

        if all((mx > minx, mx < maxx, my > miny, my < maxy)):
            return True
        return False

class Image:
    def __init__(self, x, y, xsize, ysize, color, texture_id):
        self.x = x
        self.y = y
        self.xsize = xsize
        self.ysize = ysize
        self.color = color
        self.texture_id = texture_id
    def render(self):
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glBegin(GL_QUADS)
        glColor3f(*self.color)

        glTexCoord2f(0, 0)
        glVertex2f(self.x * ONE_SIXTEENTH, self.y * ONE_NINTH)
        glTexCoord2f(0, 1)
        glVertex2f(self.x * ONE_SIXTEENTH, self.y * ONE_NINTH + self.ysize * ONE_NINTH)
        glTexCoord2f(1, 1)
        glVertex2f(self.x * ONE_SIXTEENTH + self.xsize * ONE_SIXTEENTH, self.y * ONE_NINTH + self.ysize * ONE_NINTH)
        glTexCoord2f(1, 0)
        glVertex2f(self.x * ONE_SIXTEENTH + self.xsize * ONE_SIXTEENTH, self.y * ONE_NINTH)

        glEnd()
    def is_mouse_colliding(self):
        mx, my = glfw.get_cursor_pos(instance)

        minx = (self.x * ONE_SIXTEENTH) * RESOLUTION[0]
        maxx = (self.x * ONE_SIXTEENTH + self.xsize * ONE_SIXTEENTH) * RESOLUTION[0]

        miny = (self.y * ONE_NINTH) * RESOLUTION[1] 
        maxy = (self.y * ONE_NINTH + self.ysize * ONE_NINTH) * RESOLUTION[1]

        if all((mx > minx, mx < maxx, my > miny, my < maxy)):
            return True
        return False