from robot_hat import ADC
from threading import Lock


class Sensor():
    def __init__(self, adc_channels=['A0', 'A1', 'A2']):
        self.adc_channels = adc_channels
        self.adc = ADC()  # Single ADC instance
        self.lock = Lock()
    
    def read_sensors(self):
        with self.lock:
            return [self.adc.read(chn) for chn in self.adc_channels]

    '''
    def __init__(self, adc_channels = ['A0', 'A1', 'A2']):
        # self.adcs = adc_channels
        self.adcs = [ADC(chn) for chn in adc_channels]

    
    def read_sensors(self):
        return [adc.read() for adc in self.adcs]

    '''