from picarx_improved import Picarx

class Controller():
    def __init__(self, px, scalar = 30):
        self.px = px
        self.scalar = scalar
    
    def drive(self, position):
        angle = position * self.scalar
        self.px.set_dir_servo_angle(angle)
        return angle
