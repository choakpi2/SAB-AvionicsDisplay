import pickle
import guage


class data_obj(object):  # Used to make a object for Definition to link to
    def __init__(self, value):
        self.value = value
        self.adjusted = value  # Used incase value needs to be adjusted


class event_obj(object):  # Used to hold send event, with its data

    def __init__(self, value):
        self.value = value
        self.event_id = 0  # Set for 0 initially, will be equal to index of event list for this object
        self.update = False  # Can be used  to tell when to update data to FSX.


class PFD_pickle_c(object):

    def __init__(self, aircraft):
        self.attitude = aircraft.attitude

    def pickle_string(self):
        return pickle.dumps(self, -1)


class altimeter_c(object):

    def __init__(self):
        self.HG = 0
        self.HPA = 1
        self.pressure_unit = self.HG
        self.indicated = data_obj(20)
        self.pressure_HG = 29.92  # Kohlsman HG Altimeter Setting
        self.pressure_HPA = 1013
        self.absolute = data_obj(20)
        self.setting = 29.92
        self.bug = data_obj(3000)
        self.Kohlsmanx16 = event_obj(0)

    def convert_to_HPA(self):
        self.pressure_HPA = int(round(1013.2 / 29.92 * self.pressure_HG, 0))
        # Used to send out to FSX.
        self.Kohlsmanx16.value = int(round(1013.2 / 29.92 * self.pressure_HG * 16, 0))
        self.Kohlsmanx16.update = True
        self.setting = self.pressure_HG

    def convert_to_HG(self):
        # temp = 29.92 / 1013.0 * self.pressure_HPA
        self.pressure_HG = round(29.92 / 1013.2 * self.pressure_HPA, 2)
        self.setting = self.pressure_HPA  # Since converting to HG HPA is valid setting
        self.Kohlsmanx16.value = int(round(self.pressure_HPA * 16, 0))
        self.Kohlsmanx16.update = True

    def reset_setting(self):
        # Reset it to 29.92 / 1013
        self.pressure_HG = 29.92
        self.pressure_HPA = 1013
        self.Kohlsmanx16.value = int(round(1013 * 16, 0))
        self.Kohlsmanx16.update = True
        if self.pressure_unit == self.HG:
            self.setting = self.pressure_HG
        else:
            self.setting = self.pressure_HPA

    def inc_setting(self):
        # increase the Kohlsman Pressure
        if self.pressure_unit == self.HG:
            self.pressure_HG += 0.01
            self.convert_to_HPA()
        else:
            self.pressure_HPA += 1
            self.convert_to_HG()

    def dec_setting(self):
        # Decrease the Kohlsman Pressure
        if self.pressure_unit == self.HG:
            self.pressure_HG -= 0.01
            self.convert_to_HPA()
        else:
            self.pressure_HPA -= 1
            self.convert_to_HG()

    def change_unit(self):
        if self.pressure_unit == self.HG:
            round(self.pressure_HPA, 0)  # Convert it to .0, to be consistent.
            self.pressure_unit = self.HPA
            self.setting = self.pressure_HPA
            self.convert_to_HG()  # Used to update everything, and send data to FSX
        else:
            round(self.pressure_HG, 2)  # Round to 2 deciman, be consistent.
            self.pressure_unit = self.HG
            self.setting = self.pressure_HG
            self.convert_to_HPA()  # Used to update everything, and send data to FSX

    def bug_inc(self):
        self.bug.value += 100
        if self.bug.value > 60000:
            self.bug.value = 60000

    def bug_dec(self):
        self.bug.value -= 100
        if self.bug.value < 0:
            self.bug.value = 0

class HSI_c(object):

    def __init__(self):
        # Constants
        self.NADA = 0
        self.VOR = 1
        self.ADF = 2
        self.FMS = 3
        # Variables
        self.Mag_Heading = data_obj(123.5)
        self.True_Heading = 0.0
        self.Mag_Variation = data_obj(0)
        self.Mag_Track = data_obj(130.0)
        self.Heading_Bug = event_obj(20)
        self.Heading_Bug_Timer = 0  # Used as timer for drawing heading bug when its value changes
        self.Heading_Bug_prev = 20
        self.Bearing1 = self.ADF  # Will either be FMS, VOR or ADF
        self.Bearing2 = self.VOR

    def cycle_Bearing1(self):
        self.Bearing1 += 1
        if self.Bearing1 > self.ADF:
            self.Bearing1 = self.NADA

    def cycle_Bearing2(self):
        self.Bearing2 += 1
        if self.Bearing2 > self.ADF:
            self.Bearing2 = self.NADA

    def inc_Heading_Bug(self):
        self.Heading_Bug.value = guage.Check_360(self.Heading_Bug.value + 1)
        self.Heading_Bug.update = True
        self.Heading_Bug_Timer = guage.globaltime.value + 5

    def dec_Heading_Bug(self):
        self.Heading_Bug.value = guage.Check_360(self.Heading_Bug.value - 1)
        self.Heading_Bug.update = True
        self.Heading_Bug_Timer = guage.globaltime.value + 5


