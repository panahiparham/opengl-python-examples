import OpenGL
from OpenGL.GL import *

import numpy

import glfw

def ParseShader(filepath):

    vertexShader, fragmentShader = ('', '')
    currentShader = None

    with open(filepath, 'r') as src:
        for line in src:
            print(line, end='')

            if '#shader' in line:
                if 'vertex' in line:
                    currentShader = 'vertex'
                elif 'fragment' in line:
                    currentShader = 'fragment'
                else:
                    raise ValueError('Wrong Shader Format!!!')
            else:
                if currentShader == 'vertex':
                    vertexShader += line
                elif currentShader == 'fragment':
                    fragmentShader += line
                else:
                    raise ValueError('Wrong Shader Format!!!')

        return vertexShader, fragmentShader



def CompileShader(shaderType, source):
    source = [source]

    id = glCreateShader(shaderType)
    glShaderSource(id, source)
    glCompileShader(id)

    result = glGetShaderiv(id, GL_COMPILE_STATUS)
    if result == GL_FALSE:
        message = glGetShaderInfoLog(id)
        print(message)
        glDeleteShader(id)
        return 0

    return id

def CreateShader(vertexShader, fragmentShader):
    program = glCreateProgram()
    vs = CompileShader(GL_VERTEX_SHADER, vertexShader)
    fs = CompileShader(GL_FRAGMENT_SHADER, fragmentShader)

    glAttachShader(program, vs)
    glAttachShader(program, fs)
    glLinkProgram(program)
    glValidateProgram(program)

    glDeleteShader(vs)
    glDeleteShader(fs)

    return program

    


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

    

    # shader
    vertexShader, fragmentShader = ParseShader('./cppRedo/Basic.shader')

    shader = CreateShader(vertexShader, fragmentShader)

    glUseProgram(shader)




    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)


        # draw call
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(window)

        glfw.poll_events()


    # glDeleteProgram(shader)


if __name__=='__main__':
    main()