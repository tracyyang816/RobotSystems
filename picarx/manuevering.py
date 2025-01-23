import picarx_improved
import time
import sys



def straight_line_test(px):
    print("here")
    px.dir_current_angle = 30
    px.forward(50)
    time.sleep(1)
    px.stop()
    px.backward(50)
    time.sleep(1)
    px.stop()

    px.dir_current_angle = -10
    px.forward(50)
    time.sleep(1)
    px.stop()
    px.backward(50)
    time.sleep(1)
    px.stop()


def paralell_park_right(px):
    px.forward(10)
    time.sleep(1)
    px.stop()

    px.dir_current_angle = 45
    px.backward(10)
    time.sleep(1)
    px.stop()

    px.dir_current_angle = 0
    px.backward(10)
    time.sleep(1)
    px.stop()

    px.dir_current_angle = -45
    px.backward(10)
    time.sleep(1)
    px.stop()

def three_point_parking(px, dir):
    if dir == "left":
        px.forward(10)
        time.sleep(1)
        px.stop()

        px.dir_current_angle = -90
        px.forward(50)
        time.sleep(1)
        px.stop()

        px.dir_current_angle = 0
        px.backward(50)
        time.sleep(1)
        px.stop()

        px.dir_current_angle = -90
        px.forward(50)
        px.stop()

    if dir == "right":
        px.forward(10)
        time.sleep(1)
        px.stop()

        px.dir_current_angle = 90
        px.forward(50)
        time.sleep(1)
        px.stop()

        px.dir_current_angle = 0
        px.backward(50)
        time.sleep(1)
        px.stop()

        px.dir_current_angle = 90
        px.forward(50)
        px.stop()

def main(args):
    cmd = args[0]
    px = picarx_improved.Picarx()

    while True:
        cmd = input("Enter new command:")
        if cmd == "1":
            straight_line_test(px)
        elif cmd == "2":
            paralell_park_right(px)
        elif cmd == "3":
            dir = input("left or right?")
            three_point_parking(px, dir)
        elif cmd == "q":
            break
        else:
            cmd = input("Please enter another valid command.")


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)