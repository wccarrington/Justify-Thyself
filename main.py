#!/usr/bin/python
import sys
import pymunk

sys.path += ['.']
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL import error

#error.ErrorChecker._regiseterdChecker = lambda: 0
#error.ErrorChecker._currentChecker = lambda: 0

import pygame
import math
import texture

from world import getworld, Game, transitionto

import screen
import texture

keydown = None
mousedown = None

pygame.init()
pymunk.init_pymunk()

size = 1280,960
worldsize = screen.init(size)

transitionto(Game)

lastframe = pygame.time.get_ticks()

while 1:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or \
           e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            sys.exit(0)
        elif e.type == pygame.KEYDOWN:
            getworld().keydown(e.key)
        elif e.type == pygame.KEYUP:
            getworld().keyup(e.key)
        elif e.type == pygame.MOUSEBUTTONDOWN:
            getworld().click([float(x) * ws / s for x, ws, s in zip(e.pos, worldsize, size)])
    thisframe = pygame.time.get_ticks()
    dt = (thisframe - lastframe)/1000.0
    lastframe = thisframe
    getworld().step(dt)
    screen.startframe()
    getworld().draw()
    screen.endframe()
    pygame.time.wait(1)