class attitude_c(object):

    class marker_c(object):

        def __init__(self):
            self.OM = 1
            self.MM = 2
            self.IM = 3
            self.value = self.OM
            self.count = 0

    def __init__(self):
        self.pitch = data_obj(10.0)
        self.bank = data_obj(10.0)
        self.FD_active = data_obj(0)
        self.FD_pitch = data_obj(10.0)
        self.FD_bank = data_obj(10.0)
        self.marker = self.marker_c()
        self.turn_coord = data_obj(0)


class declutter_c(object):

    def __init__(self):
        self.active = False

    def comp(self, pitch, bank):  # Declutter active when pitch >=30 or <= -20, bank >= 65 degrees
        if (pitch >= 20.0) | (pitch <= -30.0):  # Pitch is reversed from FSX
            self.active = True
        elif (abs(bank) >= 65.0):
            self.active = True
        else:
            self.active = False


class airspeed_c(object):

    class V_speed_c(object):

        def inc(self):
            self.value += 1
            if self.value > 350:
                self.value = 350

        def dec(self):
            self.value -= 1
            if self.value < 40:
                self.value = 40

        def onoff(self):
            if self.visible:
                self.visible = False
            else:
                self.visible = True

        def __init__(self, text, initvalue):
            self.value = initvalue
            self.visible = True
            self.text = text

    def set_disp(self, Vspeed):
        # This sets what is displayed below speed tape. (Goes blank after a few seconds)
        self.Vspeed_disp = Vspeed
        self.Vspeed_disp_timer = guage.globaltime.value + 5  # 5 sec delay

    def cycle_Vspeed_input(self):
        temp = self.Vspeed_input
        if temp == self.V1:
            out = self.VR
        elif temp == self.VR:
            out = self.V2
        else:
            out = self.V1
        self.Vspeed_input = out
        self.set_disp(out)

    def inc_Vspeed_input(self):
        self.Vspeed_input.inc()
        self.set_disp(self.Vspeed_input)

    def dec_Vspeed_input(self):
        self.Vspeed_input.dec()
        self.set_disp(self.Vspeed_input)

    def visible_Vspeed_input(self):
        self.Vspeed_input.onoff()
        self.set_disp(self.Vspeed_input)

    def inc_VT(self):
        self.VT.inc()
        self.set_disp(self.VT)

    def dec_VT(self):
        self.VT.dec()
        self.set_disp(self.VT)

    def visible_VT(self):
        self.VT.onoff()
        self.set_disp(self.VT)

    def __init__(self):
        self.IAS = data_obj(360.0)  # self.IAS.value is value read from FSX
        self.IAS_guage = 360.0
        self.IAS_diff = 10.0  # Pink Line to show accel or decell
        self.trend_visible = False  # Speed trend turns on  H> 20ft, turns off speed <105kts
        self.IAS_prev = self.IAS.value
        self.IAS_list = [0] * 40  # This is used to compute IAS accelertation for airspped tape
        self.TAS = 0.0
        self.Mach = data_obj(0.475)
        self.Mach.active = False
        self.GS = data_obj(0.0)
        self.V1 = self.V_speed_c("V1 ", 135)
        self.V2 = self.V_speed_c("V2 ", 144)
        self.VR = self.V_speed_c("VR ", 137)
        self.VT = self.V_speed_c("VT ", 110)
        self.Vspeed_input = self.V1  # Currently selected one to be changed by knob
        self.Vspeed_disp = self.V1  # The one that is displayed below speed tape
        self.Vspeed_disp_timer = 0  # Used for delay of timer
        self.bug = data_obj(150)
        self.maxspeed = 260  # Never Exceed speed Red line
        self.minspeed = 220  # Stall speed
        self.lowspeed = 140

    def comp(self):
        if self.IAS.value <= 40:
            self.IAS_guage = 40
        else:
            self.IAS_guage = self.IAS.value

    def comp_IAS_accel(self, airspeed, frame_rate):
        # Computes forcastes IAS in 10 seconds for the IAS tape IAS_diff
        # Find difference between new_IAS and last reading
        diff = self.IAS.value - self.IAS_prev
        self.IAS_prev = self.IAS.value
        # Add diff reading to list pop oldest one
        self.IAS_list.append(diff)
        self.IAS_list.pop(0)
        a = self.IAS_list
        self.IAS_diff = (sum(a) / len(a)) / frame_rate * 10
