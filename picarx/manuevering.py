import picarx_improved
import time
import sys
from sensor import Sensor
from interpreter import Interpretor
from controller import Controller



def straight_line_test(px):
    px.set_dir_servo_angle(10)
    px.forward(50)
    time.sleep(1)
   
    px.set_dir_servo_angle(0)
    px.forward(50)
    time.sleep(1)

    px.backward(50)
    time.sleep(1)
    

    px.set_dir_servo_angle(-10)
    px.forward(50)
    time.sleep(1)

    px.set_dir_servo_angle(0)
    px.forward(50)
    time.sleep(1)
  
    px.backward(50)
    time.sleep(1)
 
    px.stop()
    px.set_dir_servo_angle(0)

# allow direction input
# go forward first
# do not over turn in the end

def paralell_park(px, dir):
    if dir == "right":
        px.forward(50)
        time.sleep(1)
       
        px.set_dir_servo_angle(45)
        px.backward(30)
        time.sleep(1)

        px.set_dir_servo_angle(0)
        px.backward(50)
        time.sleep(1)

        px.set_dir_servo_angle(-45)
        px.backward(30)
        time.sleep(1)

        px.stop()
        px.set_dir_servo_angle(0)
    
    if dir == "left":
        px.set_dir_servo_angle(0)
        px.forward(50)
        time.sleep(1)
     

        px.set_dir_servo_angle(-45)
        px.backward(30)
        time.sleep(1)
  

        px.set_dir_servo_angle(0)
        px.backward(50)
        time.sleep(1)

        px.set_dir_servo_angle(45)
        px.backward(30)
        time.sleep(1)

        px.stop()
        px.set_dir_servo_angle(0)

def three_point_parking(px, dir):
    px.set_dir_servo_angle(0)
    if dir == "left":
        px.forward(50)
        time.sleep(1)
    

        px.set_dir_servo_angle(-90)
        px.forward(50)
        time.sleep(1)

        px.set_dir_servo_angle(0)
        px.backward(50)
        time.sleep(1)


        px.set_dir_servo_angle(-90)
        px.forward(50)
        time.sleep(1)
        px.stop()

        px.set_dir_servo_angle(0)

    if dir == "right":
        px.forward(50)
        time.sleep(1)
      

        px.set_dir_servo_angle(90)
        px.forward(50)
        time.sleep(1)
     
        px.set_dir_servo_angle(0)
        px.backward(50)
        time.sleep(1)
     

        px.set_dir_servo_angle(90)
        px.forward(50)
        time.sleep(1)
 

    
        px.stop()
        px.set_dir_servo_angle(0)

def line_following(px):
    sensor = Sensor() # px.get_grayscale_data()
    interpretor = Interpretor(100, "darker") # might adjust these value later
    controller = Controller(px, 30)
    prev_pos = 0

    try:
        while True:
            adc_val = sensor.read_sensors()
            car_pos = interpretor.process(adc_val, prev_pos)
            prev_pos = car_pos
            controller.drive(car_pos)
            time.sleep(1)

            px.forward(30)
            time.sleep(0.05)
            
    
    except KeyboardInterrupt:
        px.stop()

    

def main():
    px = picarx_improved.Picarx()

    while True:
        cmd = input("Enter new command:")
        if cmd == "1":
            straight_line_test(px)
        elif cmd == "2":
            dir = input ("left or right? ")
            paralell_park(px, dir)
        elif cmd == "3":
            dir = input("left or right? ")
            three_point_parking(px, dir)
        elif cmd == "4":
            line_following(px)
        elif cmd == "q":
            break
        else:
            cmd = input("Please enter another valid command.")


if __name__ == "__main__":
    main()