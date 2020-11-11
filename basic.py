import OpenGL
from OpenGL.GL import *

import glfw

def main():
    if not glfw.init():
        print('glfw.init error')
        return
    
    window = glfw.create_window(640, 480, 'Basic', None, None)
    if not window:
        glfw.terminate()
        print('glfw.create_window error')
        return

    glfw.make_context_current(window)

    print(glGetString(GL_VERSION))

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        glBegin(GL_TRIANGLES)
        glVertex2f(-0.5, -0.5)
        glVertex2f( 0. ,  0.5)
        glVertex2f( 0.5, -0.5)
        glEnd()

        glfw.swap_buffers(window)

        glfw.poll_events()


if __name__=='__main__':
    main()