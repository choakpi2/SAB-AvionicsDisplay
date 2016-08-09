# Importing the Necessary Packages
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import VSI_Guage_747


def InitPyGame():
    glutInit(())
    pygame.init()
    s = pygame.display.set_mode((1024, 768), DOUBLEBUF | OPENGL)
    return s


def InitView(smooth, width, height):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glOrtho(0, width, 0.0, height, -1.0, 1.0)
    x_s = width/1024.0
    y_s = height/768.0
    glScalef(x_s, y_s, 1.0)
    # scissor.x_s = x_s
    # scissor.y_s = y_s
    if smooth:
        # Enable Smoothing Antianalising
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_BLEND)
        # GlBlendFunc
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)


def main(x, y, objDraw):
    while True:
        # Quit Condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        objDraw.draw(x/2, y/2, 140, 1000)
        pygame.display.flip()
        pygame.time.wait(10)


x = 1024
y = 768
# Display Window through pygame
InitPyGame()
InitView(True, x, y)
VSI = VSI_Guage_747.VSI_Guage()
main(x, y, VSI)
