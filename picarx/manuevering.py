import picarx_improved
import time
import sys



def straight_line_test(px):
    px.set_dir_servo_angle(10)
    px.forward(10)
    time.sleep(1)
  

    px.set_dir_servo_angle(0)
    px.forward(20)
    time.sleep(1)
    px.stop()

    px.backward(50)
    time.sleep(1)
    px.stop()

    px.set_dir_servo_angle(-10)
    px.forward(10)
    time.sleep(1)

    px.set_dir_servo_angle(0)
    px.forward(50)
    time.sleep(1)
    px.stop()
    px.backward(50)
    time.sleep(1)
    px.stop()

    px.set_dir_servo_angle(0)

# allow direction input
# go forward first
# do not over turn in the end

def paralell_park(px, dir):
    if dir == "right":
        px.set_dir_servo_angle(10)
        px.set_dir_servo_angle(0)
        px.forward(10)
        time.sleep(1)
        px.stop()
       

        px.set_dir_servo_angle(45)
        px.backward(10)
        time.sleep(1)
        px.stop()

        px.set_dir_servo_angle(0)
        px.backward(10)
        time.sleep(1)
        px.stop()

        px.set_dir_servo_angle(-45)
        px.backward(10)
        time.sleep(1)
        px.stop()

        px.set_dir_servo_angle(0)
    
    if dir == "left":
        # px.set_dir_servo_angle(0)
        px.forward(10)
        time.sleep(1)
        px.stop()


        px.set_dir_servo_angle(-45)
        px.backward(10)
        time.sleep(1)
        px.stop()

        px.set_dir_servo_angle(0)
        px.backward(10)
        time.sleep(1)
        px.stop()

        px.set_dir_servo_angle(45)
        px.backward(10)
        time.sleep(1)
        px.stop()

        px.set_dir_servo_angle(0)

def three_point_parking(px, dir):
    px.set_dir_servo_angle(0)
    if dir == "left":
        px.forward(10)
        time.sleep(1)
        px.stop()

        px.set_dir_servo_angle(-90)
        px.forward(20)
        time.sleep(1)
        px.stop()

        px.set_dir_servo_angle(0)
        px.backward(20)
        time.sleep(1)
        px.stop()

        px.set_dir_servo_angle(-90)
        px.forward(20)
        time.sleep(1)
        px.stop()

       

        px.set_dir_servo_angle(0)

    if dir == "right":
        px.forward(10)
        time.sleep(1)
        px.stop()

        px.set_dir_servo_angle(90)
        px.forward(20)
        time.sleep(1)
        px.stop()

        px.set_dir_servo_angle(0)
        px.backward(20)
        time.sleep(1)
        px.stop()

        px.set_dir_servo_angle(90)
        px.forward(20)
        time.sleep(1)
        px.stop()

    

        px.set_dir_servo_angle(0)

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
        elif cmd == "q":
            break
        else:
            cmd = input("Please enter another valid command.")


if __name__ == "__main__":
    main()