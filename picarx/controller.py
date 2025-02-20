import time
import random 

class Controller():
    def __init__(self, px, scalar = 10):
        self.px = px
        self.scalar = scalar
        self.no_line = 0
    
    def drive(self, position, has_line):
        
        if has_line == False:

            '''
            self.no_line += 1
            # then we need to go find the line
            print("no line")

            position = float(position)
            angle = position * self.scalar

            self.angle = angle
    

            if self.no_line > 5:
                self.angle = -self.angle
                self.no_line = 0

            '''

            self.px.set_dir_servo_angle(0)
            self.px.backward(30)
            time.sleep(0.2)
            self.px.stop()
            

            # angle = 0
            # self.px.set_dir_servo_angle(self.angle)
            
        else:
            position = float(position)
            angle = position * self.scalar
            self.px.set_dir_servo_angle(angle)
            # self.angle = angle
        
            self.px.forward(30)
            time.sleep(0.2)
            self.px.stop()

        return angle
