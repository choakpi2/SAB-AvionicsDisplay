import socket
import csv
import time
import config
from guage import *
import keyboard
import math
import sounds
import formula
import pickle
from PFDND_data import *
from EICAS_data import *

#def __init__(self):
    #self.data = data()

class data(object):

    def __init__(self, PFD):
        self.global_time = 0.0 #Used for timing reasons. 
        self.prev_time = 0.0 #Used for delta time calc in comp function.
        self.count = 0
        self.comp_time = 0.0 #Used for timer for comp_second function.
        self.quit_flag = False #If True then RJGlass will exit

        self.aileron_pos= data_obj(0)
        self.elev_trim = data_obj(0)
        self.ias_bug = 220 #Integer

        #From EICAS_data
        self.flaps = flaps_c()
        self.fuel = fuel_c()
        self.gear = Gear_c()
        self.brakes = Brakes_c()
        self.trim = Trim_c()
        self.APU = APU_c()
        self.onground = data_obj(1)
        self.total_weight = data_obj(0)
        self.OAT = data_obj(25.0)
        self.Eng_1 = Engine_c(1)
        self.Eng_2 = Engine_c(2)
        
        #From PFDND_data
        self.attitude = attitude_c()
        self.HSI = HSI_c()
        self.NAV = NAV_c()
        self.ND = ND_c()
        self.VSI = data_obj(-800)
        self.altimeter = altimeter_c()
        self.declutter = declutter_c()
        self.airspeed = airspeed_c()


        self.Latitude = data_obj(math.radians(32.36))
        self.Longitude = data_obj(math.radians(-91.7))
        
        #PICKLE        
        self.PFD_pickle = PFD_pickle_c(self)
        self.EICAS_pickle = EICAS_pickle_c(self)
        
        
        self.clock = time.time() 
        self.count2 = 0 #counter used to determine clock cycle
        self.frame_time = 0.01 #Time between frames. 1 / frame_time = FPS (frames per second)
        self.nodata = False
        self.nodata_time = 0
  
        #Initialize sounds
        self.callouts = sounds.init_callouts(True)
        #Dynamic variable for testing
        self.dynamic_value = 0
        self.dynamic_step = 1
        
        
    def quit(self):
        self.quit_flag = True
      
    def comp_frame_time(self, i):
        if self.count2 >= i:
            t = globaltime.value
            self.frame_time = (t - self.clock) / self.count2
            self.clock = t
            self.count2 = 0
        #print self.frame_time
        else:
            self.count2+=1

    def get_PFD_data(self):
        return pickle.dumps(self.PFD_pickle, -1)
        
    #comp() -- this method simply makes sure that the values of aircraft object
    #remain in the correct range, that is it does not exceed the indicators etc
    def comp(self, test=False):
        #Test is true, if RJGlass is in test mode.
        self.global_time = globaltime.value

        #Computer delta_t = Time between last comp and this one
        delta_t = self.global_time - self.prev_time
        if delta_t > 0.1: delta_t = 0.1 #Limit to .1 sec (incase of hickup)
        self.prev_time = self.global_time
        
        #Computation section, main one for data that is updated every frame.
        #self.count+=1
        self.comp_time+= delta_t

        if self.comp_time > 1.0:
            self.comp_time -= 1.0
            #Do low priority stuff
            self.brakes.comp(self)
            self.comp_second()
            
        self.airspeed.comp()
        self.Eng_1.comp()
        self.Eng_2.comp()
        self.flaps.comp()
        self.gear.comp()
        self.fuel.comp()
        self.APU.comp(delta_t,self.global_time)
        self.trim.comp(self.onground)
        
        EICAS_comp(self)
        self.declutter.comp(self.attitude.pitch.value, self.attitude.bank.value)
        if self.altimeter.indicated.value <-1000: self.altimeter.indicated.value = -1000
        self.attitude.GS = self.NAV.active.GSI.value
        self.comp_frame_time(20)
        self.airspeed.comp_IAS_accel(self.airspeed, self.frame_time)
        
        #Check to see if IAS speed trend (Pink line) visible
        if self.airspeed.trend_visible: #If on check if speed <105kts
            if self.airspeed.IAS.value <105:
                self.airspeed.trend_visible = False
        else: #If off check for H>20ft
            if self.altimeter.absolute.adjusted > 20:
                self.airspeed.trend_visible = True
        
        self.HSI.True_Heading = Check_360(self.HSI.Mag_Heading.value + self.HSI.Mag_Variation.value)
        #self.HSI.True_Heading = Check_360(self.HSI.Mag_Heading.value + 0)
        #print "RA ", self.altimeter.absolute.value
        self.altimeter.absolute.adjusted = self.altimeter.absolute.value - 7
        #Mach visible
        if self.airspeed.Mach.value < 0.4:
            self.airspeed.Mach.active = False
        elif self.airspeed.Mach.value >=0.45:
            self.airspeed.Mach.active = True
        #Check for altitude callouts
        #if self.altimeter.MDA.changed or self.altimeter.DH.changed: #If they changed then update minimums
        if self.altimeter.absolute.adjusted < 2500: #If under 2500 AGL then check altitude callouts
            self.callouts.update_minimums(self.altimeter.MDA, self.altimeter.DH, self.altimeter.absolute.adjusted, self.altimeter.indicated.value)
            self.callouts.check(self.altimeter.absolute.adjusted, self.altimeter.indicated.value)
        
    def comp_second(self):
        temp = self.flaps.handle.value
        if temp <=5: 
            self.airspeed.maxspeed = config.VNE_flaps[temp]
            self.airspeed.minspeed = config.VS_flaps[temp] * 1.06
            self.airspeed.lowspeed = config.VS_flaps[temp] * 1.265
        if self.gear.handle.value:
                if self.airspeed.maxspeed> config.Gear_speed_limit:
                    self.airspeed.maxspeed = config.Gear_speed_limit
        self.ND.dis_traveled.calc(self.Latitude.value, self.Longitude.value)
    
    def get_mode_func(self, mode, right_screen, left_screen):
        if mode==config.TEST: 
            mode_func = self.test
        else:
            print "ERROR: Mode in config file is not defined"
        return mode_func

    def test(self):
        self.attitude.bank.value += 0.0005
        self.attitude.pitch.value += 0.005
        self.gear.Left.position.value = 0.0
        self.gear.Nose.position.value = 0.0
        self.gear.Right.position.value = 0.0
        self.fuel.left.gal.value -= 0.1
        self.comp(True) #Set true to tell self.comp, RJGlass is in test mode.
        self.HSI.Mag_Heading.value += 1
        self.VSI.value = 1000
        self.Eng_1.N2.value = 65.1
        self.Eng_2.N2.value = 65.5
        self.NAV.VOR1.OBS.value = 112
        if self.count >=30:
            self.altimeter.indicated.value = self.altimeter.indicated.value + 7
            self.NAV.VOR1.hasGS.value = False
            self.count =0
        self.count +=1
        self.airspeed.IAS.value += 1
           
