from OpenGL import GL
from OpenGL import GLU
from OpenGL import GLUT


def glText(s, space=80):
    'takes string input and outputs it to OpenGl Environment'
    for c in s:
        GL.glPushMatrix()
        if c == "1":  # If a 1 then move right a little so looks better
            GL.glTranslatef(16.0, 0.0, 0.0)
        elif c == "I":  # If a I then move right too
            GL.glTranslatef(30.0, 0.0, 0.0)
        elif c == "(":  # Looks better if moved right too
            GL.glTranslatef(25.0, 0.0, 0.0)
        if c == ".":
            s = 35
        else:
            s = space
        GLUT.glutStrokeCharacter(GLUT.GLUT_STROKE_ROMAN, ord(c))
        GL.glPopMatrix()
        GL.glTranslatef(s, 0.0, 0.0)


class VSI_Guage_747:

    def box(x1, y1, width, height):
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex2f(x1, y1)
        GL.glVertex2f(x1+width, y1)
        GL.glVertex2f(x1, y1+height)
        GL.glVertex2f(x1+width, y1+height)
        GL.glEnd()

    def line(y1, y2):
        GL.glBegin(GL.GL_LINES)
        GL.glVertex2f(0.0, y1)
        GL.glVertex2f(0.0, y2)
        GL.glEnd()

    def scale(x1, y1, width, height, upp_lim, exp):
        # Make List of Lengths
        a = []


class VSI_Guage:

    def line(y1, y2):
        GL.glBegin(GL.GL_LINES)
        GL.glVertex2f(0.0, y1)
        GL.glVertex2f(0.0, y2)
        GL.glEnd()

    def marks(self, radius):

        def line(y1, y2):
            GL.glBegin(GL.GL_LINES)
            GL.glVertex2f(0.0, y1)
            GL.glVertex2f(0.0, y2)
            GL.glEnd()

        def text(x, y, s):
            GL.glPushMatrix()
            GL.glTranslatef(x, y - 6.0, 0.0)
            GL.glScalef(0.13, 0.13, 0.0)
            glText(s)
            GL.glPopMatrix()

        # Set up lists with degree marks
        a = [15] * 3 + [5] * 4 + [10] + [5] * 4
        size = a + [15] + a[::-1]  # Above + large at 0 + reverse of above
        # Now Degrees to rotate
        rot = [30] * 3 + [6] * 20 + [15] * 2
        
        b = [5] * 4 + [10] + [5] * 4 + [15]
        deg = [180/20] * 20
        for i in range(9):
            b += [5] * 4 + [10] + [5] * 4 + [15] 

        white = (1.0, 1.0, 1.0)
        GL.glColor(white)

        GL.glLineWidth(2.0)
        GL.glPushMatrix()

        # Go through all point on list
        for i in range(25):
            line(radius, radius - size[i])
            GL.glRotate(rot[i], 0.0, 0.0, 1.0)
        GL.glPopMatrix()

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

        green = (0.0, 0.8, 0.0)
        GL.glColor(green)
        GL.glLineWidth(2.0)
        GL.glPushMatrix()
        GL.glRotate(angle, 0.0, 0.0, 1.0)
        GL.glTranslatef(-radius + 10.0, 0.0, 0.0)

        # Draw line and arrow
        GL.glBegin(GL.GL_LINES)  # Draw Line
        GL.glVertex2f(40.0, 0.0)
        GL.glVertex2f(0.0, 0.0)
        GL.glEnd()
        GL.glBegin(GL.GL_POLYGON)  # Draw Tip
        GL.glVertex2f(0.0, 0.0)
        GL.glVertex2f(30.0, 5.0)
        GL.glVertex2f(30.0, -5.0)
        GL.glEnd()
        GL.glPopMatrix()

    def text(self, VS):
        # Draw text in center of guage
        green = (0.0, 0.8, 0.0)
        GL.glColor(green)
        GL.glPushMatrix()
        GL.glTranslate(-18.0, -6.0, 0.0)
        GL.glScalef(0.13, 0.13, 0.0)
        value = round(abs(VS / 1000.0), 1)
        if value >= 10:
            glText("%2.0f" % value)
        else:
            glText("%2.1f" % value)
        GL.glPopMatrix()

    def draw(self, x, y, radius, VS):
        GL.glPushMatrix()
        GL.glTranslate(x, y, 0.0)
        self.marks(radius)
        self.pointer(radius, VS)
        self.text(VS)
        GL.glPopMatrix()
