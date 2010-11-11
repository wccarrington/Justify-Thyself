from pygame import display, OPENGL, DOUBLEBUF, FULLSCREEN, time
from OpenGL.GL import *
from OpenGL.GLU import *
import math

def init(size, fullscreen = False):
	global width, height, ratio
        width, height = size
	ratio = float(width)/float(height)
        flags = OPENGL | DOUBLEBUF
        if fullscreen:
                flags = flags | FULLSCREEN
        surface = display.set_mode(size, flags)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, ratio*3, 3, 0, -10, 10)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)

	glLineWidth(3)

        return (ratio*3, 3)
        
def startframe():
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def endframe():
        display.flip()
