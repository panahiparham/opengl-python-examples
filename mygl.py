import OpenGL
from OpenGL.GL import *

import numpy, math, sys, os
import glutils

import glfw

strVS = """
#version 330 core
layout(location = 0) in vec3 aVert;

uniform float uTheta;

out vec2 vCoord;
void main() {
    mat4 rot2 = mat4(
    vec4(cos(uTheta), sin(uTheta), 0.0, 0.0),
    vec4(-sin(uTheta), cos(uTheta), 0.0, 0.0),
    vec4(0.0, 0.0, 1.0, 0.0),
   vec4(0.0, 0.0, 0.0, 1.0)  
    );

        mat4 rot = mat4(
    vec4(cos(uTheta), 0.0, sin(uTheta), 0.0),
        vec4(0.0, 1.0, 0.0, 0.0),
    vec4(-sin(uTheta), 0.0, cos(uTheta), 0.0),

    vec4(0.0, 0.0, 0.0, 1.0)  
    );
    gl_Position = rot * rot2 * vec4(aVert, 1.0);
    vCoord = (rot * vec4(aVert, 1.0)).xy;
}
"""

strFS = """
#version 330 core
out vec4 fragColor;
in vec2 vCoord;
void main(){
    if(sin(100 * distance(vCoord, vec2(0.0, 0.0))) > 0.8){
        discard;
    }
    fragColor = vec4(0.05, 0.3, 0.8, 0.1);
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

    window = glfw.create_window(window_width, window_height, 'myGL', None, None)

    glfw.make_context_current(window)

    # init GL
    glViewport(0, 0, window_width, window_height)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.5, 0.5, 0.5, 1)




#####################################################
    program = glutils.loadShaders(strVS, strFS)
    glUseProgram(program)

    vertexData = numpy.array([-0.5, -0.5, 0.0, 0.5, -0.5, 0.0, 0.0, 0.5, 0.0], numpy.float32)
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    vertexBuffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer)
    glBufferData(GL_ARRAY_BUFFER, 4*len(vertexData), vertexData, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glBindVertexArray(0)


#################################
    glfw.set_time(0)
    win_t = 0.0

    while not glfw.window_should_close(window):
        currT = glfw.get_time()
        if currT - win_t > 0.01:
            # rotation angle
            glUniform1f(glGetUniformLocation(program, 'uTheta'), math.radians(50*win_t))
            # print(win_t)
            win_t = currT
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            # render scene
            glUseProgram(program)

            glBindVertexArray(vao)
            glDrawArrays(GL_TRIANGLES, 0, 3)
            glBindVertexArray(0)

            glfw.swap_buffers(window)
            glfw.poll_events()
    glfw.terminate()

if __name__=='__main__':
    main()