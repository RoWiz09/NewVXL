from OpenGL.GL import *

class Mesh():
    def __init__(self, vertices, colors, texture_coords, texture_atlas_id):
        self.vertices = vertices
        self.colors = colors
        self.atlas_image_id = texture_atlas_id
        self.texture_coords = texture_coords
        self._vbo = []
    def create_mesh_vbo(self):
        _vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, _vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes + self.colors.nbytes + self.texture_coords.nbytes, None, GL_STATIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.vertices.nbytes, self.vertices)
        glBufferSubData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.colors.nbytes, self.colors)
        glBufferSubData(GL_ARRAY_BUFFER, self.vertices.nbytes + self.colors.nbytes, self.texture_coords.nbytes, self.texture_coords)
        self._vbo = _vbo
    def display_mesh_vbo(self):
        glBindBuffer(GL_ARRAY_BUFFER, self._vbo)
        glVertexPointer(3, GL_FLOAT, 0, None)
        glColorPointer(3, GL_FLOAT, 0, ctypes.c_void_p(self.vertices.nbytes))
        glTexCoordPointer(2, GL_FLOAT, 0, ctypes.c_void_p(self.vertices.nbytes + self.colors.nbytes))

        glBindTexture(GL_TEXTURE_2D, self.atlas_image_id)

        glDrawArrays(GL_QUADS, 0, len(self.vertices) // 3)
    def update_mesh_vbo(self):
        glBindBuffer(GL_ARRAY_BUFFER, self._vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes + self.colors.nbytes + self.texture_coords.nbytes, None, GL_STATIC_DRAW)

        glBufferSubData(GL_ARRAY_BUFFER, 0, self.vertices.nbytes, self.vertices)
        glBufferSubData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.colors.nbytes, self.colors)
        glBufferSubData(GL_ARRAY_BUFFER, self.vertices.nbytes + self.colors.nbytes, self.texture_coords.nbytes, self.texture_coords)