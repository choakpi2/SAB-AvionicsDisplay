import sys
import os
from OpenGL import GL
from OpenGL import GLU
from OpenGL import GLUT
import pygame
from pygame import locals
from pygame import image
import time
import guage

# This is code to import config file (config.py)
try:
    import config
except ImportError:
    # We're in a py2exe, so we'll append an element to the (one element)
    # sys.path which points to Library.zip, to the directory that contai
    # Library.zip, allowing us to import config.py
    # Adds one level up from the Library.zip directory to the path, so import will go forward
    sys.path.append(os.path.split(sys.path[0])[0])
    import config


class screen_c(object):
    # This controls what is in each screen.
    def __init__(self, x, guage_list):
        self.guage_list = guage_list  # list of guages to cycle through
        self.guage_index = 0
        self.x = x
        self.y = 20
        self.width = 512
        self.heigth = 768

    def cycle(self):
        self.guage_index += 1
        if self.guage_index >= len(self.guage_list):
            self.guage_index = 0

    def cycle_reverse(self):
        self.guage_index -= 1
        if self.guage_index < 0:
            self.guage_index = len(self.guage_list) - 1

    def draw(self, aircraft):
        self.guage_active = self.guage_list[self.guage_index]
        self.guage_active.draw(aircraft, self.x, self.y)


def InitPyGame():
    GLUT.glutInit(())
    pygame.init()
    if config.full_screen:
        s = pygame.display.set_mode((1024, 768), locals.DOUBLEBUF | locals.OPENGL | locals.FULLSCREEN)
    else:
        s = pygame.display.set_mode((1024, 768), locals.DOUBLEBUF | locals.OPENGL)
    return s


def InitView(smooth, width, heigth):
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    GL.glLoadIdentity()
    GL.glOrtho(0, width, 0.0, heigth, -1.0, 1.0)

    x_s = width/1024.0
    y_s = heigth/768.0

    GL.glScalef(x_s, y_s, 1.0)
    guage.scissor.x_s = x_s
    guage.scissor.y_s = y_s
    if smooth:
        # Enable Smoothing Antianalising
        GL.glEnable(GL.GL_LINE_SMOOTH)
        GL.glEnable(GL.GL_BLEND)
        # glBlendFunc(GL_SRC_ALPHA, GL_ZERO)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glHint(GL.GL_LINE_SMOOTH_HINT, GL.GL_DONT_CARE)


def DisplaySplash(filename, delay, window_x, window_y):
    # Display needs to be initialized first.
    i = image.load(filename)
    splash_image = guage.bitmap_image(i)
    # Determine the x and y coords to put in center of screen.
    splash_x = (window_x / 2) - (splash_image.w/2)
    splash_y = (window_y / 2) - (splash_image.h/2)
    GL.glRasterPos3f(splash_x, splash_y, 0)
    GL.glDrawPixels(splash_image.w, splash_image.h, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, splash_image.tostring)
    pygame.display.flip()
    time.sleep(delay)


def DrawWindow(left_screen):

    def draw_nodata(x, y):  # Draw no data text on screen.
        GL.glColor(guage.red)
        GL.glLineWidth(5.0)
        GL.glPushMatrix()
        GL.glTranslatef(x, y, 0)
        GL.glScalef(0.4, 0.4, 1.0)
        guage.glText("NO SIM DATA", 100)
        GL.glPopMatrix()

    global count
    left_screen.draw(aircraft_data)
    # right_screen.draw(aircraft_data)
    GL.glDisable(GL.GL_SCISSOR_TEST)  # Disable any scissoring.
    guage.draw_FPS(512, 740, aircraft_data.frame_time)
    # If Nodata is coming from Flight Sim, show on screen
    if aircraft_data.nodata:
        draw_nodata(50, 500)
    count = count + 1  # Used for FPS calc


def main(mode):
    # global window
    global starttime
    global count

    # Start Event Processing Engine
    starttime = time.time()  # Used for FPS (Frame Per Second) Calculation
    screen = screen_c(512, [PFD, EICAS1])

    # SETUP KEYBOARD
    keys = keyboard.keylist(aircraft_data, screen)

    # LOAD GUAGE TEXTURES
    EICAS1.load_texture()

    while not (aircraft_data.quit_flag):
        # CLEAR SCREEN
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # UPDATE GLOBALTIME
        aircraft_data.globaltime = time.time()
        guage.globaltime.update(time.time())

        # DRAW WINDOW
        DrawWindow(screen)

        # UPDATE SCREEN
        pygame.display.flip()
        aircraft_data.test()

        # CHECK KEYPRESS
        keys.check_events(pygame.event.get(), guage.globaltime.value)

# ===========================================================================
#  Main program
# ===========================================================================
global count
# global scissor
guage.scissor.x_s = 1.1  # Just assign these, will be reset later.
guage.scissor.y_s = 1.0
count = 0
x = config.window_x
y = config.window_y

# INITIALIZE WINDOW
InitPyGame()
InitView(True, x, y)

# LOAD SPLASH SCREEN
if config.splash:
    DisplaySplash(config.splash_filename, config.splash_delay, x, y)

# IMPORT REST OF MODULES WHILE SPLASH DISPLAYED
import PFD_mod
import EICAS1_mod
import aircraft
import keyboard

# INITIALIZE GUAGES
PFD = PFD_mod.PFD_Guage()
EICAS1 = EICAS1_mod.EICAS1_guage()
aircraft_data = aircraft.data(PFD)

# RUN MAIN USING CONFIG.PY SETTINGS
print "Main Loop"
main(config.mode)

# ===========================================================================
#  Shuting Down
# ===========================================================================
# Close LogFile
guage.datafile.close()
# Close pygame mixer
pygame.mixer.quit()
# Print average Frames per second on shutdown
print "FPS ", count / (time.time() - starttime)
