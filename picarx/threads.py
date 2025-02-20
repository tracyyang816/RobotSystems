import picarx_improved
import time
import sys
from sensor import Sensor
from interpreter import Interpreter
from controller import Controller
from bus import Bus
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from threading import Event



px = picarx_improved.Picarx()

sensor = Sensor()
controller = Controller(px, 30)
interpretor = Interpreter(100, "darker")

sensor_values_bus = Bus()
interpreter_bus = Bus()

# Define shutdown event
shutdown_event = Event()



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
        pos = interpretor.process(adc_val)
        pos_bus.write(pos)
        time.sleep(delay)



def handle_exception(future):
    exception = future.exception()
    if exception:
        print(f"Exception in worker thread: {exception, future}")
        shutdown_event.set()


if __name__ == "__main__":
    

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for i in range(0, 3):
            match i:
                case 0: 
                    eSensor = executor.submit(sensor_function, sensor_values_bus, 0.5)
                    eSensor.add_done_callback(handle_exception)
                case 1:
                    eInterpreter = executor.submit(interpreter_function,sensor_values_bus, interpreter_bus,0.5)
                    eInterpreter.add_done_callback(handle_exception)
                case 2:
                    eController = executor.submit(controller_function, interpreter_bus, 1)
                    eController.add_done_callback(handle_exception)

        try:
            # Keep the main thread running to response for the kill signal
            while not shutdown_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            # Trigger the shutdown event when receive the kill signal
            print("Shutting down")
            shutdown_event.set()
        finally:
            # Ensures all threads finish
            executor.shutdown()