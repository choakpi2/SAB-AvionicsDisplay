from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import EICAS_data
import time
import sys, os
import math, pickle
import config

#This is code to import config file (config.py)
try:
    import config
except ImportError:
    # We're in a py2exe, so we'll append an element to the (one element) 
    # sys.path which points to Library.zip, to the directory that contains 
    # Library.zip, allowing us to import config.py
    # Adds one level up from the Library.zip directory to the path, so import will go forward
    sys.path.append(os.path.split(sys.path[0])[0])
    import config

from guage import * #All add on guage functions colors etc.


class EICAS1_guage(object):
    
    
    class Flaps_Bar_c(object):
     
        def __init__(self, x,y,width):
            self.x = x
            self.y = y
            self.width = width
            self.tick_heigth = 8
            self.tick_width = 2
   
        def draw_ticks(self, flap_pos, cur_guage_pos):
            glColor(white)
            glLineWidth(2.0)
            w = self.tick_width
            h = self.tick_heigth
            for i in flap_pos:
                cen_x = self.width * i
                glBegin(GL_LINE_LOOP)
                glVertex2f(cen_x - w, h)
                glVertex2f(cen_x - w, -h)
                glVertex2f(cen_x + w, -h)
                glVertex2f(cen_x + w, h)
                glEnd()
    
        def draw_bar(self, guage_pos):
            glColor(green)
            glLineWidth(10.0)
            if guage_pos > 0.0:
                glBegin(GL_LINE_STRIP)
                glVertex2f(-1,0)
                glVertex2f((1+ self.width) * guage_pos , 0)
                glEnd()
            
        def draw(self, flaps):
            glPushMatrix()
            glTranslatef(self.x, self.y, 0)
            self.draw_bar(flaps.guage_pos)
            self.draw_ticks(flaps.guage_flap_pos, flaps.guage_pos)
            glPopMatrix()
            
   
    class Flaps_Text_c(object):
        
        def __init__(self, x,y, size= 0.11):
            self.x = x
            self.y = y
            self.size = size
        
        def draw(self, flaps_deg):
            glPushMatrix()
            glTranslatef(self.x,self.y,0)
            glPushMatrix()
            glScalef(self.size,self.size,1.0)
            glColor(white)
            glText("FLAPS",95)
            glColor(green)
            glScalef(1.36,1.36,1.0)
            glText(" %2d" %flaps_deg, 95)
            glPopMatrix()
            glPopMatrix()
        
  
    class Gear_Disp(object):
     
        def __init__(self, x,y):
            self.x = x
            self.y = y
                    
        def draw(self,value):
            glPushMatrix()
            glTranslatef(self.x,self.y,0)
            #Three cases UP Down or Transition (Yellow cross hatch)
            if value == 0: #Gear up
                color = white
                text = "UP"
            elif value >= .99: #Gear down
                color = green
                text = "DN"
            else: #Gear in transition
                color = yellow
                text = "--"
            
            glColor(color)
            #Draw outer box
            w = 26
            h = 17
            glBegin(GL_LINE_LOOP)
            glVertex2f(-w,-h)
            glVertex2f(w,-h)
            glVertex2f(w,h)
            glVertex2f(-w,h)
            glEnd()
            #Draw Text
            if text!="--":
                glPushMatrix()
                glTranslatef(-17,-10,0)
                glScalef(0.2,0.2,1.0)
                glText(text,87)
                glPopMatrix()
            else: #Draw crosshatch
                glBegin(GL_LINES)
                glVertex2f(-w+2,-h)
                glVertex2f(4, h)
                glVertex2f(-4, -h)
                glVertex2f(w-2,h)
                glVertex2f(-w+12,h)
                glVertex2f(-w, h-15)
                glVertex2f(w-12,-h)
                glVertex2f(w, -h+15)
                glEnd()
            glPopMatrix()


    class Fuel_Qty_Disp(object):
     
        def __init__(self, x,y, text_size):
            self.x = x
            self.y = y
            self.size = text_size
            self.metric = config.use_metric_units
            
        def draw_fuel_qty_text(self,fuel_tank):            
            glColor(fuel_tank.EICAS_color)
            glText("%5d" %fuel_tank.EICAS_disp,95)    
            
        def draw(self, fuel_tank):        
            glPushMatrix()
            glTranslatef(self.x,self.y,0)
            glPushMatrix()
            glScalef(self.size,self.size,1.0)
            self.draw_fuel_qty_text(fuel_tank)
            glPopMatrix()
            glPopMatrix()
 

    class FanVib_Label_c(object):
        #Unique label with vertical and horizontal Words
        def __init__(self, x,y):
            self.x = x
            self.y = y
            
        def draw(self):
            glPushMatrix()
            glTranslatef(self.x, self.y, 0)
            glScalef(0.12, 0.12, 1.0)
            glColor(white)
            for c in "FAN":
                glText(c, 95)
                glTranslatef(-95, -155,0)
            glTranslatef(-97, -111, 0)
            glText("VIB", 95)
            glPopMatrix()
   

    class FF_Data_c(object):
     
        def __init__(self, x,y, format):
            self.x = x
            self.y = y
            self.text_format = format
            self.size = 0.15
   
        def draw(self, value):
            glPushMatrix()
            glTranslatef(self.x, self.y, 0)
            glScalef(self.size,self.size,1.0)
            glColor(green)
            glText(self.text_format %value, 95)
            glPopMatrix()
            
   
    class OilTemp_Data_c(object):
     
        def __init__(self, x,y, format, red, yellow):
            self.x = x
            self.y = y
            self.text_format = format
            self.red = red
            self.yellow = yellow
            self.size = 0.15
            
        def check_color(self,value):
            #Check appopriate color for OilTemp
            if value < self.yellow:
                glColor(green)
            elif value >= self.red:
                glColor(red)
            else:
                glColor(yellow)
                
        def draw(self, value):
            glPushMatrix()
            glTranslatef(self.x, self.y, 0)
            glScalef(self.size,self.size, 1.0)
            self.check_color(value)
            glText(self.text_format %value , 95)
            glPopMatrix()
            
   
    class OilPress_Data_c(object):
     
        def __init__(self, x,y, format, red, yellow):
            self.x = x
            self.y = y
            self.text_format = format
            self.red = red
            self.yellow = yellow
            self.size = 0.15
            
        def check_color(self,value):
            #Check appopriate color for OilTemp
            if value <= self.red:
                glColor(red)
            elif value <= self.yellow:
                glColor(green)
            else:
                glColor(yellow)
                
        def draw(self, value):
            glPushMatrix()
            glTranslatef(self.x, self.y, 0)
            glScalef(self.size,self.size, 1.0)
            self.check_color(value)
            glText(self.text_format %value , 95)
            glPopMatrix()
    

                
    class N1_bug_c(object):
    #This is only used for the bugs on N1, both circle in V.
        def __init__(self):
            self.active = False
            self.color = cyan
            self.caret = [[-3, -7],[0,0],[3, -7]]
            self.doughnut = List_Circle(5,8) 
                
        def draw(self, radius, angle):
            glColor(self.color)
            glPushMatrix()
            glRotate(-angle,0,0,1)
            glTranslatef(0,radius, 0)
            glBegin(GL_LINE_STRIP)
            Draw_List(self.caret)
            glEnd()
            glPopMatrix()

                    
    class Dial_Guage(object):
        
        class arcs_c(object):
            
            def __init__(self, color, start_angle=0, stop_angle=0 , list= []):
                self.color = color
                self.list = list
                self.start_angle = start_angle
                self.stop_angle = stop_angle
                if len(list) == 0:
                    self.active = False
                else:
                    self.active = True
                
            def within(self, angle):
                if (self.start_angle <= angle <= self.stop_angle):
                    return True
                else:
                    return False
            def draw(self):
                glColor(self.color)
                glBegin(GL_LINE_STRIP)
                Draw_List(self.list)
                glEnd()
                        
        def __init__(self, x,y, radius, min_angle, max_angle, min_guage, max_guage, min_display, max_display, text_format, line_arrow = False, flash_limit = None):
            self.x = x
            self.y = y
            self.text_x = 0
            self.text_y = 0
            self.max = max_guage
            self.min = min_guage
            if flash_limit != None:
                self.flash = flash_c(1,4)
                self.flash_limit = flash_limit
            else:
                self.flash = None
                
            self.max_display = max_display
            self.min_display = min_display
            self.angle_max = max_angle
            self.angle_min = min_angle
            self.green_arc = self.arcs_c(black) #Make arcs blank for now
            self.red_arc = self.arcs_c(black) 
            self.amber_arc = self.arcs_c(black)
            self.radius = radius
            self.tick_radius = radius - 7
            self.text_format = text_format
            self.bug = None #Only used on N1 Guage
            if line_arrow == True:
                self.draw_arrow = self.line_arrow
            else:
                self.draw_arrow = self.full_arrow
            
        def calc_angle(self, value):    
            if value < self.min:
                value = self.min
            elif value > self.max:
                value = self.max
            angle = (self.angle_max - self.angle_min)* (1.0 * value / (self.max-self.min) + self.min) + self.angle_min
            return angle
        
        def get_color(self, value):
            color = green
            if self.amber_arc.active:
                if self.amber_arc.within(value):
                    color = yellow
            if self.red_arc.active:
                if self.red_arc.within(value):
                    color = red
            return color
            
        def arc(self, color, segments, start_value, stop_value, start_tick, stop_tick):
            start_angle = self.calc_angle(start_value)
            stop_angle = self.calc_angle(stop_value)
            return self.arcs_c(color, start_angle, stop_angle, List_Circle(self.radius, segments, start_angle, stop_angle, start_tick, stop_tick, self.tick_radius))
        
        def full_arrow(self, angle):
            #Green Arrow
            glPushMatrix()
            #angle = self.angle_max * (1.0 * value / self.max) + 90
            #print self.angle_max, value, self.max, angle
            glRotatef(-angle, 0,0,1)
            arrow_w = 5.0
            arrow_h = self.radius - 7
            body_w = 2.0
            body_h = self.radius - 18
                        
            glLineWidth(2.0)
            glBegin(GL_LINE_STRIP)
            glVertex2f(body_w,0)
            glVertex2f(body_w,body_h)
            glVertex2f(arrow_w,body_h)
            glVertex2f(0,arrow_h)
            glVertex2f(-arrow_w,body_h)
            glVertex2f(-body_w, body_h)
            glVertex2f(-body_w, 0)
            glEnd()
            glPopMatrix()
            
        def line_arrow(self, angle):
            #Nice Line Arrow - For FAN VIB and Oil Pressure
            glPushMatrix()
            glRotate(-angle,0,0,1)
            glLineWidth(2.0)
            glBegin(GL_LINE_STRIP)
            glVertex2f(0,0)
            glVertex2f(0, self.radius - 7)
            glEnd()
            glPopMatrix()
            
        def draw_arc(self):
            self.green_arc.draw()
            self.red_arc.draw()
            self.amber_arc.draw()
    
        def draw_text(self, value):
            if self.text_format !="":
                if value> self.max_display:
                    value = self.max_display
                elif value < self.min_display:
                    value = self.min_display
                glPushMatrix()
                glTranslatef(self.text_x, self.text_y,0)
                #If no decimal point shit over slightly to right ex. ITT
                if "d" in self.text_format: 
                    glTranslatef(12,0,0)
                
                text = self.text_format %value
                glScalef(0.18,0.18,1.0)
                glText(text, 97)
                glPopMatrix()
        
        def check_flash(self, value):
            
            if self.flash == None:
                return False
            elif value >= self.flash_limit:
                if (self.flash.overflow == False) & (self.flash.active == False):
                    self.flash.start()
                return self.flash.flash()
            else:
                self.flash.stop()
                return False
            
        def draw(self, value, globaltime = 0, text= None):
            glLineWidth(2.0)
            angle = self.calc_angle(value)
            #if self.flash !=None:
            flash = self.check_flash(value)
                
            glPushMatrix()
            glTranslatef(self.x, self.y, 0.0)
            
            if self.bug != None:
                self.bug.draw(self.radius, self.calc_angle(82.0))
            self.draw_arc()
            glColor(self.get_color(angle))
            if not flash:
                self.draw_arrow(angle)
                glTranslatef(0,22,0)
                self.draw_text(value)
            if text: #POSSIBLY NOT USED
                glTranslatef(-18,-60,0)
                glScalef(0.14,0.14,1.0)
                glText(text, 95)
            
            glPopMatrix()
            

    def load_texture(self):
            self.bg_image = texture_image('images/EICAS_L.png')    
    
 
    def __init__(self):
        
        vert_spacing = 134
        #Create Engine Guages
        radius = 60
        self.Eng_CONST = EICAS_data.Engine_constants()
        self.show_FANVIB = EICAS_data.showFANVIB_c()
        #Eng1 N1 Guage
        self.Eng1_N1 = self.Dial_Guage(-180,600, 60, 90, 320, 0.0, 100, 0.0,  105, "%3.1f", flash_limit = self.Eng_CONST.N1_Overspeed)
        self.Eng1_N1.bug = self.N1_bug_c()
        self.Eng1_N1.green_arc = self.Eng1_N1.arc(green, 20, 0, self.Eng_CONST.N1_Overspeed, True, False)
        self.Eng1_N1.red_arc = self.Eng1_N1.arc(red, 5, self.Eng_CONST.N1_Overspeed, 100, False, True)
        #Eng2 N1 Guage
        self.Eng2_N1 = self.Dial_Guage(-40,600, 60, 90, 320, 0, 100, 0, 105, "%3.1f", flash_limit = self.Eng_CONST.N1_Overspeed)
        self.Eng2_N1.bug = self.Eng1_N1.bug
        self.Eng2_N1.green_arc = self.Eng1_N1.arc(green, 20, 0, self.Eng_CONST.N1_Overspeed, True, False)
        self.Eng2_N1.red_arc = self.Eng1_N1.arc(red, 5, self.Eng_CONST.N1_Overspeed, 100, False, True)
        #Eng1 ITT Guage
        self.Eng1_ITT = self.Dial_Guage(-180,600-vert_spacing, 60, 90, 320, 0, 900, 0, 1000, "%3d")
        self.Eng1_ITT.green_arc = self.Eng1_ITT.arc(green, 25, 0, self.Eng_CONST.ITT_OverTemp, True, False)
        self.Eng1_ITT.red_arc = self.Eng1_ITT.arc(red, 2,self.Eng_CONST.ITT_OverTemp,self.Eng_CONST.ITT_OverTemp,False, True)
        #Eng2 ITT Guage
        self.Eng2_ITT = self.Dial_Guage(-40,600-vert_spacing, 60, 90, 320, 0, 900, 0, 1000,"%3d")
        self.Eng2_ITT.green_arc = self.Eng2_ITT.arc(green, 25, 0, self.Eng_CONST.ITT_OverTemp, True, False)
        self.Eng2_ITT.red_arc = self.Eng2_ITT.arc(red, 2,self.Eng_CONST.ITT_OverTemp,self.Eng_CONST.ITT_OverTemp,False, True)
        #Eng1 N2 Guage
        self.Eng1_N2 = self.Dial_Guage(-180,600-2*vert_spacing, 60, 90,315, 0, 100, 0, 105, "%3.1f")
        self.Eng1_N2.green_arc = self.Eng1_N2.arc(green, 20, 0, self.Eng_CONST.N2_Overspeed, True, False)
        self.Eng1_N2.red_arc = self.Eng1_N2.arc(red, 20, self.Eng_CONST.N2_Overspeed, 100, False, True)
        #Eng2 N2 Guage
        self.Eng2_N2 = self.Dial_Guage(-40,600-2*vert_spacing, 60, 90, 315, 0, 100, 0, 105, "%3.1f")
        self.Eng2_N2.green_arc = self.Eng2_N2.arc(green, 20, 0, self.Eng_CONST.N2_Overspeed, True, False)
        self.Eng2_N2.red_arc = self.Eng2_N2.arc(red, 20, self.Eng_CONST.N2_Overspeed, 100, False, True)
        #Fuel Flow Data
        self.Eng1_FuelFlow = self.FF_Data_c(-223, 229, "%-5d")
        self.Eng2_FuelFlow = self.FF_Data_c(-78, 229, "%5d")
        #Oil Temp Data
        self.Eng1_OilTemp = self.OilTemp_Data_c(-223, 198, "%-3d", self.Eng_CONST.OilTemp_Red, self.Eng_CONST.OilTemp_Amber)
        self.Eng2_OilTemp = self.OilTemp_Data_c(-78, 198, "%5d", self.Eng_CONST.OilTemp_Red, self.Eng_CONST.OilTemp_Amber)
        #Oil Pressure Data
        self.Eng1_OilPress = self.OilPress_Data_c(-223, 167, "%-3d", self.Eng_CONST.OilPres_Red, self.Eng_CONST.OilPres_Amber)
        self.Eng2_OilPress = self.OilPress_Data_c(-78, 167, "%5d", self.Eng_CONST.OilPres_Red, self.Eng_CONST.OilPres_Amber)
        #Eng1 Oil Pressure Guage
        self.Eng1_OilGuage = self.Dial_Guage(-155, 105, 55, 210, 330, 0,136, 0, 156, "", True)
        self.Eng1_OilGuage.green_arc = self.Eng1_OilGuage.arc(green, 15, self.Eng_CONST.OilPres_Red, self.Eng_CONST.OilPres_Amber, True, False)
        self.Eng1_OilGuage.amber_arc = self.Eng1_OilGuage.arc(yellow, 15, self.Eng_CONST.OilPres_Amber, 136, True, True)
        self.Eng1_OilGuage.red_arc = self.Eng1_OilGuage.arc(red, 15, 0, self.Eng_CONST.OilPres_Red, True, False)
        #Eng2 Oil Pressure Guage
        self.Eng2_OilGuage = self.Dial_Guage(0, 105, 55, 210, 330, 0,136, 0, 156, "", True)
        self.Eng2_OilGuage.green_arc = self.Eng2_OilGuage.arc(green, 15, self.Eng_CONST.OilPres_Red, self.Eng_CONST.OilPres_Amber, True, False)
        self.Eng2_OilGuage.amber_arc = self.Eng2_OilGuage.arc(yellow, 15, self.Eng_CONST.OilPres_Amber, 136, True, True)
        self.Eng2_OilGuage.red_arc = self.Eng2_OilGuage.arc(red, 15, 0, self.Eng_CONST.OilPres_Red, True, False)
        #Eng1 Fan vibration Guage
        self.Eng1_FanVib = self.Dial_Guage(-180, 105, 55, 90, 330, 0, 5.2, 0, 5.2, "%3.1f", True)
        self.Eng1_FanVib.green_arc = self.Eng1_FanVib.arc(green, 25, 0, self.Eng_CONST.FANVIB_Yellow, True, False)
        self.Eng1_FanVib.amber_arc = self.Eng1_FanVib.arc(yellow,25, self.Eng_CONST.FANVIB_Yellow, 5.2, True, True)
        #Eng2 Fan vibration Guage
        self.Eng2_FanVib = self.Dial_Guage(-40, 105, 55, 90, 330, 0, 5.2, 0, 5.2, "%3.1f", True)
        self.Eng2_FanVib.green_arc = self.Eng2_FanVib.arc(green, 25, 0, self.Eng_CONST.FANVIB_Yellow, True, False)
        self.Eng2_FanVib.amber_arc = self.Eng2_FanVib.arc(yellow,25, self.Eng_CONST.FANVIB_Yellow, 5.2, True, True)
        #Create Engine Labels
        self.N1_Label = Guage_Label(-120, 545 +15, "N1")
        self.ITT_Label = Guage_Label(-127, 545- vert_spacing, "ITT")
        self.N2_Label = Guage_Label(-120, 545- 2*vert_spacing - 5, "N2")
        if config.use_metric_units:
            fuel_flow_text = "FF (KPH)"
        else:
            fuel_flow_text = "FF (PPH)"
        self.FF_Label = Guage_Label(-160, 230, fuel_flow_text)
        self.OilTemp_Label = Guage_Label(-160, 199, "OIL TEMP")
        self.OilPressure_Label = Guage_Label(-165, 168, "OIL PRESS")
        self.FanVib_Label = self.FanVib_Label_c(-118, 125)
        self.temp = 0
        
        #Gear and Flap show calc
        self.show_GEARFLAP = EICAS_data.show_GEARFLAP
        
        #Create GEAR Display
        y= 202
        x = 75
        self.Gear_Label = Guage_Label(x+47, y+25, "GEAR")
        spacing = 70
        self.Gear_Left_Disp = self.Gear_Disp(x, y)
        self.Gear_Nose_Disp = self.Gear_Disp(x+spacing, y)
        self.Gear_Right_Disp = self.Gear_Disp(x+2*spacing, y)
        
        #Create FLAPS Display
        x = 50 
        y= 136
        self.Flaps_Text = self.Flaps_Text_c(x+50, y+17)
        self.Flaps_Bar = self.Flaps_Bar_c(x,y, 190)
        
        #Create FUEL QTY Display
        x = 45
        y = 80
        if config.use_metric_units:
            fuel_text = "FUEL QTY (KGS)"
        else:
            fuel_text = "FUEL QTY (LBS)"
            
        self.Fuel_Qty_Label = Guage_Label(x+24,y+20, fuel_text, 0.11)
        self.Total_Fuel_Label = Guage_Label(x,y-25, "TOTAL FUEL", 0.11)
        self.Fuel_Left_Qty = self.Fuel_Qty_Disp(x-23,y-2, 0.14)
        self.Fuel_Center_Qty = self.Fuel_Qty_Disp(x+55,y-2, 0.14)
        self.Fuel_Right_Qty = self.Fuel_Qty_Disp(x+135,y-2, 0.14)
        self.Fuel_Total_Qty = self.Fuel_Qty_Disp(x+131,y-26, 0.14)
        
    def comp(self, aircraft):
        #Do all computes for this guage.
        self.show_FANVIB.comp(aircraft.Eng_1, aircraft.Eng_2, aircraft.onground.value, aircraft.global_time)
        #self.show_GEARFLAP.comp(aircraft.flaps, aircraft.gear, aircraft.global_time)
        
    def draw(self, aircraft, x,y):
        #self.bg_image.draw(x-255,y+32)
        glPushMatrix()
        glTranslatef(x,y,0)
        Eng1 = aircraft.Eng_1
        Eng2 = aircraft.Eng_2
        #Compute logic of Guage
        self.comp(aircraft)
        #Draw Engine Guages
        self.Eng1_N1.draw(Eng1.N1.value, globaltime, Eng1.N1_text)
        self.Eng2_N1.draw(Eng2.N1.value, globaltime, Eng2.N1_text)
        self.Eng1_ITT.draw(Eng1.ITT.value)
        self.Eng2_ITT.draw(Eng2.ITT.value)
        self.Eng1_N2.draw(Eng1.N2.value)
        self.Eng2_N2.draw(Eng2.N2.value)
        self.Eng1_FuelFlow.draw(Eng1.Fuel_Flow_disp)
        self.Eng2_FuelFlow.draw(Eng2.Fuel_Flow_disp)
        self.Eng1_OilTemp.draw(Eng1.Oil_Temp.value)
        self.Eng2_OilTemp.draw(Eng2.Oil_Temp.value)
        #Draw OilPressure Text
        self.Eng1_OilPress.draw(Eng1.Oil_Pressure.value)
        self.Eng2_OilPress.draw(Eng2.Oil_Pressure.value)
        #Draw Oil Pressure Guage or Fan Vibration Guage
        if self.show_FANVIB.show:
            #Draw Fan Vibration Guage
            self.Eng1_FanVib.draw(Eng1.Fan_Vibration.value)
            self.Eng2_FanVib.draw(Eng2.Fan_Vibration.value)
            self.FanVib_Label.draw()
        else: #Draw OilGuage
            self.Eng1_OilGuage.draw(Eng1.Oil_Pressure.value)
            self.Eng2_OilGuage.draw(Eng2.Oil_Pressure.value)
        
        #Draw Engine Guages Labels
        self.N1_Label.draw()
        self.ITT_Label.draw()
        self.N2_Label.draw()
        self.FF_Label.draw()
        self.OilTemp_Label.draw()
        self.OilPressure_Label.draw()
        
        if self.show_GEARFLAP.show:
            #Draw GEAR Display
            self.Gear_Label.draw()
            self.Gear_Left_Disp.draw(aircraft.gear.Left.position.value)
            self.Gear_Nose_Disp.draw(aircraft.gear.Nose.position.value)
            self.Gear_Right_Disp.draw(aircraft.gear.Right.position.value)
            #Draw FLAPS Display
            self.Flaps_Text.draw(aircraft.flaps.flap_deg)
            self.Flaps_Bar.draw(aircraft.flaps)
        
        #Draw FUEL QTY DIsplay
        self.Fuel_Qty_Label.draw()
        self.Total_Fuel_Label.draw()
        self.Fuel_Left_Qty.draw(aircraft.fuel.left)
        self.Fuel_Center_Qty.draw(aircraft.fuel.center)
        self.Fuel_Right_Qty.draw(aircraft.fuel.right)
        self.Fuel_Total_Qty.draw(aircraft.fuel.total)
                
        glPopMatrix()
