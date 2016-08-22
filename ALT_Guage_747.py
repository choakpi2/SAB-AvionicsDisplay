from OpenGL import GL
from OpenGL import GLUT
from pygame import locals


def scissor(x, y, w, h):
    global scissor
    x_s = int(locals.scissor.x_s)
    y_s = int(locals.scissor.y_s)
    GL.glScissor(x*x_s, y*y_s, w*x_s, h*y_s)


class Alt_Guage:

    def glText(s, space=80):
        'takes string input and outputs it to OpenGl Environment'
        for c in s:
            GL.glPushMatrix()
            if c == "1":
                GL.glTranslatef(16.0, 0.0, 0.0)
            elif c == "I":
                GL.glTranslatef(30.0, 0.0, 0.0)
            elif c == "(":
                GL.glTranslatef(25.0, 0.0, 0.0)
            if c == ".":
                s = 35
            else:
                s = space
            GLUT.glutStrokeCharacter(GLUT.GLUT_STROKE_ROMAN, ord(c))
            GL.glPopMatrix()
            GL.glTranslatef(s, 0.0, 0.0)

    def alt_bug(self, altitude, bug, y_center):

        def line(y):  # Draws purple lines for bug
            GL.glVertex2f(52, y)
            GL.glVertex2f(94, y)

        units_apart = 13.0 / 20
        diff = altitude - bug
        if abs(diff) <= 300:  # If farther than that away no need to draw it.
            loc = y_center - (diff * units_apart)
            # Draw two purple lines above and below loc
            y1 = 16
            y2 = 19
            purple = (1.0, 0.0, 1.0)
            GL.glColor(purple)
            GL.glLineWidth(2.0)
            GL.glBegin(GL.GL_LINES)
            line(loc - y1)
            line(loc - y2)
            line(loc + y1)
            line(loc + y2)
            GL.glEnd()

    def tick_marks(self, altitude):

        def white_square():
            GL.glLineWidth(2.0)
            GL.glBegin(GL.GL_POLYGON)
            GL.glVertex2f(-10.0, -3)
            GL.glVertex2f(-4.0, -3)
            GL.glVertex2f(-4.0, 3)
            GL.glVertex2f(-10.0, 3)
            GL.glEnd()

        # Draw the tick mark
        # Every 20 ft is 13 units apart
        units_apart = 13.0
        y_center = 150.0
        # altitude = aircraft.altitude
        GL.glColor3f(1.0, 1.0, 1.0)
        GL.glLineWidth(2.0)
        start_tick_ten = (altitude / 20) - 16
        tick_ten = start_tick_ten
        start_loc = y_center - ((altitude - (tick_ten * 20)) * units_apart/20)
        # start_loc =0.0
        loc = start_loc

        GL.glBegin(GL.GL_LINES)
        for i in range(32):
            # Tick itself
            GL.glVertex2f(42.0, loc)
            GL.glVertex2f(50.0, loc)
            tick_ten = tick_ten + 1
            loc = loc + 13.0
        GL.glEnd()

        loc = start_loc
        tick_ten = start_tick_ten
        GL.glLineWidth(1.0)
        for i in range(32):
            # Put in numbers
            if (tick_ten >= -50) & (tick_ten % 5 == 0):  # Must be multiple of 200 and above 0 feet
                # Print out number print
                GL.glPushMatrix()
                temp = abs(tick_ten / 5) % 10
                # if tick_ten<0: temp = 10 - temp
                h = 16.0
                if temp == 0:  # Need to be lines above and below altitude
                    GL.glPushMatrix()
                    GL.glTranslatef(52.0, loc, 0.0)
                    GL.glLineWidth(2.0)
                    GL.glBegin(GL.GL_LINES)
                    GL.glVertex2f(0.0, h)
                    GL.glVertex2f(42.0, h)
                    GL.glVertex2f(0.0, -h)
                    GL.glVertex2f(42.0, -h)
                    GL.glEnd()
                    white_square()
                    GL.glPopMatrix()
                elif temp == 5:  # Need lines above and below 500' marks also
                    GL.glPushMatrix()
                    GL.glTranslatef(52.0, loc, 0.0)
                    GL.glLineWidth(2.0)
                    GL.glBegin(GL.GL_LINES)
                    GL.glVertex2f(0.0, h)
                    GL.glVertex2f(21.0, h)
                    GL.glVertex2f(0.0, -h)
                    GL.glVertex2f(21.0, -h)
                    GL.glEnd()
                    white_square()
                    GL.glPopMatrix()
                GL.glTranslatef(53.0, loc - 8.0, 0.0)
                GL.glLineWidth(2.0)
                GL.glScalef(0.15, 0.15, 1)  # Scale text, also done in else statement below.
                s = str(temp) + "00"
                self.glText(s, 90)
                GL.glPopMatrix()

            tick_ten = tick_ten + 1
            loc = loc + 13.0

    def thousand_alt_bug(self, altitude, bug, y_center):

        def line(y):  # Draws purple lines for bug
            GL.glVertex2f(21, y)
            GL.glVertex2f(37, y)

        units_apart = 0.13
        diff = altitude - bug
        if abs(diff) <= 1400:  # If farther than that away no need to draw it.
            loc = y_center - (diff * units_apart)
            # Draw two purple lines above and below loc
            y1 = 7
            y2 = 11
            purple = (1.0, 0.0, 1.0)
            GL.glColor(purple)
            GL.glLineWidth(2.0)
            GL.glBegin(GL.GL_LINES)
            line(loc - y1)
            line(loc - y2)
            line(loc + y1)
            line(loc + y2)
            GL.glEnd()

    def thousand_tick_marks(self, altitude, y_center):
        alt = altitude % 1000  # Only need the hundreds feet part because it repeats
        # Draw the tick marks
        # Every 100 ft is 13 units apart
        units_apart = 0.13  # 13.0 / 100
        black_l = y_center - 30.0
        black_h = y_center + 30.0
        # altitude = aircraft.altitude
        white = (1.0, 1.0, 1.0)
        GL.glColor(white)
        GL.glLineWidth(2.0)
        tick = (alt / 500) - 3
        loc = y_center - ((alt - (tick * 500)) * units_apart)

        for i in range(7):
            # Tick itself
            if (tick % 2):  # If odd then 500 foot mark make smaller, if even then make larger 1000 foot mark
                GL.glBegin(GL.GL_LINE_LOOP)
                GL.glVertex2f(29.0, loc - 3)
                GL.glVertex2f(37.0, loc - 3)
                GL.glVertex2f(37.0, loc + 3)
                GL.glVertex2f(29.0, loc + 3)
                GL.glEnd()
            else:
                GL.glBegin(GL.GL_LINE_LOOP)
                GL.glVertex2f(21.0, loc - 3)
                GL.glVertex2f(37.0, loc - 3)
                GL.glVertex2f(37.0, loc + 3)
                GL.glVertex2f(21.0, loc + 3)
                GL.glEnd()
            tick = tick + 1
            loc = loc + 65
        # Draw black plygon over area, therefore these ticks need to be done first, eaiser then doing multiple scissor boxes
        black = (0.0, 0.0, 0.0)
        GL.glColor(black)
        GL.glBegin(GL.GL_POLYGON)
        GL.glVertex2f(20.0, black_l)
        GL.glVertex2f(38.0, black_l)
        GL.glVertex2f(38.0, black_h)
        GL.glVertex2f(20.0, black_h)
        GL.glEnd()

    def altitude_disp(self, altitude, x, y):
        # altitude = aircraft.altitude
        def background():
            # Background with white outline
            GL.glPushMatrix()
            GL.glTranslatef(x, y, 0.0)  # Move to where point of outline is
            # Draw White Outline suronding alt reading
            GL.glColor3f(1.0, 1.0, 1.0)
            GL.glLineWidth(2.0)
            GL.glBegin(GL.GL_LINE_STRIP)
            GL.glVertex2f(20.0, 30.0)
            GL.glVertex2f(35.0, 30.0)
            GL.glVertex2f(42.0, 18.0)
            GL.glVertex2f(100, 18.0)
            GL.glEnd()
            GL.glBegin(GL.GL_LINE_STRIP)
            GL.glVertex2f(20.0, -30.0)
            GL.glVertex2f(35.0, -30.0)
            GL.glVertex2f(42.0, -18.0)
            GL.glVertex2f(100, -18.0)
            GL.glEnd()

        def thousands():  # This does the thousands and ten thousands digit
            alt = altitude
            thou = alt // 1000

            def text_out(d):  # Just output the text.
                GL.glScalef(0.18, 0.20, 1.0)
                self.glText("%2d" % d, 90)

            # Check to see if near change in thousand above 900 feet
            alt_1000 = alt % 1000
            GL.glPushMatrix()
            if thou < 0:  # negative number no rolling
                # Display yellow NEG in place of number
                yellow = (1.0, 1.0, 0.0)
                GL.glColor(yellow)
                GL.glDisable(GL.GL_SCISSOR_TEST)  # Turn off so text will show up
                GL.glTranslatef(28.0, 8.0, 0.0)
                GL.glScalef(0.10, 0.10, 1.0)
                self.glText("N", 0)
                GL.glTranslatef(0.0, -120.0, 0.0)
                self.glText("E", 0)
                GL.glTranslatef(0.0, -120.0, 0.0)
                self.glText("G", 0)
            elif (alt_1000 >= 970):  # Close to change in thousand will roll digits
                loc = 30 - (1000 - alt_1000)  # / 1.0
                if ((thou + 1) % 10) > 0:  # If both digits aren't changing then don't roll the 10k digit
                    if thou >= 10:  # This prevents 0 for being drawn in 10k digit spot
                        GL.glPushMatrix()  # Draw 10k digit in normal place
                        GL.glTranslatef(6.0, -10.0, 0.0)
                        GL.glScalef(0.18, 0.20, 1.0)
                        self.glText("%d" % (thou // 10))
                        GL.glPopMatrix()
                    thou = thou % 10  # Change thou to mod 10 so only 1K digit is drawn
                GL.glPushMatrix()
                GL.glTranslatef(6.0, 20.0 - loc, 0.0)
                text_out(thou + 1)
                GL.glPopMatrix()
                GL.glTranslatef(6.0, -10.0 - loc, 0.0)
                text_out(thou)
            else:
                GL.glTranslatef(6.0, -10.0, 0.0)
                text_out(thou)
            GL.glPopMatrix()

        # Main draw function for altitude_display
        # Draw Background
        GL.glDisable(GL.GL_SCISSOR_TEST)
        background()

        GL.glEnable(GL.GL_SCISSOR_TEST)
        scissor(x-10, y-15, 80, 30)
        # Draw thousands digits
        thousands()

        GL.glPopMatrix()  # Altitude_disp

    def alt_bug_text(self, bug, x, y):
        # This Displays Altitude Bug Setting
        purple = (1.0, 0.0, 1.0)
        GL.glColor(purple)
        GL.glLineWidth(2.0)
        GL.glPushMatrix()
        GL.glTranslatef(x, y, 0.0)  # Move to start of digits
        GL.glScalef(0.16, 0.16, 1.0)
        self.glText("%2d" % (bug // 1000), 95)
        GL.glScalef(0.85, 0.85, 1.0)  # Scale digits 85%
        self.glText("%03d" % (bug % 1000), 95)
        GL.glPopMatrix()

    def alt_setting_disp(self, setting, x, y):
        # This Displays the Kollsman Window Setting
        GL.glPushMatrix()
        GL.glTranslate(x, y, 0)
        GL.glLineWidth(2.0)
        cyan = (0.0, 1.0, 1.0)
        GL.glColor(cyan)
        # Text out setting
        GL.glPushMatrix()
        GL.glScalef(0.14, 0.15, 0)
        # value += 0.01
        if setting < 35:
            self.glText("%5.2f" % setting, 90)  # Round it to 2 places after decimal point 0.01 is slight correction. (Rouding Error?)
        else:
            self.glText("%4d" % setting, 90)
        GL.glPopMatrix()  # Text 29.92
        # Display IN
        if setting < 35:  # Must by HG if under 35 HPA if not.
            GL.glTranslate(58, -1, 0)  # move for In display
            GL.glScalef(0.12, 0.12, 0)
            self.glText("I N", 40)
        else:  # Must be HPA
            GL.glTranslate(53, -1, 0)
            GL.glScalef(0.12, 0.12, 0)
            self.glText("HPA", 90)
        GL.glPopMatrix()

    def draw(self, altimeter, x, y, frame_time, declutter):
        y_center = 150.0
        GL.glPushMatrix()
        GL.glEnable(GL.GL_SCISSOR_TEST)
        scissor(x, y, 100, 300)
        GL.glTranslate(x, y, 0.0)
        GL.glLineWidth(1.0)
        self.tick_marks(altimeter.indicated.value)
        if not declutter:
            self.thousand_alt_bug(altimeter.indicated.value, altimeter.bug.value, y_center)
        self.thousand_tick_marks(altimeter.indicated.value, y_center)
        if not declutter:
            self.alt_bug(altimeter.indicated.value, altimeter.bug.value, y_center)
        GL.glPopMatrix()

        GL.glPushMatrix()
        self.altitude_disp(altimeter.indicated.value, x, y + 150)
        # print altimeter.value
        GL.glDisable(GL.GL_SCISSOR_TEST)
        if not declutter:
            self.alt_bug_text(altimeter.bug.value, x+30, y+345)
            self.alt_setting_disp(altimeter.setting, x+7, y-25)
        GL.glPopMatrix()
