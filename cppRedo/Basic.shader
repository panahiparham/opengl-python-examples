#shader vertex
#version 330 core

layout(location = 0) in vec4 position;

void main()
{
    gl_Position = position;
}



#shader fragment
#version 330 core

out vec4 color;

void main()
{
    color = vec4(0.1922, 0.6471, 0.4941, 1.0);
}