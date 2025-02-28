
import ast 

class Interpreter():
    def __init__(self, sensitivity, polarity):
        self.sensitivity = sensitivity 
        self.polarity = polarity
        self.pos = 0

        # if polarity == "darker", line is darker
        # if polarity == "lighter", line is lighter
    
    def process(self, sensor_values): # sensor_vals is a list of 3 adc values

        if sensor_values == "0":
            position = 0

        line = False
        for i in range(0, 2):
            diff = abs(sensor_values[i] - sensor_values[i+1])
            if diff > self.sensitivity:
                line = True

        if line == False:
            position = self.pos

        else: 
        
            max_sensor_val = max(sensor_values)
            max_sensor = sensor_values.index(max_sensor_val)

            if self.polarity == "lighter":

                if max_sensor == 1:
                    position = 0
                
                elif max_sensor == 0:
                    position = -(max_sensor_val - sensor_values[1])/max_sensor_val
                
                elif max_sensor == 2:
                    position = (max_sensor_val - sensor_values[1])/max_sensor_val
            

            min_sensor_val = min(sensor_values)
            min_sensor = sensor_values.index(min_sensor_val)

            if self.polarity == "darker":

                if min_sensor == 1:
                    position = 0
                
                elif min_sensor == 0:
                    position = min_sensor_val/ (min_sensor_val + sensor_values[1]) - 1
                
                elif min_sensor == 2:
                    position = 1 - min_sensor_val/ (min_sensor_val + sensor_values[1]) 
     
            self.pos = position
        return position, line



class Ultrasonic_Interpreter():
    def __init__(self):
        pass
    
    def process(self, distance):
        if distance < 3:
            return 0
        else:
            return 1