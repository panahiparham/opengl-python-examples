import OpenGL
from OpenGL.GL import *

import numpy
import glutils

import glfw

import math

import time


strVS = """
#version 330 core

layout(location = 0) in vec3 aVert;

uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;

uniform float uTheta;

void main() {
    mat4 rot = mat4(
    vec4(cos(uTheta), sin(uTheta), 0.0, 0.0),
    vec4(-sin(uTheta), cos(uTheta), 0.0, 0.0),
    vec4(0.0, 0.0, 1.0, 0.0),
    vec4(0.0, 0.0, 0.0, 1.0)
    );

    gl_Position =  uPMatrix * uMVMatrix * rot * vec4(aVert , 1.0);
}
"""

strFS = """
#version 330 core

out vec4 fragColor;

void main(){
    fragColor = vec4(0.05, 0.3, 0.8, 0.1);
}
"""


def main():
    if not glfw.init():
        print('glfw.init error')
        return
    
    window = glfw.create_window(640, 480, 'Cube', None, None)
    if not window:
        glfw.terminate()
        print('glfw.create_window error')
        return

    glfw.make_context_current(window)

    print(glGetString(GL_VERSION))

    # init OpenGL
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.5, 0.5, 0.5, 1)
    # glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

    
    # shader
    program = glutils.loadShaders(strVS, strFS)
    glUseProgram(program)



        # vertex buffer
    positions = numpy.array([ -1.0,  1.0, -1.0,
                               1.0,  1.0, -1.0,
                               1.0,  1.0,  1.0,
                              -1.0,  1.0,  1.0,

                               1.0,  1.0,  1.0,
                               1.0,  1.0, -1.0,
                               1.0, -1.0, -1.0,
                               1.0, -1.0,  1.0,

                               1.0, -1.0,  1.0,
                              -1.0, -1.0,  1.0,
                              -1.0, -1.0, -1.0,
                               1.0, -1.0, -1.0,

                              -1.0, -1.0,  1.0,
                              -1.0,  1.0,  1.0,
                              -1.0,  1.0, -1.0,
                              -1.0, -1.0, -1.0,

                               1.0,  1.0,  1.0,
                               1.0, -1.0,  1.0,
                              -1.0, -1.0,  1.0,
                              -1.0,  1.0,  1.0,

                               1.0,  1.0, -1.0,
                              -1.0,  1.0, -1.0,
                              -1.0, -1.0, -1.0,
                               1.0, -1.0, -1.0,], numpy.float32)


    buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)
    glBufferData(GL_ARRAY_BUFFER, positions.itemsize * len(positions), positions, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, positions.itemsize * 3, None)

    
    # Projections
    pMatrix = glutils.perspective(45, 640/480.0 , 0.1, 100.0)
    mvMatrix = glutils.lookAt([ 3.0, 3.0, 3.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1])

    pMatrixUniform = glGetUniformLocation(program, b'uPMatrix')
    mvMatrixUniform = glGetUniformLocation(program, b'uMVMatrix')

    glUniformMatrix4fv(pMatrixUniform, 1, GL_FALSE, pMatrix)
    glUniformMatrix4fv(mvMatrixUniform, 1, GL_FALSE, mvMatrix)

    t = 0
    while not glfw.window_should_close(window):
        time.sleep(1/60)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)



        # glBegin(GL_TRIANGLES)
        # glVertex2f(-0.5,  -0.5)
        # glVertex2f( 0.0 ,  0.5)
        # glVertex2f( 0.5,  -0.5)
        # glEnd()

        # rotation animation
        t = (t + 1) % 360
        # set shader angle in radians
        glUniform1f(glGetUniformLocation(program, 'uTheta'), math.radians(t))


        # draw call
        glDrawArrays(GL_QUADS, 0, 24)

        glfw.swap_buffers(window)

        glfw.poll_events()


if __name__=='__main__':
    main()