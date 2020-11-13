import OpenGL
from OpenGL.GL import *

import numpy
import glutils

import glfw

import math

import time


strVS = """
#version 330 core

layout(location = 0) in vec3 pVert;
layout(location = 1) in vec3 nVert;

uniform vec3 uLight;

uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;

uniform float uTheta;

out vec4 vColor;

void main() {
    mat4 rot = mat4(
    vec4(cos(uTheta), sin(uTheta), 0.0, 0.0),
    vec4(-sin(uTheta), cos(uTheta), 0.0, 0.0),
    vec4(0.0, 0.0, 1.0, 0.0),
    vec4(0.0, 0.0, 0.0, 1.0)
    );


    // light and shadow

    vec4 light = uMVMatrix * vec4(uLight , 1.0);
    vec4 normal = uMVMatrix * rot * vec4(nVert , 1.0);


    float dotted = dot(normalize(light.xyz), normalize(normal.xyz));

    float intensity;

    if(dotted <= 0.0) {
        intensity = 0.0;
    } else {
        intensity = dotted;
    }

    vColor = intensity * vec4(0.0, 1.0, 1.0, 1.0);


    // position
    gl_Position =  uPMatrix * uMVMatrix * rot * vec4(pVert , 1.0);

}
"""

strFS = """
#version 330 core

in vec4 vColor;

out vec4 fragColor;

void main(){
    // fragColor = vec4(0.05, 0.3, 0.8, 0.1);
    fragColor = vColor;
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
                            # position              # normal
    positions = numpy.array([ -1.0,  1.0, -1.0,     0.0,  1.0,  0.0,
                               1.0,  1.0, -1.0,     0.0,  1.0,  0.0,
                               1.0,  1.0,  1.0,     0.0,  1.0,  0.0,
                              -1.0,  1.0,  1.0,     0.0,  1.0,  0.0,

                               1.0,  1.0,  1.0,     1.0,  0.0,  0.0,
                               1.0,  1.0, -1.0,     1.0,  0.0,  0.0,
                               1.0, -1.0, -1.0,     1.0,  0.0,  0.0,
                               1.0, -1.0,  1.0,     1.0,  0.0,  0.0,

                               1.0, -1.0,  1.0,     0.0, -1.0,  0.0,
                              -1.0, -1.0,  1.0,     0.0, -1.0,  0.0,
                              -1.0, -1.0, -1.0,     0.0, -1.0,  0.0,
                               1.0, -1.0, -1.0,     0.0, -1.0,  0.0,

                              -1.0, -1.0,  1.0,    -1.0,  0.0,  0.0,
                              -1.0,  1.0,  1.0,    -1.0,  0.0,  0.0,
                              -1.0,  1.0, -1.0,    -1.0,  0.0,  0.0,
                              -1.0, -1.0, -1.0,    -1.0,  0.0,  0.0,

                               1.0,  1.0,  1.0,     0.0,  0.0,  1.0,
                               1.0, -1.0,  1.0,     0.0,  0.0,  1.0,
                              -1.0, -1.0,  1.0,     0.0,  0.0,  1.0,
                              -1.0,  1.0,  1.0,     0.0,  0.0,  1.0,

                               1.0,  1.0, -1.0,     0.0,  0.0, -1.0,
                              -1.0,  1.0, -1.0,     0.0,  0.0, -1.0,
                              -1.0, -1.0, -1.0,     0.0,  0.0, -1.0,
                               1.0, -1.0, -1.0,     0.0,  0.0, -1.0,
                            ], numpy.float32)


    buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)
    glBufferData(GL_ARRAY_BUFFER, positions.itemsize * len(positions), positions, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, positions.itemsize * 6, None)

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, positions.itemsize * 3, None)

    
    # Projections
    pMatrix = glutils.perspective(45, 640/480.0 , 0.1, 100.0)
    mvMatrix = glutils.lookAt([ 3.0,  1.0, 3.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1])

    pMatrixUniform = glGetUniformLocation(program, b'uPMatrix')
    mvMatrixUniform = glGetUniformLocation(program, b'uMVMatrix')

    glUniformMatrix4fv(pMatrixUniform, 1, GL_FALSE, pMatrix)
    glUniformMatrix4fv(mvMatrixUniform, 1, GL_FALSE, mvMatrix)

    # Light Source 
    lightSourceUniform = glGetUniformLocation(program, b'uLight')

    glUniform3f(lightSourceUniform, 1, 0, 0)

    t = 0
    while not glfw.window_should_close(window):
        time.sleep(1/45)
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