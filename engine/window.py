import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

from engine.cfg.reader import RESOLUTION
from engine import texture, states, hot
from engine.world import world
from engine.cfg.world import chunk_size
from engine.render import player

instance = None

class Window():
    def init():
        global instance
        
        # if glfw cant be loaded, we cant launch a window anyway
        if not glfw.init():
            quit()

        # enable opengl
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE)

        # set as not resizable
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)

        # make the window
        instance = glfw.create_window(RESOLUTION[0], RESOLUTION[1], "vxl", glfw.get_primary_monitor(), None)

        if not instance: # if it fails, kill glfw and exit
            glfw.terminate()
            quit()
        
        # make the window the current one to draw to, so we can actually see something!
        glfw.make_context_current(instance)

        # set the 3d scene with specified fov and perspective view
        glMatrixMode(GL_PROJECTION)
        gluPerspective(75, (RESOLUTION[0] / RESOLUTION[1]), 0.01, 1024)
        glMatrixMode(GL_MODELVIEW)

        glClearColor(0, 0, 0, 1) # set the default clear color

        # enable depth sorting, face culling, textures, and transparency
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_TEXTURE_2D)

        glEnable(GL_ALPHA_TEST)
        glAlphaFunc(GL_GEQUAL, 0.5)

        # for some reason, the following does not work very well in terms of sorting:
        
        #glEnable(GL_BLEND)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # initialize the textures
        texture.init()
    def run():
        global instance, clock

        from engine.UiManager import UI
        from engine.input import handle as inphandle
        from engine.player import Player

        uiManager = UI()

        hot.player_instance = Player()
        _spawnpos = world.find_highest_block(0, 0)
        if _spawnpos == False:
            _spawnpos = [0, 100, 0]
        hot.player_instance.pos = [_spawnpos[0] + 0.001, _spawnpos[1] + 1, _spawnpos[2] + 0.001] # small offset to trigger collisions
        last_frame_time = glfw.get_time()

        # keep running the window until closed
        while not glfw.window_should_close(instance):
            glfw.poll_events()

            # get opengl ready for a new frame
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            # get the current delta time
            current_time = glfw.get_time()
            hot.deltatime = current_time - last_frame_time
            last_frame_time = current_time
            
            # generate chunks if needed
            if len(world.load_queue) > 0:
                _data = world.load_queue[0]
                world.load_queue.remove(world.load_queue[0])

                world.world[(_data[0], _data[1], _data[2])] = _data[3]
                world.world[(_data[0], _data[1], _data[2])].gen_mesh()

            # render things
            if states.window == states.WindowStates.MAIN_MENU:
                glMatrixMode(GL_PROJECTION)
                glPushMatrix()
                glLoadIdentity()
                gluOrtho2D(0, 1, 1, 0)
                glMatrixMode(GL_MODELVIEW)
                glPushMatrix()
                glLoadIdentity()

                uiManager.RenderMenu(0)
                uiManager.HandleInput(0)

                glMatrixMode(GL_PROJECTION)
                glPopMatrix()
                glMatrixMode(GL_MODELVIEW)
                glPopMatrix()
                glLoadIdentity()
            if states.window == states.WindowStates.IN_GAME:
                hot.player_instance.update()

                player.render_players()

                for chunk in world.world:
                    glPushMatrix()

                    glTranslatef(chunk[0] * chunk_size, chunk[1] * chunk_size, chunk[2] * chunk_size)

                    glEnableClientState(GL_VERTEX_ARRAY)
                    glEnableClientState(GL_COLOR_ARRAY)
                    glEnableClientState(GL_TEXTURE_COORD_ARRAY)

                    world.world[chunk].render()

                    glDisableClientState(GL_TEXTURE_COORD_ARRAY)
                    glDisableClientState(GL_COLOR_ARRAY)
                    glDisableClientState(GL_VERTEX_ARRAY)

                    glPopMatrix()
                
                glMatrixMode(GL_PROJECTION)
                glPushMatrix()
                glLoadIdentity()
                gluOrtho2D(0, 1, 1, 0)
                glMatrixMode(GL_MODELVIEW)
                glPushMatrix()
                glLoadIdentity()

                uiManager.RenderMenu(1)
                uiManager.HandleInput(1, "e")

                glMatrixMode(GL_PROJECTION)
                glPopMatrix()
                glMatrixMode(GL_MODELVIEW)
                glPopMatrix()
                glLoadIdentity()

            # end rendering things

            inphandle()

            #print(1000 / (hot.deltatime * 1000))

            # finally, render the new frame.
            glfw.swap_buffers(instance)