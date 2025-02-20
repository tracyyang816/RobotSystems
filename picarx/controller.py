import time
import random 

class Controller():
    def __init__(self, px, scalar = 10):
        self.px = px
        self.scalar = scalar
        self.no_line = 0
        self.angle = 0
    
    def drive(self, position, has_line):
        
        if has_line == False:

            self.px.set_dir_servo_angle(self.angle)
            self.no_line += 1

            if self.no_line > 5:

                self.no_line = 0
                self.px.set_dir_servo_angle(0)
                self.px.backward(30)
                time.sleep(0.2)
                self.px.stop()
                

                # angle = random.randint([30, -30])
            
        else:
            position = float(position)
            angle = position * self.scalar
            self.px.set_dir_servo_angle(angle)
            self.angle = angle
        
            self.px.forward(30)
            time.sleep(0.2)
            self.px.stop()

        # return angle
