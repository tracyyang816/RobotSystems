import time
import random 

class Controller():
    def __init__(self, px, scalar = 10):
        self.px = px
        self.scalar = scalar
        # self.angle = 0
    
    def drive(self, position, has_line):
        
        if has_line == False:
            # then we need to go find the line
            print("no line")
            angle = random.choice([-30, 30])

            # position = float(position)
            # angle = position * self.scalar
            self.px.set_dir_servo_angle(angle)
            self.px.forward(10)
            time.sleep(0.02)
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
