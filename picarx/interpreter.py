
import ast 

class Interpretor():
    def __init__(self, sensitivity, polarity):
        self.sensitivity = sensitivity 
        self.polarity = polarity
        self.pos = 0

        # if polarity == "darker", line is darker
        # if polarity == "lighter", line is lighter
    
    def process(self, sensor_values): # sensor_vals is a list of 3 adc values

        sensor_values = ast.literal_eval(sensor_values)
        

        line = False
        for i in range(0, 2):
            diff = abs(sensor_values[i] - sensor_values[i+1])
            if diff > self.sensitivity:
                line = True

        if line == False:
            position = self.pos

        else: 
        
            position = None
            
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
                
            print(sensor_values,min_sensor, position)
            self.pos = position
            return position
        '''
        for i in range(0, 2):
            diff = sensor_values[i] - sensor_values[i+1]

            rising_edge = None
            falling_edge = None

            if self.polarity == "darker":
                if diff < -self.sensitivity: 
                    rising_edge = i
                if diff > self.sensitivity:
                    falling_edge = i

            if self.polarity == "lighter":
                if diff < -self.sensitivity: 
                    falling_edge = i
                if diff > self.sensitivity:
                    rising_edge = i
        
        if rising_edge == 0 and falling_edge == 1:
            position = 0

        elif falling_edge == 0: # car is on the right 
            position = -1.0 
        elif rising_edge == 0:
            position = 0.5
        elif rising_edge == 1: # car is on the left 
            position = 1.0 
        elif falling_edge == 1:
            position = -0.5
        else:
            position = None

        print(rising_edge, position)
        return position
        '''


