

class Interpretor():
    def __init__(self, sensitivity, polarity):
        self.sensitivity = sensitivity 
        self.polarity = polarity

        # if polarity == "darker", line is darker
        # if polarity == "lighter", line is lighter
    
    def process(self, sensor_values): # sensor_vals is a list of 3 adc values
        rising_edge = None
        falling_edge = None
        for i in range(0, 2):
            diff = sensor_values[i] -sensor_values[i+1]

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



