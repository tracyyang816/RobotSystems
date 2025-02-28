from robot_hat import ADC
from robot_hat import Ultrasonic
from threading import Lock



class Sensor():

    def __init__(self, adc_channels = ['A0', 'A1', 'A2']):
        # self.adcs = adc_channels
        self.adcs = [ADC(chn) for chn in adc_channels]

    
    def read_sensors(self):
        return [adc.read() for adc in self.adcs]


class Ultrasonic_Sensor():

    def __init__(self, px):
        self.px = px
    
    def read(self):
        return self.px.ultrasonic.read()
