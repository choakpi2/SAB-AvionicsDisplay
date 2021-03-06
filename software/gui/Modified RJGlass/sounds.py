#!/usr/bin/env python
# ----------------------------------------------------------
# Sounds MODULE for GlassCockpit procject RJGlass
# ----------------------------------------------------------
# This module will take the keys that are pressed on the keyboard and take appropriate action.
#
# Copyright 2007 Michael LaBrie
#
#    This file is part of RJGlass.
#
#    RJGlass is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.

#   RJGlass is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ---------------------------------------------------------------


import pygame
import os
import config
import time
import guage


class callouts_c(object):

    def __init__(self):
        self.channel = pygame.mixer.find_channel()
        if self.channel is None:
            print "Error, Initialize channel for callouts"
        self.list = []
        self.counter = 0  # Due to MDA, update_minimums needs to be checked every few seconds

    def add(self, name, filename, alt):
        self.list.append(callout_sound_c(name, filename, alt))

    def check(self, indicated_altitude):
        temp_time = guage.globaltime.value  # time for this function
        for callouts in self.list:
            alt = indicated_altitude
            if callouts.played is False:
                if alt <= callouts.altitude:
                    if callouts.active:
                        self.channel.queue(callouts.sound)
                    callouts.played = True  # Weather sound active or not, it still keeps track if airplane passed altitude
                    callouts.time_played = temp_time
            else:  # else not played, meaning played and not reset yet
                if alt > callouts.altitude + 100:  # 100' buffer, so you must be 100 above altitude before it calls it again
                    if temp_time - callouts.time_played > 120:  # 120seconds
                        callouts.played = False  # Sound is reset to played again


class callout_sound_c(callouts_c):
    def __init__(self, name, filename, altitude):
        self.name = name
        self.altitude = altitude
        self.played = True  # Used to see if has played  set to true so doesn't play on start of program
        self.active = True
        self.time_played = 0

        # Get sound directory
        cwd = os.getcwd()
        dir = os.path.join(cwd, config.sound_directory)
        filepath = os.path.join(dir, filename)
        self.sound = pygame.mixer.Sound(filepath)

    def reset(self):
        self.played = False


def init_callouts(extra_callouts):
    callouts = callouts_c()
    # Keep MDA and DH in same position, has update_minimums assumes MDA is index 0 DH is index 1
    callouts.add('500', '500.wav', 500)
    if extra_callouts:
        callouts.add('400', '400.wav', 400)
        callouts.add('300', '300.wav', 300)
        callouts.add('200', '200.wav', 200)
    callouts.add('100', '100.wav', 100)
    callouts.add('50', '50.wav', 50)
    callouts.add('40', '40.wav', 40)
    callouts.add('30', '30.wav', 30)
    callouts.add('20', '20.wav', 20)
    callouts.add('10', '10.wav', 10)
    return callouts

# def close_sounds():
# pygame.mixer.quit()
# Do every time
# Initialize mixer
pygame.mixer.init()

if __name__ == '__main__':

    callouts = callouts_c()
    callouts.add('500.wav', 500, 200)
    callouts.add('400.wav', 400, 200)
    callouts.add('300.wav', 300, 200)
    callouts.add('200.wav', 200, 200)
    callouts.add('100.wav', 100, 200)
    callouts.add('50.wav', 50, 200)
    callouts.add('40.wav', 40, 200)
    callouts.add('30.wav', 30, 200)
    callouts.add('20.wav', 20, 200)
    callouts.add('10.wav', 10, 200)
    callouts.add('Minimums.wav', 200, 200)

    for radar_alt in range(700, 1, -1):
        callouts.check(radar_alt)
        print radar_alt
        time.sleep(0.025)

    time.sleep(2)
    pygame.mixer.quit()
