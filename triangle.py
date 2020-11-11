import OpenGL
from OpenGL.GL import *

import numpy, math, sys, os
import glutils

import glfw


strVS = """
#version 330 core
layout(location = 0) in vec3 aVert;

void main() {
    gl_Position = vec4(aVert, 1.0);
}
"""

strFS = """
#version 330 core
out vec4 fragColor;
void main(){
    fragColor = vec4(0.05, 0.3, 0.8, 1.0);
}
"""


def main():
    # init GLFW
    glfw.init()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window_width, window_height = 1280, 720
    window_aspect = window_width / float(window_height)

    window = glfw.create_window(window_width, window_height, 'Triangle', None, None)

    glfw.make_context_current(window)

    # init GL
    glViewport(0, 0, window_width, window_height)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.5, 0.5, 0.5, 1)



    program = glutils.loadShaders(strVS, strFS)

    vertexData = numpy.array([-0.5, -0.5, 0.0, 0.5, -0.5, 0.0, 0.0, 0.5, 0.0,], numpy.float32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vertexBuffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer)
    glBufferData(GL_ARRAY_BUFFER, 4*len(vertexData), vertexData, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    glBindVertexArray(0)



    glfw.set_time(0)
    win_t = 0.0

    while not glfw.window_should_close(window):
        currT = glfw.get_time()
        if currT - win_t > 0.1:
            # rotation angle
            # print(win_t)
            win_t = currT
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            # render scene
            glUseProgram(program)

            glBindVertexArray(vao)
            
            glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
            glBindVertexArray(0)

            glfw.swap_buffers(window)
            glfw.poll_events()
    glfw.terminate()


if __name__=='__main__':
    main()