#!/usr/bin/python3

import cv2
import numpy as np
import matplotlib.pyplot as plt

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL import Image
from cv2 import cvtColor

from objloader import *
 
def initOpenGL(dimensions):

    (width, height) = dimensions
    
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
 
    fovy = 45
    aspect = (width)/(height)
    gluPerspective(fovy, aspect, 0.1, 100.0)

def drawBackground(frame):
    # Convert frame to OpenGL format
    background = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    background = cv2.flip(background, 0)

    height, width, channels = background.shape
    background = np.frombuffer(background.tobytes(), dtype=background.dtype, count=height * width * channels)
    background.shape = (height, width, channels)

    glBindTexture(GL_TEXTURE_2D, background_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, background)
    glDepthMask(GL_FALSE)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)

    glMatrixMode(GL_MODELVIEW)
    glBindTexture(GL_TEXTURE_2D, background_id)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, background)
    glPushMatrix()

    # Plane with video frame texture
    glBegin(GL_QUADS)
    glTexCoord2i(0, 0); glVertex2i(0, 0)
    glTexCoord2i(1, 0); glVertex2i(width, 0)
    glTexCoord2i(1, 1); glVertex2i(width, height)
    glTexCoord2i(0, 1); glVertex2i(0, height)
    glEnd()
    glPopMatrix()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)
    glDepthMask(GL_TRUE)
    glDisable(GL_TEXTURE_2D)

'''
Loop de renderização
'''
def displayCallback():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # habilita o uso de texturas (o Pikachu tem textura)
    glEnable(GL_TEXTURE_2D)

    read, frame = vid.read()

    if read:
        drawBackground(frame)   


def idleCallback():
    glutPostRedisplay()
   
    

if __name__ == '__main__':
    # Intrinsic paremeters from camera calibration


    # Open input video
    vid = cv2.VideoCapture('tp2-icv-input.mp4')

    # Viewport dimensions
    dimensions = (1920, 1080)

    # GLUT configuration
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION)
    glutInitWindowSize(*dimensions)
    window = glutCreateWindow(b'Realidade Aumentada')

    # OpenGL intialization
    initOpenGL(dimensions)
        
    # Load Pikachu model
    obj = OBJ("Pikachu.obj", swapyz=True)

    # Background 
    background_id = glGenTextures(1)

    glutDisplayFunc(displayCallback)
    glutIdleFunc(idleCallback)

    glutMainLoop()

    vid.release()