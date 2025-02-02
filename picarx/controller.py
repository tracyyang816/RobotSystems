

class Controller():
    def __init__(self, px, scalar = 10):
        self.px = px
        self.scalar = scalar
        self.angle = 0
    
    def drive(self, position):
        if position == None:
            # then we need to go find the line
            self.px.stop()
            angle = 0

            self.px.set_dir_servo_angle(self.angle)
        else:
            angle = position * self.scalar
            self.px.set_dir_servo_angle(angle)
            self.angle = angle
        return angle
