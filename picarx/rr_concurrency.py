# WEEK 5 Concurrent Line Following Using RossRos


import sys
import time 

import rossros as rr
from rossros import Bus, Producer, Consumer, ConsumerProducer, Timer
from picarx_improved import Picarx

from sensor import Sensor, Ultrasonic_Sensor
from interpreter import Interpreter, Ultrasonic_Interpreter
from controller import Controller, Ultrasonic_Controller

import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import logging
logging.basicConfig(level=logging.INFO)



px = Picarx()

sensor = Sensor()
controller = Controller(px, 30)
interpreter = Interpreter(100, "darker")

sensor_values_bus = Bus()
interpreter_bus = Bus()
shutdown_event = Event()


bTerminate = Bus(0, "Termination Bus")

def cam_sensor_function(): # producer
    print("camera sensor reading")
    adc_val = sensor.read_sensors()
    return adc_val
    
    
def cam_controller_function(pos): # consumer 
    print("camera controller driving")
    controller.drive(pos)


def cam_interpreter_function(adc_val): # consumer_producer
    print("camera interpreter read and write")
    pos = interpreter.process(adc_val)
    return pos




# Ultrasonic Stuff
us_sensor = Ultrasonic_Sensor(px)
us_interpreter = Ultrasonic_Interpreter()
us_controller = Ultrasonic_Controller(px)

us_distance_bus = Bus()
us_interpreter_bus = Bus()

def us_sensor_function(): # producer
    print("ultrasonic sensor reading")
    distance = us_sensor.read()
    return distance

    
    
def us_controller_function(stop_signal): # consumer 
    print("ultrasonic controller driving")
    us_controller.stop(stop_signal)


def us_interpreter_function(dist): # consumer_producer
    print("interpreter read and write")
    stop_signal = us_interpreter.process(dist)
    return stop_signal



if __name__ == "__main__":

    terminationTimer = Timer(
        bTerminate,  # Output data bus
        3,  # Duration
        0.01,  # Delay between checking for termination time
        bTerminate,  # Bus to check for termination signal
        "Termination timer")  # Name of this timer

    cam_interpreter = ConsumerProducer(
        cam_interpreter_function, 
        (sensor_values_bus), 
        interpreter_bus, 
        0.5,
        bTerminate,
        "cam interpreter")


    cam_sensor = Producer(
        cam_sensor_function, 
        sensor_values_bus, 
        0.5,
        bTerminate,
        "cam sensor")

    cam_controller = Consumer(
        cam_controller_function, 
        (interpreter_bus), 
        1, 
        bTerminate,
        "camera drive controller")



    us_interpreter_cp = ConsumerProducer(
        us_interpreter_function, 
        (us_distance_bus), 
        us_interpreter_bus, 
        0.5,
        bTerminate,
        "ultrasonic interpreter")

    us_sensor_p = Producer(
        us_sensor_function, 
        us_distance_bus, 
        0.5,
        bTerminate,
        "ultrasonic sensor")

    us_controller_c = Consumer(
        us_controller_function, 
        (us_interpreter_bus), 
        1,
        bTerminate,
        "ultrasonic stop controller")

    producer_consumer_list = [cam_interpreter, cam_sensor, cam_controller, us_interpreter_cp, us_sensor_p, us_controller_c, terminationTimer]

# Execute the list of producer-consumers concurrently



rr.runConcurrently(producer_consumer_list)
