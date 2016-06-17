from pygame.locals import *
import guage

#import aircraft

CTRL = 1
ALT = 2
SHIFT = 3

class keylist(object):
	
	def __init__(self, aircraft, screen):
		self.keydown = False #Used for status of sticky keys
		self.setup_lists(aircraft, screen) #Load in all keybindings
		self.mousedown = False
		self.screen = screen
		self.aircraft = aircraft
		
	def check_events(self,events, globaltime):
		#keys.check(pygame.event.get())
		for event in events:
			#print event
			if event.type == KEYDOWN:
				self.pressed(event.key, event.mod, globaltime)
			elif event.type == KEYUP:
				self.keyup_event()

	def keyup_event(self):
		self.keydown = False
  
	def check_stuckkey(self, globaltime):
		#Stuck key delay
		def check_delay(elapsed, period, globaltime):
				if globaltime - self.keydown_time  > elapsed:
					if globaltime - self.keydown_repeat_time > period:
						self.keydown_func[1]()
						self.keydown_repeat_time = globaltime #Reset 
					return True
				else:
					return False

		if self.keydown: #If key still down
			if check_delay(3.5, 0.05, globaltime): #If key down for more than 3 seconds then simulate 20 / second
				pass
			else:
				check_delay(1.5, 0.1, globaltime) #If key down for more than 1.5 second then simulate 10 /second
	
	def pressed(self, key, mods, globaltime):
		#
		if (mods & KMOD_CTRL):
			k_list = self.key_list_ctrl
		elif (mods & KMOD_ALT):
			k_list = self.key_list_alt
		elif (mods & KMOD_SHIFT):
			k_list = self.key_list_shift
		else:
			k_list = self.key_list
		for i in k_list:
			if i[0] == key:
				i[1]() #Call the function 
				if i[2]: #if key repeat enabled then setup keydown data
					self.keydown = True
					self.keydown_time = globaltime
					self.keydown_repeat_time = globaltime
					self.keydown_func = i
					
	
	#Set up association with keys and function upon a keydown event	
	def setup_lists(self, aircraft, screen):
	#	global key_list, key_list_ctrl, key_list_alt, key_list_shift
		#key_list = [[K_b, aircraft.ND.range.down], [K_v, aircraft.ND.range.up]]
		
		
		
		def add_key(key, func, ctrl_alt = None, repeat = False):
		#global key_list, key_list_ctrl, key_list_alt
		
			if ctrl_alt == CTRL:
				self.key_list_ctrl.append([key,func,repeat])
			elif ctrl_alt == ALT:
				self.key_list_alt.append([key,func,repeat])
			elif ctrl_alt == SHIFT:
				self.key_list_shift.append([key,func,repeat])
			else:
				self.key_list.append([key,func,repeat])
				
			
		self.key_list = []
		self.key_list_ctrl = []
		self.key_list_alt = []
		self.key_list_shift = []


		#Debuging Keys for Programming Only
		add_key(K_1, guage.globaltest.one_inc, SHIFT, True)
		add_key(K_1, guage.globaltest.one_dec, CTRL, True)
		add_key(K_2, guage.globaltest.two_inc, SHIFT, True)
		add_key(K_2, guage.globaltest.two_dec, CTRL, True)
		add_key(K_3, guage.globaltest.three_inc, SHIFT, True)
		add_key(K_3, guage.globaltest.three_dec, CTRL, True)
  
		add_key(K_PAGEDOWN, aircraft.ND.range.down)
		add_key(K_PAGEUP, aircraft.ND.range.up)
		add_key(K_1, aircraft.HSI.cycle_Bearing1)
		add_key(K_2, aircraft.HSI.cycle_Bearing2)
		
		add_key(K_TAB, aircraft.NAV.cycle_Active_NAV)
		add_key(K_q, aircraft.quit, CTRL) #Either CTRL-Q or ESCAPE will quit
		add_key(K_ESCAPE, aircraft.quit)
		#Vspeed manipulation
		add_key(K_z, aircraft.airspeed.cycle_Vspeed_input, ALT)
		add_key(K_z, aircraft.airspeed.inc_Vspeed_input, None, True)
		add_key(K_z, aircraft.airspeed.dec_Vspeed_input, SHIFT, True)
		add_key(K_z, aircraft.airspeed.visible_Vspeed_input, CTRL)
		#VT specific manipulation
		add_key(K_y, aircraft.airspeed.visible_VT, CTRL)
		add_key(K_y, aircraft.airspeed.inc_VT, None, True)
		add_key(K_y, aircraft.airspeed.dec_VT, SHIFT, True)
		#Decision Height
		add_key(K_d, aircraft.altimeter.DH.cycle_visible, CTRL)
		add_key(K_d, aircraft.altimeter.DH.bug_increase, None, True)
		add_key(K_d, aircraft.altimeter.DH.bug_decrease, SHIFT, True)
		#MDA
		add_key(K_m, aircraft.altimeter.MDA.cycle_visible, CTRL)
		add_key(K_m, aircraft.altimeter.MDA.bug_increase, None, True)
		add_key(K_m, aircraft.altimeter.MDA.bug_decrease, SHIFT, True)
		#Heading Bug
		add_key(K_h, aircraft.HSI.inc_Heading_Bug, None, True)
		add_key(K_h, aircraft.HSI.dec_Heading_Bug, SHIFT, True)
		#Kollsman
		add_key(K_b, aircraft.altimeter.reset_setting, None, False)
		add_key(K_b, aircraft.altimeter.change_unit, ALT, False)
		add_key(K_b, aircraft.altimeter.inc_setting, SHIFT, True)
		add_key(K_b, aircraft.altimeter.dec_setting, CTRL, True)

		#Cycle the screen
		add_key(K_RIGHTBRACKET, screen.cycle, None)
		add_key(K_RIGHTBRACKET, screen.cycle_reverse, SHIFT)
