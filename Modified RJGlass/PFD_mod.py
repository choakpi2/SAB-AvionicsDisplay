from OpenGL import GL
from OpenGL import GLUT
import sys
import os
# This is code to import config file (config.py)
try:
    import config
except ImportError:
    # We're in a py2exe, so we'll append an element to the (one element)
    # sys.path which points to Library.zip, to the directory that contains
    # Library.zip, allowing us to import config.py
    # Adds one level up from the Library.zip directory to the path, so import will go forward
    sys.path.append(os.path.split(sys.path[0])[0])
    import config

import guage  # All add on guage functions colors etc.


class PFD_Guage(object):

    class Speed_Guage:

        y_center = 140.0
        x_center = 50.0
        knot_unit = 3.5  # Number of units per knot

        def arrow(self):
            # White Arrow
            y = self.y_center
            w = 18.0
            h = 10.0
            point = 50.0  # Point of arrow's X cord
            GL.glColor(guage.white)
            GL.glLineWidth(2.0)
            GL.glBegin(GL.GL_LINE_LOOP)
            GL.glVertex2f(point, y)
            GL.glVertex2f(point + w, y - h)
            GL.glVertex2f(point + w, y + h)
            GL.glEnd()
            GL.glBegin(GL.GL_LINES)
            GL.glVertex2f(point + w, y)
            GL.glVertex2f(point + w + 12.0, y)
            GL.glEnd()

        def airspeed_diff(self, difference):
            # Pink Line above or below arrow that shoes accel or decel rate.
            # Forcast 5 seconds ahead??
            # If forcasted not difference is less than 2 knots then down't show
            if abs(difference) > 1:
                y1 = self.y_center
                y2 = y1 + difference * self.knot_unit
                x1 = self.x_center + 18
                x2 = x1 + 12.0
                GL.glLineWidth(2.0)
                GL.glColor(guage.purple)
                GL.glBegin(GL.GL_LINE_STRIP)
                GL.glVertex2f(x1, y2)
                GL.glVertex2f(x2, y2)
                GL.glVertex2f(x2, y1)
                GL.glEnd()

        def V_Speeds(self, air_spd, text_y):

            def V_Text(Vspeed, x, y):
                if Vspeed.visible:
                    GL.glPushMatrix()
                    GL.glTranslatef(x, y, 0.0)
                    GL.glPushMatrix()
                    GL.glScalef(0.15, 0.15, 1.0)
                    s = Vspeed.text + str(Vspeed.value)
                    guage.glText(s, 85.0)
                    GL.glPopMatrix()
                    GL.glPopMatrix()

            space = 30.0
            GL.glColor(guage.cyan)
            # VT
            V_Text(air_spd.VT, 5.0, text_y)
            text_y -= space
            # V2
            V_Text(air_spd.V2, 5.0, text_y)
            text_y -= space
            # VR
            V_Text(air_spd.VR, 5.0, text_y)
            text_y -= space
            # V1
            V_Text(air_spd.V1, 5.0, text_y)
            # Vselected one
            text_y = -100
            V_Text(air_spd.Vspeed_input, 5.0,  text_y)
            # After done reset color to white
            GL.glColor(guage.white)

        def Vspeed_selection(self, Vspeed, offtime, x, y):
            if guage.globaltime.value <= offtime:
                s = Vspeed.text
                # Draw text
                GL.glColor(guage.cyan)
                GL.glPushMatrix()
                GL.glTranslatef(x, y, 0.0)
                GL.glPushMatrix()
                GL.glScalef(0.15, 0.15, 1.0)
                if Vspeed.visible:
                    s += str(Vspeed.value)
                    guage.glText(s, 85.0)
                else:  # If not visible value is dashes ---
                    guage.glText(s, 85.0)
                    GL.glTranslatef(-20, 0, 0.0)  # Move dashes left a little for apperance
                    guage.glText('---', 110.0)
                GL.glPopMatrix()
                GL.glPopMatrix()

        def speed_cues(self, air_spd):

            def lowspeedcue(y):
                x1 = 45
                x2 = 80
                GL.glColor(guage.green)
                GL.glLineWidth(2.0)
                GL.glBegin(GL.GL_LINES)
                GL.glVertex2f(x1, y)
                GL.glVertex2f(x2, y)
                GL.glEnd()

            def barber_pole(start, finish, dir):
                step = 12  # Determine step between
                x1 = 52
                x2 = 64
                GL.glColor(guage.red)
                GL.glLineWidth(2.0)
                GL.glBegin(GL.GL_LINES)
                GL.glVertex2f(x1, start)
                GL.glVertex2f(x1, finish)
                GL.glVertex2f(x2, start)
                GL.glVertex2f(x2, finish)
                GL.glEnd()
                num = abs((finish - start) // step) + 1
                loc = start
                i = 0
                d = step * dir
                while i <= num:
                    i += 1
                    GL.glBegin(GL.GL_POLYGON)
                    GL.glVertex2f(x1, loc)
                    GL.glVertex2f(x2, loc)
                    loc += d
                    GL.glVertex2f(x2, loc)
                    GL.glVertex2f(x1, loc)
                    loc += d
                    GL.glEnd()

            y_center = self.y_center
            airspeed = air_spd.IAS_guage
            diff = air_spd.maxspeed - airspeed
            loc = diff * self.knot_unit
            if loc <= y_center:
                barber_pole(loc + y_center, 150 + y_center, 1)
            # Begin under_speed
            diff = air_spd.minspeed - airspeed
            loc = diff * self.knot_unit
            if loc >= -y_center:
                barber_pole(loc + y_center, -150 + y_center, -1)
            # Begin low speed awareness cue
            diff = air_spd.lowspeed - airspeed
            loc = diff * self.knot_unit
            lowspeedcue(loc + y_center)

        def tick_marks(self, air_spd, x, y):
            # Draw the tick mark
            # Every knot is 2.0 units apart
            unit_apart = self.knot_unit
            center = 50.0
            y_center = self.y_center
            # air_spd is class of speed, will use IAS, Mach, and V Speeds, possibly Ground Speed
            airspeed = air_spd.IAS_guage
            # glScissor(5, 152, 80, 300)
            guage.scissor(x, y, 90, 280)
            GL.glEnable(GL.GL_SCISSOR_TEST)
            GL.glColor3f(1.0, 1.0, 1.0)
            GL.glLineWidth(2.0)
            start_tick_ten = (int(airspeed) / 10) - 6
            tick_ten = start_tick_ten
            start_loc = y_center - ((airspeed - (tick_ten * 10)) * unit_apart)
            loc = start_loc
            GL.glBegin(GL.GL_LINES)
            vert_line_bottom = -10
            for i in range(13):
                if tick_ten == 4:
                    vert_line_bottom = loc
                if tick_ten >= 4:  # This causes nothing below 40 to be displyed
                    GL.glVertex2f(center - 10.0, loc)
                    GL.glVertex2f(center, loc)
                    if tick_ten < 20:  # If its under 200 knots add a 5 knot mork
                        mid_loc = loc + (unit_apart * 5)  # This is equivelent of 5 knots higher
                        GL.glVertex2f(center - 5.0, mid_loc)
                        GL.glVertex2f(center, mid_loc)
                tick_ten = tick_ten + 1
                loc = loc + (unit_apart * 10)
            # Draw verticle Line of airspeed tape
            GL.glVertex2f(center, vert_line_bottom)
            GL.glVertex2f(center, 300.0)
            GL.glEnd()

            loc = start_loc
            tick_ten = start_tick_ten
            GL.glLineWidth(2.0)
            for i in range(13):  # Put in numbers
                if (tick_ten >= 4) & (tick_ten % 2 == 0):  # Must be multiple of 20 and above 0 knots
                    # Print out number print
                    GL.glPushMatrix()
                    if tick_ten >= 10:
                        GL.glTranslatef(8.0, loc - 6.0, 0.0)
                        GL.glScalef(0.13, 0.13, 1)  # Scale text, also done in else statement below.
                        c = (tick_ten / 10) + 48
                        GLUT.glutStrokeCharacter(GLUT.GLUT_STROKE_ROMAN, c)
                    else:
                        GL.glTranslatef(18.0, loc - 6.0, 0.0)  # Move over since no hundreds digit
                        GL.glScalef(0.13, 0.13, 1)  # Don't forget to scale text
                    c = (tick_ten % 10) + 48
                    GLUT.glutStrokeCharacter(GLUT.GLUT_STROKE_ROMAN, c)  # Tens digit
                    GLUT.glutStrokeCharacter(GLUT.GLUT_STROKE_ROMAN, 48)  # Ones Digit
                    GL.glPopMatrix()
                elif (tick_ten == 3):  # Put in V Speed Text
                    self.V_Speeds(air_spd, loc - 12.0)
                tick_ten = tick_ten + 1
                loc = loc + (unit_apart * 10)

        def bug_polygon(self):
            GL.glColor(guage.purple)
            GL.glBegin(GL.GL_LINE_LOOP)
            GL.glVertex2f(0.0, 0.0)
            GL.glVertex2f(10.0, 8.0)
            GL.glVertex2f(10.0, 15.0)
            GL.glVertex2f(0.0, 15.0)
            GL.glVertex2f(0.0, -15.0)
            GL.glVertex2f(10.0, -15.0)
            GL.glVertex2f(10.0, -8.0)
            GL.glEnd()

        def airspeed_mach_text(self, value, x, y):  # Text on top
            GL.glLineWidth(2.0)
            GL.glColor(guage.white)
            # Draw Text Part
            GL.glPushMatrix()
            GL.glTranslate(x, y, 0.0)
            GL.glScale(0.13, 0.13, 1.0)
            guage.glText("M", 100)
            guage.glText(("%3.3f" % value)[1:], 90)
            GL.glPopMatrix()

        def airspeed_bug_text(self, bug):  # Text on top
            GL.glPushMatrix()
            GL.glLineWidth(2.0)
            # Draw Bug Symbol
            GL.glTranslate(10.0, -25.0, 0.0)
            self.bug_polygon()
            GL.glPopMatrix()
            # Draw Text Part
            GL.glPushMatrix()
            GL.glTranslate(30.0, -32.0, 0.0)
            GL.glScale(0.15, 0.15, 1.0)
            guage.glText(str(bug))
            GL.glPopMatrix()

        def airspeed_bug(self, airspeed):  # Also speed on top
            GL.glPushMatrix()
            bug_value = airspeed.bug.value
            if bug_value < 40:  # prevents bug from going below 40knot mark.
                bug_value = 40
            # Determine bugs position
            diff = bug_value - airspeed.IAS_guage
            # Determine translation amount
            unit_apart = self.knot_unit
            center = self.y_center
            noshow = center + 15.0
            t = diff * unit_apart  # 2.5 units per knot
            # If its out of bounds dont even draw it.
            if abs(t) <= noshow:
                GL.glTranslate(52.0, center + t, 0.0)  # Move to point of bug center + translation of t
                GL.glLineWidth(2.0)
                self.bug_polygon()
            GL.glPopMatrix()

        def Vspeed_bug(self, air_spd):  # Puts in the blue marks on speed tape for V-Speeds

            def mark_bug(IAS, Vbug):
                if Vbug.visible:
                    text = " " + Vbug.text[1]
                    # IAS current airspeed, bug is bug airspeed text is text to put next to mark
                    diff = (IAS - Vbug.value) * self.knot_unit
                    center = self.y_center
                    noshow = center + 5.0  # If out of this range then don't show
                    if abs(diff) <= noshow:
                        GL.glPushMatrix()
                        GL.glTranslate(30.0, center - diff, 0.0)  # Move to point of V speed bug
                        # Draw Line
                        GL.glBegin(GL.GL_LINES)
                        GL.glVertex(0.0, 0.0)
                        GL.glVertex(30.0, 0.0)
                        GL.glEnd()
                        # Draw Text next to line 1,2,R,T
                        GL.glTranslate(32.0, -6.0, 0.0)
                        GL.glScalef(0.12, 0.12, 1.0)
                        guage.glText(text, 90)
                        GL.glPopMatrix()
            GL.glColor(guage.cyan)
            GL.glLineWidth(2.0)
            mark_bug(air_spd.IAS_guage, air_spd.V1)
            mark_bug(air_spd.IAS_guage, air_spd.V2)
            mark_bug(air_spd.IAS_guage, air_spd.VR)
            mark_bug(air_spd.IAS_guage, air_spd.VT)

        def draw(self, airspeed, onground, x, y, declutter):
            # airspeed is in knots.
            # CRJ - Airspped Guage
            # Location 2,88 to 90,368
            # Start x,y point is top left corner of airspeed tape
            GL.glPushMatrix()
            GL.glTranslatef(x, y, 0.0)
            self.tick_marks(airspeed, x, y)  # Draw tick marks with numbers
            if not (onground | declutter):
                self.speed_cues(airspeed)  # If on ground don't display speed cues
            if airspeed.trend_visible:
                self.airspeed_diff(airspeed.IAS_diff)
            self.arrow()
            if not (declutter):
                self.Vspeed_bug(airspeed)
                GL.glDisable(GL.GL_SCISSOR_TEST)
                self.airspeed_bug(airspeed)
                self.airspeed_bug_text(airspeed.bug.value)
                if airspeed.Mach.active:
                    self.airspeed_mach_text(airspeed.Mach.value, 5, 300)
                self.Vspeed_selection(airspeed.Vspeed_disp, airspeed.Vspeed_disp_timer, 5, -65)
            GL.glPopMatrix()

    class Attitude_Guage:

        def __init__(self):  # Selects varient of Flight Director
            if config.FD_Type == config.LINES:  # Defaults to Inverted V
                self.Flight_Director = self.Flight_Director_Lines
                self.Center_Mark = self.Center_Mark_L
            else:
                self.Flight_Director = self.Flight_Director_V
                self.Center_Mark = self.Center_Mark_V

        def Grnd_Sky(self):
            # Draw Ground and Sky & Horizon
            GL.glColor3f(0.69, 0.4, 0.0)  # Draw Brown Color
            GL.glBegin(GL.GL_QUADS)
            GL.glVertex2f(-250.0, -800.0)
            GL.glVertex2f(250.0, -800.0)
            GL.glVertex2f(250.0, 0.0)
            GL.glVertex2f(-250.0, 0.0)
            GL.glColor3f(0.0, 0.6, 0.8)  # Draw Blue Color
            GL.glVertex2f(250.0, 0.0)
            GL.glVertex2f(-250.0, 0.0)
            GL.glVertex2f(-250.0, 800.0)
            GL.glVertex2f(250.0, 800.0)
            GL.glEnd()

            # Draw Horizon
            GL.glColor(guage.white)
            GL.glLineWidth(2.5)
            GL.glBegin(GL.GL_LINES)
            w = 115
            GL.glVertex2f(-w, 0.0)
            GL.glVertex2f(w, 0.0)
            GL.glEnd()

        def Pitch_Marks(self, pitch, line_width, pixel_per_degree, loc_active):

            def get_width(pitch):
                x = int(round(pitch / 2.5))
                if x == 0:
                    w = 0  # Horizon is now draw in Grnd_Sky()
                elif (x % 4) == 0:
                    w = 30
                elif (x % 2) == 0:
                    w = 15
                else:
                    w = 5
                return w

            # Draw the pitch marks
            # Uses pitch to determine which pitch lines need to be drawn
            # pixel_per_degree = 7.25 Starts 12.5 degrees down and goes up 11 lines
            start_point = 12.5
            num_lines = 11
            GL.glColor(guage.white)
            GL.glPushMatrix()  # Save matrix state
            GL.glLineWidth(line_width)
            # pitch = pitch * -1
            # Round pitch to nearest 2.5 degrees
            start = round(pitch / 2.5) * 2.5
            start = start - start_point  # Go down 25 degrees
            GL.glTranslatef(0.0, start * pixel_per_degree, 0.0)
            for i in range(num_lines):
                w = get_width(start)
                if w > 0:
                    GL.glBegin(GL.GL_LINES)
                    GL.glVertex2f(-w, 0.0)
                    GL.glVertex2f(w, 0.0)
                    GL.glEnd()
                if (w == 30):  # Draw number for degrees
                    c = int(round(abs(start))) / 10 + 48
                    if (c > 48):  # If greater than 0
                        GL.glPushMatrix()
                        GL.glTranslatef(30.0, -6.0, 0.0)  # Move over to right (Numbers only on right side)
                        GL.glPushMatrix()
                        GL.glScalef(0.13, 0.13, 1.0)  # Scale down for numbers
                        GLUT.glutStrokeCharacter(GLUT.GLUT_STROKE_ROMAN, c)
                        GLUT.glutStrokeCharacter(GLUT.GLUT_STROKE_ROMAN, 48)
                        GL.glPopMatrix()
                        GL.glPopMatrix()
                GL.glTranslatef(0.0, 2.5 * pixel_per_degree, 0.0)
                start = start + 2.5
            GL.glPopMatrix()

        def Center_Mark_L(self):  # This is one varent of the center mark (Boeing look) L shapes

            def Square(w):
                GL.glVertex2f(w, w)
                GL.glVertex2f(w, -w)
                GL.glVertex2f(-w, -w)
                GL.glVertex2f(-w, w)

            def L_Shape(side, w, h, l_w):
                GL.glVertex2f(-l_w * side, l_w)
                GL.glVertex2f((w + l_w) * side, l_w)
                GL.glVertex2f((w + l_w) * side, -l_w)
                GL.glVertex2f(l_w * side, -l_w)
                GL.glVertex2f(l_w * side, -l_w - h)
                GL.glVertex2f(-l_w * side, -l_w - h)
                # glVertex2f(-l_w, l_w)

            # Draws center dot and l shaped things off to the side
            # glPushMatrix() No need to push, will do not translating
            # Do black parts
            GL.glPushMatrix()
            GL.glColor3f(0.0, 0.0, 0.0)  # Black
            GL.glBegin(GL.GL_POLYGON)
            Square(5)
            GL.glEnd()
            GL.glTranslatef(45, 0, 0)
            # Right L
            GL.glBegin(GL.GL_POLYGON)
            L_Shape(1, 75, 25, 5)
            GL.glEnd()
            GL.glTranslatef(-90, 0, 0)
            # Left L
            GL.glBegin(GL.GL_POLYGON)
            L_Shape(-1, 75, 25, 5)
            GL.glEnd()
            GL.glPopMatrix()
            # Do white parts
            GL.glColor(guage.white)
            GL.glLineWidth(2.5)
            GL.glPushMatrix()
            GL.glBegin(GL.GL_LINE_LOOP)
            Square(5)
            GL.glEnd()
            GL.glTranslatef(45, 0, 0)
            # Right L
            GL.glBegin(GL.GL_LINE_LOOP)
            L_Shape(1, 75, 25, 5)
            GL.glEnd()
            # Left L
            GL.glTranslatef(-90, 0, 0)
            GL.glBegin(GL.GL_LINE_LOOP)
            L_Shape(-1, 75, 25, 5)
            GL.glEnd()
            GL.glPopMatrix()

        def Center_Mark_V(self):  # This is one varent of the center mark

            def Rect(side):
                GL.glVertex2f(-side * 106.0, 2.0)
                GL.glVertex2f(-side * 106.0, -2.0)
                GL.glVertex2f(-side * 126.0, -2.0)
                GL.glVertex2f(-side * 126.0, 2.0)

            def V_Shape(side):
                GL.glVertex2f(0, 0)
                GL.glVertex2f(side * 40.0, -30.0)
                GL.glVertex2f(side * 80.0, -30.0)

            # Draws center dot and l shaped things off to the side
            # glPushMatrix() No need to push, will do not translating
            # Do black parts
            GL.glColor3f(0.0, 0.0, 0.0)
            GL.glBegin(GL.GL_POLYGON)
            V_Shape(1)
            GL.glEnd()
            GL.glBegin(GL.GL_POLYGON)
            V_Shape(-1)
            GL.glEnd()
            # Do white parts
            GL.glColor3f(1.0, 1.0, 1.0)
            GL.glLineWidth(2.5)
            GL.glBegin(GL.GL_LINE_LOOP)
            V_Shape(1)
            GL.glEnd()
            GL.glBegin(GL.GL_LINE_LOOP)
            V_Shape(-1)
            GL.glEnd()
            # Do Rectangles on Either End
            GL.glBegin(GL.GL_LINE_LOOP)
            Rect(1)
            GL.glEnd()
            GL.glBegin(GL.GL_LINE_LOOP)
            Rect(-1)
            GL.glEnd()

        def Flight_Director_Lines(self, bank, FDbank, pitch, FDpitch):  # Draw the flight director 2 Lines (Boeing style)
            # Note: bank and pitch not used, just used for placeholders, to have same arguments as other flight director varient
            length = 55
            # need scale factor
            FDpitch_diff = pitch - FDpitch
            FDbank_diff = bank - FDbank
            # Limit Max of bank diff to 30 degrees
            bank_limit = 30.0
            if FDbank_diff > bank_limit:
                FDbank_diff = bank_limit
            elif FDbank_diff < -bank_limit:
                FDbank_diff = -bank_limit
            # Limit Max pitch diff to 20 degrees
            pitch_limit = 12.5
            if FDpitch_diff > pitch_limit:
                FDpitch_diff = pitch_limit
            elif FDpitch_diff < -pitch_limit:
                FDpitch_diff = -pitch_limit
            pitch_scale = -100 / pitch_limit
            bank_scale = -45 / bank_limit
            # Scale distances to max for max deflection
            FDpitch_diff *= pitch_scale
            FDbank_diff *= bank_scale
            GL.glColor(guage.purple)
            GL.glLineWidth(4.0)
            GL.glBegin(GL.GL_LINES)
            GL.glVertex2f(-length, -FDpitch_diff)
            GL.glVertex2f(length, -FDpitch_diff)
            GL.glVertex2f(-FDbank_diff, length)
            GL.glVertex2f(-FDbank_diff, -length)
            GL.glEnd()

        def Flight_Director_V(self, bank, FDbank, pitch, FDpitch):  # Draw the flight director

            def draw_V(side):
                GL.glBegin(GL.GL_LINE_STRIP)
                GL.glVertex2f(side * 10, -2)  # Flight director stars offset from center
                GL.glVertex2f(side * 85, -32.0)
                GL.glVertex2f(side * 100, -22.0)
                GL.glVertex2f(side * 10, -2)  # slope is 22/100
                GL.glEnd()
                GL.glBegin(GL.GL_LINE_STRIP)
                GL.glVertex2f(side * 100, -22.0)
                GL.glVertex2f(side * 100, -40.0)
                GL.glVertex2f(side * 85, -32.0)
                GL.glEnd()
            FDbank_diff = bank - FDbank
            FDpitch_diff = pitch - FDpitch
            # FDbank_diff = - FDbank
            # FDpitch_diff = - FDpitch
            pixel_per_degree = 7.25
            # FDpitch_diff = pitch - FDpitch
            # make sure pitch differeance isn't grater than 10 degrees, so FD always is visible
            if FDpitch_diff > 10:
                FDpitch_diff = 10
            elif FDpitch_diff < -10:
                FDpitch_diff = -10
            if FDbank_diff > 30:
                FDbank_diff = 30
            elif FDbank_diff < -30:
                FDbank_diff = -30
            GL.glPushMatrix()
            GL.glRotate(-FDbank_diff, 0.0, 0.0, 1.0)
            # glRotate(-FDbank, 0.0, 0.0, 1.0)
            GL.glPushMatrix()
            GL.glTranslatef(0.0, (FDpitch_diff) * pixel_per_degree, 0.0)  # Pitch
            GL.glColor(guage.purple)
            GL.glLineWidth(3.0)
            draw_V(1)
            draw_V(-1)
            GL.glPopMatrix()
            GL.glPopMatrix()

        def Static_Triangle(self):  # Static Triangle and Marks on top of Atitude

            def bank_ticks(dir):

                def short():
                    GL.glBegin(GL.GL_LINES)
                    GL.glVertex2f(0.0, radius + 12.0)
                    GL.glVertex2f(0.0, radius)
                    GL.glEnd()

                def long():
                    GL.glBegin(GL.GL_LINES)
                    GL.glVertex2f(0.0, radius)
                    GL.glVertex2f(0.0, radius + 25.0)
                    GL.glEnd()

                def triang():
                    size = 5.0
                    GL.glBegin(GL.GL_LINE_LOOP)
                    GL.glVertex2f(0.0, radius)
                    GL.glVertex2f(size, radius + size * 2)
                    GL.glVertex2f(-size, radius + size * 2)
                    GL.glEnd()

                GL.glPushMatrix()
                GL.glRotatef(dir * 10.0, 0.0, 0.0, 1.0)
                short()
                GL.glRotatef(dir * 10.0, 0.0, 0.0, 1.0)
                short()
                GL.glRotatef(dir * 10.0, 0.0, 0.0, 1.0)
                long()
                GL.glRotatef(dir * 15.0, 0.0, 0.0, 1.0)
                triang()
                GL.glRotatef(dir * 15.0, 0.0, 0.0, 1.0)
                long()
                GL.glPopMatrix()

            radius = 120.0
            GL.glLineWidth(2.5)
            # Draw Solid Triangle
            GL.glColor3f(1.0, 1.0, 1.0)
            size = 8.0
            GL.glBegin(GL.GL_LINE_LOOP)
            GL.glVertex2f(0.0, radius)
            GL.glVertex2f(size, radius + size * 2)
            GL.glVertex2f(-size, radius + size * 2)
            GL.glEnd()
            bank_ticks(1)
            bank_ticks(-1)

        def Dynamic_Triangle(self, roll, turn_coord):  # Triangle that moves durning turn
            GL.glLineWidth(2.5)
            a = abs(roll)
            radius = 120.0
            size = 8.0

            # Draw Traingle
            if a >= 30:  # Bank Angle check turns yellow and goes solid
                GL.glColor(guage.yellow)
                GL.glBegin(GL.GL_POLYGON)
            else:
                GL.glColor(guage.white)
                GL.glBegin(GL.GL_LINE_LOOP)
            # Draw actually traingle
            GL.glVertex2f(0.0, radius)
            GL.glVertex2f(size, radius - size * 2)
            GL.glVertex2f(-size, radius - size * 2)
            GL.glEnd()
            # Draw rectangle below, (This also acts as turn coordinator)
            top = radius - size * 2 - 1.0
            x_offset = (size * 2) * (turn_coord / 127.0)  # via trun coordinator move rectangel left or right
            # Draw vertex of rectangle
            GL.glBegin(GL.GL_LINE_LOOP)
            GL.glVertex2f(-size + x_offset, top)
            GL.glVertex2f(-size + x_offset, top - 7.0)
            GL.glVertex2f(size + x_offset, top - 7.0)
            GL.glVertex2f(size + x_offset, top)
            GL.glEnd()

        def Localizer(self, offset, x, y):

            def LOC_Diamond(h, w, dir):
                # dir direction of error either 1 or -1
                GL.glBegin(GL.GL_LINE_STRIP)
                w = w * dir
                GL.glVertex2f(0.0, -h)
                GL.glVertex2f(w, 0.0)
                GL.glVertex2f(0.0, h)
                GL.glEnd()

            w = 10
            lines_offset = 50
            lines_h = w
            scale = 0.8  # Make outer lines equal to 1 'degree"
            max = 90 * scale  # The limit, (arrow turns into 1/2 arrow)

            # Draws Glide_Slope if ILS Active
            # x,y is offset from attitude guage
            GL.glPushMatrix()
            GL.glTranslatef(x, y, 0.0)
            # Draw Center Line
            GL.glLineWidth(2.0)
            GL.glColor(guage.white)
            GL.glBegin(GL.GL_LINES)
            GL.glVertex2f(0.0, w-2)
            GL.glVertex2f(0.0, -(w-2))
            GL.glEnd()
            # Draw 2 Outer Lines
            GL.glLineWidth(3.0)
            GL.glBegin(GL.GL_LINES)
            GL.glVertex2f(lines_offset, -lines_h)
            GL.glVertex2f(lines_offset, lines_h)
            GL.glVertex2f(-lines_offset, -lines_h)
            GL.glVertex2f(-lines_offset, lines_h)
            GL.glEnd()
            GL.glLineWidth(2.0)
            # ------
            pos = -offset * scale  # invert needed.
            # Limit it to max deflection
            if pos >= max:
                pos = max
            elif pos <= -max:
                pos = -max
            GL.glTranslate(pos, 0.0, 0.0)
            GL.glColor(guage.green)
            GL.glLineWidth(3.0)
            if pos > -max:  # As long as not on bottom draw top arrow
                LOC_Diamond(w-2, w+2, 1)  # On Guage.py file
            if pos < max:  # AS long as not on top draw bottom arrow
                LOC_Diamond(w-2, w+2, -1)
            GL.glPopMatrix()

        def Markers(self, marker, frame_time, x, y):
            # if attitude.marker
            def draw_box(w, h, t):
                # Draw Rectangle
                GL.glBegin(GL.GL_LINE_LOOP)
                GL.glVertex2f(0, 0)
                GL.glVertex2f(w, 0)
                GL.glVertex2f(w, h)
                GL.glVertex2f(0, h)
                GL.glEnd()
                # Draw Text
                GL.glTranslatef(3, 3, 0)  # Move for text
                GL.glScalef(0.13, 0.13, 1)
                guage.glText(t, 105)
            w = 33
            h = 20
            GL.glPushMatrix()
            GL.glTranslatef(x, y, 0)
            GL.glLineWidth(2.0)
            if marker.value == marker.IM:
                marker.count += frame_time
                if marker.count > 0.2:
                    GL.glColor(guage.white)
                    draw_box(w, h, "IM")
                    if marker.count > 0:
                        marker.count -= 0.4
            elif marker.value == marker.MM:
                marker.count += frame_time
                if marker.count >= 1.2:
                    marker.count -= 1.2
                num = int(marker.count / 0.2)  # Get 0-4 if 0 or 2 flash off, else flash on
                if (num == 1) | (num > 2):  # If thoes numbers draw on
                    GL.glColor(guage.yellow)
                    draw_box(w, h, "MM")
            elif marker.value == marker.OM:
                marker.count += frame_time
                if marker.count > 0.5:
                    GL.glColor(guage.cyan)
                    # print frame_time
                    draw_box(w, h, "OM")
                    if marker.count > 1.0:
                        marker.count -= 1.0
            GL.glPopMatrix()

        def draw_declutter_arrow(self, w, h):
            GL.glBegin(GL.GL_LINE_STRIP)
            GL.glVertex2f(-w, h)
            GL.glVertex2f(0, 0)
            GL.glVertex2f(w, h)
            GL.glEnd()
            # Start of Draw_Atitude

        def draw(self, attitude, r_alt, frame_time, x, y, declutter):
            loc_active = False
            pixel_per_degree = 7.25
            pitch = -attitude.pitch.value
            roll = -attitude.bank.value
            guage_width = 310
            guage_heigth = 290
            # pitch = 0.0
            # roll = 10.0
            GL.glPushMatrix()
            GL.glTranslatef(x, y, 0.0)  # Moves to appropriate place
            guage.scissor(x - (guage_width // 2), y - (guage_heigth // 2), guage_width, guage_heigth)  # Only Draw in Atitude guage area
            GL.glEnable(GL.GL_SCISSOR_TEST)
            GL.glLineWidth(1.0)
            # glTranslatef(175.0, 300.0, 0.0) #Move to Guage
            GL.glPushMatrix()
            GL.glRotate(roll, 0.0, 0.0, 1.0)  # Rotate
            GL.glPushMatrix()
            GL.glTranslatef(0.0, pitch * -pixel_per_degree, 0.0)  # Pitch
            self.Grnd_Sky()
            # self.Horizon()
            self.Pitch_Marks(pitch, 2.5, pixel_per_degree, loc_active)  # Pitch and linewidth
            GL.glPopMatrix()  # Exit pitch
            self.Dynamic_Triangle(roll, attitude.turn_coord.value)
            GL.glPopMatrix()  # Exit Rotation
            self.Center_Mark()
            GL.glLineWidth(2.5)
            self.Static_Triangle()
            # Below is not drawn if in declutter mode
            if (not declutter):
                if attitude.FD_active.value:
                    #self.Flight_Director_V(attitude.bank.value, attitude.FD_bank.value, attitude.pitch.value, attitude.FD_pitch.value)
                    #self.Flight_Director_Lines(attitude.bank.value, attitude.FD_bank.value, attitude.pitch.value, attitude.FD_pitch.value)
                    self.Flight_Director(attitude.bank.value, attitude.FD_bank.value, attitude.pitch.value, attitude.FD_pitch.value)
                GL.glDisable(GL.GL_SCISSOR_TEST)
                self.Markers(attitude.marker, frame_time, 115, 148)  # Draw Outer, Middle, or Inner Marker
                # End if not declutter
            else:  # Since in declutter need to draw large red arrows to point towards horizon.
                GL.glPushMatrix()
                if pitch > 0:  # This is required so arrow always points towards horizon.
                    angle = roll + 180
                else:
                    angle = roll
                GL.glRotate(angle, 0.0, 0.0, 1.0)
                GL.glColor(guage.red)
                GL.glLineWidth(2.0)
                GL.glTranslatef(0.0, -10, 0.0)
                self.draw_declutter_arrow(40, -15 * pixel_per_degree -15)
                GL.glTranslatef(0.0, -15, 0.0)
                self.draw_declutter_arrow(30, -15 * pixel_per_degree)
                GL.glPopMatrix()
            GL.glPopMatrix()

    class Alt_Guage:

        def alt_bug(self, altitude, bug, y_center):
            # Draws putple lines for bug
            def line(y):
                GL.glVertex2f(52, y)
                GL.glVertex2f(94, y)

            units_apart = 13.0 / 20
            diff = altitude - bug
            if abs(diff) <= 300:  # If farther than that away no need to draw it.
                loc = y_center - (diff * units_apart)
                # Draw two purple lines above and below loc
                y1 = 16
                y2 = 19
                GL.glColor(guage.purple)
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
                    guage.glText(s, 90)
                    GL.glPopMatrix()

                tick_ten = tick_ten + 1
                loc = loc + 13.0

        def thousand_alt_bug(self, altitude, bug, y_center):
            # Draws putple lines for bug
            def line(y):
                GL.glVertex2f(21, y)
                GL.glVertex2f(37, y)

            units_apart = 0.13
            diff = altitude - bug
            if abs(diff) <= 1400:  # If farther than that away no need to draw it.
                loc = y_center - (diff * units_apart)
                # Draw two purple lines above and below loc
                y1 = 7
                y2 = 11
                GL.glColor(guage.purple)
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
            GL.glColor(guage.white)
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
            GL.glColor(guage.black)
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
                    guage.glText("%2d" % d, 90)
                # Check to see if near change in thousand above 900 feet
                alt_1000 = alt % 1000
                GL.glPushMatrix()
                if thou < 0:  # negative number no rolling
                    # Display yellow NEG in place of number
                    GL.glColor(guage.yellow)
                    GL.glDisable(GL.GL_SCISSOR_TEST)  # Turn off so text will show up
                    GL.glTranslatef(28.0, 8.0, 0.0)
                    GL.glScalef(0.10, 0.10, 1.0)
                    guage.glText("N", 0)
                    GL.glTranslatef(0.0, -120.0, 0.0)
                    guage.glText("E", 0)
                    GL.glTranslatef(0.0, -120.0, 0.0)
                    guage.glText("G", 0)
                elif (alt_1000 >= 970):  # Close to change in thousand will roll digits
                    loc = 30 - (1000 - alt_1000)  # / 1.0
                    if ((thou + 1) % 10) > 0:  # If both digits aren't changing then don't roll the 10k digit
                        if thou >= 10:  # This prevents 0 for being drawn in 10k digit spot
                            GL.glPushMatrix()  # Draw 10k digit in normal place
                            GL.glTranslatef(6.0, -10.0, 0.0)
                            GL.glScalef(0.18, 0.20, 1.0)
                            guage.glText("%d" % (thou // 10))
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
            guage.scissor(x-10, y-15, 80, 30)
            # Draw thousands digits
            thousands()

            GL.glPopMatrix()  # Altitude_disp

        def radar_disp(self, aag, x, y, notify):
            if (aag < 2500):  # If its above 2500 then don't display
                # Determine number to print on atitude display.
                num = aag
                if num >= 1000:  # Then do multiples of 50
                    # round  to multiples of 50.
                    num = (num + 25) // 50 * 50
                elif num >= 200:  # Do multiples of 10
                    num = (num + 5) // 10 * 10
                else:  # Do multiples of  5 (less than 200')
                    num = (num + 2.5) // 5 * 5
                # Display radar altitude
                if notify:  # If DH notify is on then change color to yellow else green (default color)
                    GL.glColor(guage.yellow)
                else:
                    GL.glColor(guage.green)
                GL.glLineWidth(2.0)
                GL.glPushMatrix()
                GL.glTranslatef(x, y, 0.0)  # Move to start of digits
                # Draw Numbers
                GL.glPushMatrix()
                GL.glScalef(0.16, 0.16, 1.0)
                guage.glText("%4d" % num, 90)
                GL.glPopMatrix()  # scale3f
                # Draw FT
                GL.glPushMatrix()
                GL.glTranslatef(65.0, -1.0, 0.0)
                GL.glScalef(0.12, 0.12, 1.0)
                guage.glText("FT")
                GL.glPopMatrix()  # translate
                GL.glPopMatrix()  # translate

        def radar_alt(self, aag, pixel_per_foot, y_cent, DH):  # Puts mark on tape that show ground.

            def foreground(aag, y_cent):  # Draw the correct white lines for foreground
                GL.glColor(guage.white)
                GL.glLineWidth(2.0)
                if aag > 1020:
                        h = 30
                else:
                        h = 12
                GL.glBegin(GL.GL_LINES)
                GL.glVertex2f(0.0, y_cent + h)
                GL.glVertex2f(20.0, y_cent + h)
                GL.glVertex2f(0.0, y_cent - h)
                GL.glVertex2f(20.0, y_cent - h)
                GL.glEnd()

            DH.notify = False  # Reset to false, will turn true is meets condition below
            if DH.visible:
                diff = aag-DH.bug
                if (diff <= 0) & (aag > 0):  # Turn on DH notifier if under DH and not on ground
                    DH.notify = True

        def alt_bug_text(self, bug, x, y):
            # This Displays Altitude Bug Setting
            GL.glColor(guage.purple)
            GL.glLineWidth(2.0)
            GL.glPushMatrix()
            GL.glTranslatef(x, y, 0.0)  # Move to start of digits
            GL.glScalef(0.16, 0.16, 1.0)
            guage.glText("%2d" % (bug // 1000), 95)
            GL.glScalef(0.85, 0.85, 1.0)  # Scale digits 85%
            guage.glText("%03d" % (bug % 1000), 95)
            GL.glPopMatrix()

        def alt_setting_disp(self, setting, x, y):
            # This Displays the Kollsman Window Setting
            GL.glPushMatrix()
            GL.glTranslate(x, y, 0)
            GL.glLineWidth(2.0)
            GL.glColor(guage.cyan)
            # Text out setting
            GL.glPushMatrix()
            GL.glScalef(0.14, 0.15, 0)
            # value += 0.01
            if setting < 35:
                guage.glText("%5.2f" % setting, 90)  # Round it to 2 places after decimal point 0.01 is slight correction. (Rouding Error?)
            else:
                guage.glText("%4d" % setting, 90)
            GL.glPopMatrix()  # Text 29.92
            # Display IN
            if setting < 35:  # Must by HG if under 35 HPA if not.
                GL.glTranslate(58, -1, 0)  # move for In display
                GL.glScalef(0.12, 0.12, 0)
                guage.glText("I N", 40)
            else:  # Must be HPA
                GL.glTranslate(53, -1, 0)
                GL.glScalef(0.12, 0.12, 0)
                guage.glText("HPA", 90)
            GL.glPopMatrix()

        def draw(self, altimeter, x, y, frame_time, declutter):
            y_center = 150.0
            GL.glPushMatrix()
            GL.glEnable(GL.GL_SCISSOR_TEST)
            guage.scissor(x, y, 100, 300)
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

    class VSI_Guage:

        def line(y1, y2):
            GL.glBegin(GL.GL_LINES)
            GL.glVertex2f(0.0, y1)
            GL.glVertex2f(0.0, y2)
            GL.glEnd()

        def marks(self, radius, small, med, large):

            def line(y1, y2):
                GL.glBegin(GL.GL_LINES)
                GL.glVertex2f(0.0, y1)
                GL.glVertex2f(0.0, y2)
                GL.glEnd()

            def text(x, y, s):
                GL.glPushMatrix()
                GL.glTranslatef(x, y - 6.0, 0.0)
                GL.glScalef(0.13, 0.13, 0.0)
                guage.glText(s)
                GL.glPopMatrix()

            # Set up lists with degree marks
            a = [large] * 3 + [small] * 4 + [med] + [small] * 4
            size = a + [large] + a[::-1]  # Above + large at 0 + reverse of above
            # Now Degrees to rotate
            rot = [15] * 2 + [6] * 20 + [15] * 3
            GL.glColor(guage.white)
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
            # Done determining angle
            # Draw Pointer
            # angle =0
            GL.glColor(guage.green)
            GL.glLineWidth(2.0)
            GL.glPushMatrix()
            GL.glRotate(angle, 0.0, 0.0, 1.0)
            GL.glTranslatef(-radius + 10.0, 0.0, 0.0)
            # Draw line and arrow
            GL.glBegin(GL.GL_LINES)
            GL.glVertex2f(40.0, 0.0)
            GL.glVertex2f(0.0, 0.0)
            GL.glEnd()
            GL.glBegin(GL.GL_POLYGON)
            GL.glVertex2f(0.0, 0.0)
            GL.glVertex2f(30.0, 5.0)
            GL.glVertex2f(30.0, -5.0)
            GL.glEnd()
            GL.glPopMatrix()

        def text(self, VS):
            # Draw text in center of guage
            GL.glColor(guage.green)
            GL.glPushMatrix()
            GL.glTranslate(-18.0, -6.0, 0.0)
            GL.glScalef(0.13, 0.13, 0.0)
            value = round(abs(VS / 1000.0), 1)
            if value >= 10:
                guage.glText("%2.0f" % value)
            else:
                guage.glText("%2.1f" % value)
            GL.glPopMatrix()

        def draw(self, x, y, radius, VS):
            GL.glPushMatrix()
            GL.glTranslate(x, y, 0.0)
            self.marks(radius, 5, 10, 15)
            self.pointer(radius, VS)
            self.text(VS)
            GL.glPopMatrix()

    class HSI_Guage:
        def Heading_Ticks(self, radius, heading):

            def HSI_Text(i):  # Returns text equivelent of tick mark
                if i == 0:
                    return "N"
                elif i == 9:
                    return "E"
                elif i == 18:
                    return "S"
                elif i == 27:
                    return "W"
                else:
                    return str(i)

            GL.glPushMatrix()
            GL.glRotate(heading, 0.0, 0.0, 1.0)
            GL.glLineWidth(2.0)
            GL.glColor(guage.white)
            for i in range(0, 36):  # Draw tick ever 10 degrees
                # Draw big tick
                GL.glBegin(GL.GL_LINES)
                GL.glVertex2f(0.0, radius)
                GL.glVertex2f(0.0, radius - 20.0)
                GL.glEnd()
                # Draw Number
                if (i % 3) == 0:  # Check to see if multiple of 3
                    GL.glPushMatrix()
                    c = HSI_Text(i)
                    if len(c) == 2:  # Two digits
                        GL.glTranslate(-6.0, 0.0, 0.0)
                    GL.glTranslate(-6.0, radius - 40.0, 0.0)
                    GL.glScalef(0.15, 0.15, 1.0)
                    guage.glText(HSI_Text(i))
                    GL.glPopMatrix()
                GL.glRotate(-5.0, 0.0, 0.0, 1.0)  # Rotate 5 degrees
                # Draw Small tick
                GL.glBegin(GL.GL_LINES)
                GL.glVertex2f(0.0, radius)
                GL.glVertex2f(0.0, radius - 15)
                GL.glEnd()
                GL.glRotate(-5.0, 0.0, 0.0, 1.0)  # Rotate 5 degrees
            GL.glPopMatrix()

        def marks(self, radius):
            # Put all marks around HSI 3 Traingles and 2 lines
            def triangle(radius, w, h):
                GL.glPushMatrix()
                GL.glTranslate(0.0, radius, 0.0)
                GL.glBegin(GL.GL_LINE_LOOP)
                GL.glVertex2f(0.0, 0.0)
                GL.glVertex2f(-w, h)
                GL.glVertex2f(w, h)
                GL.glEnd()
                GL.glPopMatrix()

            def line(radius, h):
                GL.glPushMatrix()
                GL.glTranslate(0.0, radius, 0.0)
                GL.glBegin(GL.GL_LINES)
                GL.glVertex2f(0, 0)
                GL.glVertex2f(0, h)
                GL.glEnd()
                GL.glPopMatrix()

            GL.glLineWidth(2.0)
            GL.glColor(guage.white)
            GL.glPushMatrix()
            # 90 Degree Line
            GL.glRotate(-90.0, 0.0, 0, 1.0)
            line(radius + 5, 15)
            # 45 Degree Smaller Triangle
            GL.glRotate(45.0, 0.0, 0, 1.0)
            triangle(radius + 2, 5, 8)
            # Top Large Triangle
            GL.glRotate(45.0, 0, 0, 1.0)
            triangle(radius - 2, 9, 15)
            # 45 Degree Smaller Triangle
            GL.glRotate(45.0, 0.0, 0, 1.0)
            triangle(radius + 2, 5, 8)
            # 90 Degree Line
            GL.glRotate(45.0, 0.0, 0, 1.0)
            line(radius + 5, 15)
            GL.glPopMatrix()

        def Plane_Figure(self):
            GL.glLineWidth(3.0)
            GL.glBegin(GL.GL_LINES)
            # Fuesalage
            GL.glVertex2f(0.0, 12.0)
            GL.glVertex2f(0.0, -35.0)
            # Wing (Note: Wing is located slightly below center (3pixeles))
            GL.glVertex2f(-25.0, -1.0)
            GL.glVertex2f(25.0, -1.0)
            # Tail
            GL.glVertex2f(-13.0, -28.0)
            GL.glVertex2f(13.0, -28.0)
            GL.glEnd()

        def magnetic_track(self, radius, HSI):
            diff = HSI.Mag_Heading.value - HSI.Mag_Track.value
            GL.glPushMatrix()
            GL.glRotate(diff, 0, 0, 1.0)
            GL.glTranslate(0, radius-12, 0)
            GL.glColor(guage.green)
            guage.glCircle(6, 10)
            GL.glPopMatrix()

        def heading_bug(self, radius, HSI, frame_time):
            # radius = radius of guage, mag = mag heading of plane bug = heading bug value
            # draw_line True if you want purple line drawn from center to bug, (Used when bug's value is changed)
            def bug_polygon():
                GL.glColor(guage.purple)
                GL.glLineWidth(2.0)
                GL.glBegin(GL.GL_LINE_LOOP)
                GL.glVertex2f(0.0, 0.0)
                GL.glVertex2f(10.0, 8.0)
                GL.glVertex2f(10.0, 15.0)
                GL.glVertex2f(0.0, 15.0)
                GL.glVertex2f(0.0, -15.0)
                GL.glVertex2f(10.0, -15.0)
                GL.glVertex2f(10.0, -8.0)
                GL.glEnd()

            def text(x, y, bug):
                GL.glPushMatrix()
                GL.glTranslatef(x, y, 0)
                GL.glScalef(0.15, 0.15, 1)
                guage.glText("HDG %03d" % bug, 90)
                GL.glPopMatrix()

            # Check for change in heading bug, reset timer is changed
            # if HSI.Heading_Bug.value != HSI.Heading_Bug_prev:
            #    HSI.Heading_Bug_Timer = 5.0 / frame_time #Calculate number of frames for 5 seconds
            #    HSI.Heading_Bug_prev = HSI.Heading_Bug.value
            # diff = is difference between current heading and bug
            diff = HSI.Mag_Heading.value - HSI.Heading_Bug.value
            if diff < 0:
                diff += 360  # Make sure diff is between 0 and 360
            GL.glPushMatrix()
            GL.glRotate(diff + 90, 0, 0, 1)  # 90 degree offset is since bug_polygon above is rotated
            if (HSI.Heading_Bug_Timer > guage.globaltime.value):  # Enable drawing of line
                draw_line = True
                # HSI.Heading_Bug_Timer -=1
            else:
                draw_line = False
            # Draw dotted line from center to heading bug
            if (draw_line) or (130 < diff < 230):
                # If diff is between 130 and 230 then line needs to be drawn because spedbug is notshown
                GL.glColor(guage.purple)
                GL.glLineWidth(2.0)
                start = 15.0
                num = 12
                step = (radius - start) / num
                # glLineStipple(1, 0x00FF) Note: Line stipple didn't look right
                # glEnable(GL_LINE_STIPPLE)
                GL.glBegin(GL.GL_LINES)
                for i in range(num / 2):
                    GL.glVertex2f(start, 0.0)
                    start += step
                    GL.glVertex2f(start, 0.0)
                    start += step
                GL.glEnd()
                # glDisable(GL_LINE_STIPPLE)
            # Draw bug_polygon

            GL.glTranslatef(radius - 3, 0.0, 0.0)
            bug_polygon()
            GL.glPopMatrix()
            if draw_line:
                text(-150, 157, HSI.Heading_Bug.value)

        def draw(self, x, y, aircraft, declutter):
            radius = 145
            GL.glPushMatrix()
            GL.glTranslate(x, y, 0.0)
            guage.scissor(x - 300, y - 80, 600, 440)
            GL.glEnable(GL.GL_SCISSOR_TEST)
            GL.glColor(guage.white)
            self.Plane_Figure()
            self.Heading_Ticks(radius, aircraft.HSI.Mag_Heading.value)
            self.marks(radius)
            if not declutter:
                # self.magnetic_track(radius, aircraft.HSI)
                self.heading_bug(radius, aircraft.HSI, aircraft.frame_time)
                GL.glDisable(GL.GL_SCISSOR_TEST)
            GL.glPopMatrix()

    def __init__(self):
        self.name = "PFD"
        self.speed = self.Speed_Guage()
        self.artifical_horizon = self.Attitude_Guage()
        self.alt_g = self.Alt_Guage()
        self.HSI = self.HSI_Guage()
        self.VSI = self.VSI_Guage()

    def draw(self, aircraft, x, y):  # x,y is the xy cordinates of center of PFD guage
        y += 445  # Fine tune position
        x -= 6
        declutter = aircraft.declutter.active
        # print aircraft.autopilot.ias_bug
        # print "Speed", time.time()
        self.speed.draw(aircraft.airspeed, aircraft.onground.value, x - 248, y - 140, declutter)
        # print "A_Horizon", time.time()
        self.artifical_horizon.draw(aircraft.attitude, aircraft.altimeter.absolute, aircraft.frame_time, x + 0, y + 0, declutter)
        # print "Altimeter", time.time()
        self.alt_g.draw(aircraft.altimeter, x + 155, y - 150, aircraft.frame_time, declutter)
        # print "HSI", time.time()
        self.HSI.draw(x, y-330, aircraft, declutter)  # Just send the whole aircraft object, as lot of data drawn on HSI
        self.VSI.draw(x + 240, y-305, 70, aircraft.VSI.value)
