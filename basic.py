import OpenGL
from OpenGL.GL import *

import numpy

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



    # vertex buffer
    positions = numpy.array([-0.5, -0.5,
                              0.0,  0.5,
                              0.5, -0.5], numpy.float32)


    buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)
    glBufferData(GL_ARRAY_BUFFER, positions.itemsize * len(positions), positions, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, positions.itemsize * 2, None)

    

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        # glBegin(GL_TRIANGLES)
        # glVertex2f(-0.5,  -0.5)
        # glVertex2f( 0.0 ,  0.5)
        # glVertex2f( 0.5,  -0.5)
        # glEnd()


        # draw call
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(window)

        glfw.poll_events()


if __name__=='__main__':
    main()