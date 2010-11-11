import math
import media
import pygame
import texture
import numpy
import random
import pymunk
from OpenGL.GL import *
from OpenGL.arrays import ArrayDatatype as ADT

currentworld = None
hexbuffer = None
vertexLoc = None
texCoord0Loc = None
normalLoc = None

def getworld():
    global currentworld
    return currentworld

def transitionto(world):
    global currentworld
    currentworld = world(currentworld)

class buffer:
    def __init__(self, vertbuffer, indexbuffer):
        self.buffer = glGenBuffers(1)
        self.indexbuffer = indexbuffer
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
        self.numverts = len(vertbuffer)
        vertbuffer = convertbuffer(vertbuffer)
        glBufferData(GL_ARRAY_BUFFER, ADT.arrayByteCount(vertbuffer), ADT.voidDataPointer(vertbuffer), GL_STATIC_DRAW)
    def __del__(self):
        if glDeleteBuffers:
            glDeleteBuffers(1, [self.buffer])
    def draw(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
        glVertexPointer(3, GL_FLOAT, 0, None)
        glDrawElementsui(GL_TRIANGLES, self.indexbuffer)
        glDisableClientState(GL_VERTEX_ARRAY)

def drawtext(pos, text):
    text = texture.Text(str(text))
    size = (text.horizsize(0.1), 0.1)
    orig = (pos[0] - size[0]/2.0, pos[1] - size[1]/2.0)
    text()
    glBegin(GL_QUADS)
    glTexCoord(0.0, 0.0)
    glVertex(orig[0], orig[1])
    glTexCoord(text.bounds[0], 0.0)
    glVertex(orig[0] + size[0], orig[1])
    glTexCoord(text.bounds[0], text.bounds[1])
    glVertex(orig[0] + size[0], orig[1] + size[1])
    glTexCoord(0.0, text.bounds[1])
    glVertex(orig[0], orig[1] + size[1])
    glEnd()

class World:
    def __init__(self, previous = None):
        pass
    def keydown(self, key):
        pass
    def keyup(self, key):
        pass
    def click(self, pos):
        pass
    def draw(self):
        pass
    def step(self, dt):
        pass

class Opening(World):
    def __init__(self, previous = None):
        self.splash = media.loadtexture('splash.png')
    def keydown(self, key):
        if key == pygame.K_RETURN:
            transitionto(Game)
    def draw(self):
        drawsquare((0,0), (4,3), self.splash)

def add_ball(space):
    mass = 1
    radius = 0.1
    inertia = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, inertia)
    body.position = (1.5, 1.5)
    shape = pymunk.Poly(body, [(0.1, 0.0), (0.0, 0.1), (-0.1, 0.0), (0.0, -0.1)])
    shape.friction = 0.5
    space.add(body, shape)
    return shape

def add_ground(space):
    body = pymunk.Body(pymunk.inf, pymunk.inf)
    body.position = (1.5, 2.5)
    line = pymunk.Poly(body, [(-10.0, 0.0), (10.0, 0.0), (10.0, -1.1), (-10.0, -0.1)])
    line.friction = 0.5
    space.add_static(line)
    return line

def draw_ground(ground):
    glColor(0.1, 0.9, 0.1, 1.0)
    points = ground.get_points()
    glBegin(GL_POLYGON)
    for p in points:
        glVertex(p[0], p[1], 0.0)
    glEnd()
#    x,y = ground.body.position.x, ground.body.position.y
#    glBegin(GL_LINES)
#    glVertex(x+ground.a.x, y+ground.a.y, 0.0)
#    glVertex(x+ground.b.x, y+ground.b.y, 0.0)
#    glEnd()

def draw_ball(ball):
    x, y = ball.body.position.x, ball.body.position.y
    points = ball.get_points()
    glColor(1.0, 1.0, 1.0, 1.0)
    glBegin(GL_POLYGON)
    for p in points:
        glVertex(p[0], p[1], 0.0)
    glEnd()

class Game(World):
    def __init__(self, previous = None):
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 10.0)
        self.ball = add_ball(self.space)
        self.ground = add_ground(self.space)
        self.push = False
        self.pushtime = 0
    def draw(self):
        glLoadIdentity()
        glTranslate(-self.ball.body.position.x + 2, -self.ball.body.position.y + 1.5, 0.0)
        draw_ball(self.ball)
        draw_ground(self.ground)
    def keydown(self, key):
        if key == pygame.K_RIGHT:
            self.push = True
            self.pushtime = 0
            self.ball.body.apply_force((0.4,0.0), (0.0, -1.0))
            self.ball.body.apply_force((-0.4,0.0), (0.0, 1.0))
    def keyup(self,key):
        if key == pygame.K_RIGHT:
            self.push = False
    def step(self, dt):
        if self.push:
            self.pushtime += dt
            if self.pushtime < 2.0:
                self.ball.body.apply_force((-0.2 * dt,0.0), (0.0, -1.0))
                self.ball.body.apply_force((0.2 * dt,0.0), (0.0, 1.0))
        if not self.push:
            self.ball.body.reset_forces()
        self.space.step(dt)
