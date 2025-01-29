

class Sensor():
    def __init__(self, adc_channels):
        self.adcs = adc_channels
        # self.adcs = [ADC(chn) for chn in adc_channels]

    
    def read_sensors(self):
        return [adc.read() for adc in self.adcs]


    def read_voltages(self):
        return [adc.read_voltage() for adc in self.adcs]
