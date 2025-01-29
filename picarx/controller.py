

class Controller():
    def __init__(self, px, scalar = 30):
        self.px = px
        self.scalar = scalar
    
    def drive(self, position):
        if position == None:
            # then we need to go find the line
            self.px.stop()
        else:
            angle = position * self.scalar
            self.px.set_dir_servo_angle(angle)
        return angle
