# Importing the Necessary Packages
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class VSI_Guage:

    def line(y1, y2):
        glBegin(GL_LINES)
        glVertex2f(0.0, y1)
        glVertex2f(0.0, y2)
        glEnd()

    def marks(self, radius, small, med, large):

        def line(y1, y2):
            glBegin(GL_LINES)
            glVertex2f(0.0, y1)
            glVertex2f(0.0, y2)
            glEnd()

        def text(x, y, s):
            glPushMatrix()
            glTranslatef(x, y - 6.0, 0.0)
            glScalef(0.13, 0.13, 0.0)
            guage.glText(s)
            glPopMatrix()

        # Set up lists with degree marks
        a = [large] * 3 + [small] * 4 + [med] + [small] * 4
        size = a + [large] + a[::-1]  # Above + large at 0 + reverse of above
        # Now Degrees to rotate
        rot = [15] * 2 + [6] * 20 + [15] * 3
        glColor(guage.white)
        glLineWidth(2.0)
        glPushMatrix()
        # Go through all point on list
        for i in range(25):
            line(radius, radius - size[i])
            glRotate(rot[i], 0.0, 0.0, 1.0)
        glPopMatrix()

        # Draw text 1,2,4 on top and bottom and appropriate spot
        x1, y1 = -46.0, 70
        x2, y2 = -26.0, 78
        x4, y4 = -6.0, 82
        # 1's
        text(x1, y1, "1")
        text(x1, -y1, "1")
        # 2's
        text(x2, y2, "2")
        text(x2, -y2, "2")
        # 4's
        text(x4, y4, "4")
        text(x4, -y4, "4")

    def pointer(self, radius, VS):
        # Draw Pointer, convert vertical speed to correct angle
        value = abs(VS)  # Disregard negative for now.
        # Determine appropriate angle
        if value <= 1000:  # Linear up to 1000
            # 1000 foot mark is at angle 60 degrees
            angle = value / 1000.0 * -60  # make float
        else:  # Value above 1000' exp scale
            if value > 4500:
                value = 4500  # Put upper limit on guage
            x = (value / 1000.0) - 1.0
            y = (-1.0/6*x*x)+(7.0/6*x)
            # print y
            # y=1 at 2000 foot mark 15deg, y =2 at 4000 ft mark 30deg
            angle = -60 - (y * 15)
        if VS <= 0:
            angle = angle * -1.0  # If VS negative then make angle -
        # Draw Pointer
        # angle =0
        glColor(guage.green)
        glLineWidth(2.0)
        glPushMatrix()
        glRotate(angle, 0.0, 0.0, 1.0)
        glTranslatef(-radius + 10.0, 0.0, 0.0)
        # Draw line and arrow
        glBegin(GL_LINES)  # Draw Line
        glVertex2f(40.0, 0.0)
        glVertex2f(0.0, 0.0)
        glEnd()
        glBegin(GL_POLYGON)  # Draw Tip
        glVertex2f(0.0, 0.0)
        glVertex2f(30.0, 5.0)
        glVertex2f(30.0, -5.0)
        glEnd()
        glPopMatrix()

    def text(self, VS):
        # Draw text in center of guage
        glColor(guage.green)
        glPushMatrix()
        glTranslate(-18.0, -6.0, 0.0)
        glScalef(0.13, 0.13, 0.0)
        value = round(abs(VS / 1000.0), 1)
        if value >= 10:
            guage.glText("%2.0f" % value)
        else:
            guage.glText("%2.1f" % value)
        glPopMatrix()

    def draw(self, x, y, radius, VS):
        glPushMatrix()
        glTranslate(x, y, 0.0)
        self.marks(radius, 5, 10, 15)
        self.pointer(radius, VS)
        self.text(VS)
        glPopMatrix()


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
    scissor.x_s = x_s
    scissor.y_s = y_s
    if smooth:
        # Enable Smoothing Antianalising
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_BLEND)
        # GlBlendFunc
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)


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

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        pygame.display.flip()
        pygame.time.wait(10)


x = 1024
y = 768
# Display Window through pygame
InitPyGame()
InitView(True, x, y)
main(x, y)
