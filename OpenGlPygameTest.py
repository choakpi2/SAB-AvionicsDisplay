# Importing the Necessary Packages
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def InitPyGame():
    glutInit(())
    pygame.init()
    s = pygame.display.set_mode((1024, 768), DOUBLEBUF | OPENGL)
    return s


def InitView(smooth, width, height, ortho):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    if ortho:
        # Enable Ortho
        glOrtho(0, width, 0.0, height, -1.0, 1.0)
    if smooth:
        # Enable Smoothing Antianalising
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_BLEND)
        # GlBlendFunc
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)


def Cube():
    # Defining the Vertices Required in the Cube
    verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1))
    # Defining the Edges by connecting the Vertices
    edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
    )
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def main(x, y):
    # Setting of the gl window
    gluPerspective(45, (x/y), 0.1, 50.0)
    # Translate the Cube so we can see it
    glTranslatef(0.0, 0.0, -5)
    while True:
        # Quit Condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # Rotate the Cube
        glRotatef(1, 3, 1, 1)
        # Clear the Screen, setting up for the next draw cycle
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Draw the Cube
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)


x = 1024
y = 768
# Display Window through pygame
InitPyGame()
InitView(True, x, y, False)
main(x, y)
