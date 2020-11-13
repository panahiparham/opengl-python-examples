import OpenGL
from OpenGL.GL import *

import numpy
import glutils

import glfw

import math

import time


strVS = """
#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;

out vec3 FragPos;
out vec3 Normal;

uniform float uTheta;

uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;

void main() {

    mat4 rot = mat4(
    vec4(cos(uTheta), sin(uTheta), 0.0, 0.0),
    vec4(-sin(uTheta), cos(uTheta), 0.0, 0.0),
    vec4(0.0, 0.0, 1.0, 0.0),
    vec4(0.0, 0.0, 0.0, 1.0)
    );

    // position

    FragPos = (rot * vec4(aPos , 1.0)).xyz;
    Normal = (rot * vec4(aNormal , 1.0)).xyz;
    
    gl_Position =  uPMatrix * uMVMatrix * rot * vec4(aPos , 1.0);

}
"""

strFS = """
#version 330 core
out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;


uniform vec3 lightPos;
//uniform vec3 viewPos;
uniform vec3 lightColor;
uniform vec3 objectColor;


void main(){
    // ambient
    float ambientStrength = 0.2;
    vec3 ambient = ambientStrength * lightColor;

    // diffuse
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;


    vec3 result = (ambient + diffuse) * objectColor;
    FragColor = vec4(result, 1.0);
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
    glClearColor(0.1, 0.1, 0.1, 1)
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
    mvMatrix = glutils.lookAt([4.0,  4.0, 3.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1])

    pMatrixUniform = glGetUniformLocation(program, b'uPMatrix')
    mvMatrixUniform = glGetUniformLocation(program, b'uMVMatrix')

    glUniformMatrix4fv(pMatrixUniform, 1, GL_FALSE, pMatrix)
    glUniformMatrix4fv(mvMatrixUniform, 1, GL_FALSE, mvMatrix)

    # Lighting
    lightColorUniform = glGetUniformLocation(program, b'lightColor')
    glUniform3f(lightColorUniform, 0.1, 0.8, 0.1)

    objectColorUniform = glGetUniformLocation(program, b'objectColor')
    glUniform3f(objectColorUniform, 0.7,0.7, 0.7)

    lightPosUniform = glGetUniformLocation(program, b'lightPos')
    glUniform3f(lightPosUniform, 2.0, 4, -3.0)




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