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

def sensor_function(adc_bus, delay): # producer
    while not shutdown_event.is_set():
        print("sensor reading")
        adc_val = sensor.read_sensors()
        adc_bus.write(adc_val)
        time.sleep(delay)
    
    
def controller_function(pos_bus, delay): # consumer 
    while not shutdown_event.is_set():
        print("controller driving")
        pos = pos_bus.read()
        controller.drive(pos)
        time.sleep(delay)


def interpreter_function(adc_bus, pos_bus, delay): # consumer_producer
    while not shutdown_event.is_set():
        print("interpreter read and write")
        adc_val = adc_bus.read()
        pos = interpreter.process(adc_val)
        pos_bus.write(pos)
        time.sleep(delay)




# Ultrasonic Stuff
us_sensor = Ultrasonic_Sensor(px)
us_interpreter = Ultrasonic_Interpreter()
us_controller = Ultrasonic_Controller(px)

us_distance_bus = Bus()
us_interpreter_bus = Bus()

def us_sensor_function(dist_bus, delay): # producer
    while not shutdown_event.is_set():
        print("ultrasonic sensor reading")
        distance = us_sensor.read()
        dist_bus.write(distance)
        time.sleep(delay)
    
    
def us_controller_function(us_bus, delay): # consumer 
    while not shutdown_event.is_set():
        print("ultrasonic controller driving")
        stop_signal = us_bus.read()
        us_controller.stop(stop_signal)
        time.sleep(delay)


def us_interpreter_function(dist_bus, us_bus, delay): # consumer_producer
    while not shutdown_event.is_set():
        print("interpreter read and write")
        dist = dist_bus.read()
        stop_signal = us_interpreter.process(dist)
        us_bus.write(stop_signal)
        time.sleep(delay)

def handle_exception(future):
    exception = future.exception()
    if exception:
        print(f"Exception in worker thread: {exception, future}")
        shutdown_event.set()


if __name__ == "__main__":

    terminationTimer = Timer(
        bTerminate,  # Output data bus
        3,  # Duration
        0.01,  # Delay between checking for termination time
        bTerminate,  # Bus to check for termination signal
        "Termination timer")  # Name of this timer

    cam_interpreter = ConsumerProducer(
        interpreter_function, 
        sensor_values_bus, 
        interpreter_bus, 
        0.5,
        bTerminate,
        "cam interpreter")



    cam_sensor = Producer(
        sensor_function, 
        sensor_values_bus, 
        0.5,
        bTerminate,
        "cam sensor")

    cam_controller = Consumer(
        controller_function, 
        interpreter_bus, 
        1, 
        bTerminate,
        "camera drive controller")



    us_interpreter = ConsumerProducer(
        us_interpreter_function, 
        us_distance_bus, 
        us_interpreter_bus, 
        0.5,
        bTerminate,
        "ultrasonic interpreter")

    us_sensor = Producer(
        us_sensor_function, 
        us_distance_bus, 
        0.5,
        bTerminate,
        "ultrasonic sensor")

    us_controller = Consumer(
        us_controller_function, 
        us_interpreter_bus, 
        1,
        bTerminate,
        "ultrasonic stop controller")

    producer_consumer_list = [cam_interpreter, cam_sensor, cam_controller, us_interpreter, us_sensor, us_controller, terminationTimer]

# Execute the list of producer-consumers concurrently


try:
    rr.runConcurrently(producer_consumer_list)
except KeyboardInterrupt:
    print("Shutting down")
    shutdown_event.set()
    time.sleep(1)
