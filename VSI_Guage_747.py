from OpenGL import GL
from OpenGL import GLUT


class VSI_Guage_747:

    def metronome(self, heightL, heightR, width, value, maxLim):

        GL.glBegin(GL.GL_POLYGON)
        GL.glColor((0.2, 0.2, 0.3))
        GL.glVertex2f(0, heightL)
        GL.glVertex2f(width, heightR)
        GL.glVertex2f(width, -heightR)
        GL.glVertex2f(0, -heightL)
        GL.glEnd()

        y1 = (0.9 * heightL * value) / (maxLim * 1000)
        y2 = (0.9 * heightR * value) / (maxLim * 1000)

        GL.glBegin(GL.GL_LINES)
        GL.glColor((1.0, 1.0, 1.0))
        GL.glVertex2f(0.0, y1)
        GL.glVertex2f(width, y2)
        GL.glEnd()

    def ruler(self, maxLim, height, expo):

        def ticks(length, y):
            GL.glBegin(GL.GL_LINES)
            GL.glColor((1.0, 1.0, 1.0))
            GL.glVertex2f(0.0, y)
            GL.glVertex2f(length, y)
            GL.glEnd()

        def box(height, width):
            GL.glBegin(GL.GL_QUADS)
            GL.glColor((0.2, 0.2, 0.3))
            GL.glVertex2f(0, 0)
            GL.glVertex2f(width, 0)
            GL.glVertex2f(width, height)
            GL.glVertex2f(0, height)
            GL.glEnd()

        def label(x, y, s):
            'takes string input and outputs it to OpenGl Environment'
            GL.glPushMatrix()
            GL.glTranslatef(x, y, 0.0)
            GL.glScalef(0.1, 0.1, 0.1)
            for c in s:
                GLUT.glutStrokeCharacter(GLUT.GLUT_STROKE_ROMAN, ord(c))
                GL.glTranslatef(20, 0.0, 0.0)
            GL.glPopMatrix()

        # Make a list of lengths, labels, thickness, width, etc
        efH = (0.9) * height  # The Effective Pixel Height
        num_label, mark_width, y_coord, mark_thick = [], [], [], []
        y_count = 0
        for i in range(1, maxLim+1):
            num_label += [0] + [i]
            mark_width += [5] * 2
            mark_thick += [1] + [2]
            y_count += efH/(maxLim*2)
            y_coord += [y_count]
            y_count += efH/(maxLim*2)
            y_coord += [y_count]

        # Draw the box
        box(height, -30)
        box(-height, -30)

        # Draw the ticks and labels
        for i in range(0, maxLim*2):
            GL.glPushMatrix()
            GL.glLineWidth(mark_thick[i])
            ticks(-mark_width[i], y_coord[i])
            ticks(-mark_width[i], -y_coord[i])
            GL.glPopMatrix()
            if num_label[i] != 0:
                label(-15, y_coord[i]-5, str(num_label[i]))
                label(-27, -y_coord[i]-5, str(-num_label[i]))

    def draw(self, x, y):
        GL.glPushMatrix()
        GL.glTranslate(x, y, 0.0)
        self.ruler(5, 150, False)
        self.metronome(150, 50, 30, 2000, 5)
        GL.glPopMatrix()
