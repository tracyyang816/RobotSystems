
try:
    from robot_hat import ADC

except ModuleNotFoundError:
    from sim_robot_hat import ADC

class Sensor():
    def __init__(self, adc_channels = ['A0', 'A1', 'A2']):
        # self.adcs = adc_channels
        self.adcs = [ADC(chn) for chn in adc_channels]

    
    def read_sensors(self):
        return [adc.read() for adc in self.adcs]