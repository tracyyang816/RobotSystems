import picarx_improved
import time
import sys
from sensor import Sensor
from interpreter import Interpretor
from controller import Controller
from bus import Bus
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from threading import Event



px = picarx_improved.Picarx()

sensor = Sensor()
controller = Controller(px, 30)
interpretor = Interpretor(100, "darker")

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
        print(f"Exception in worker thread: {exception}")
        shutdown_event.set()

'''
# Define robot task
def robot_task(i):

    print("Starting robot task", i)
    while not shutdown_event.is_set():
        # Run some robot task...

        print("Running robot task", i)
        time.sleep(1)
        # Print shut down message
        print("Shutting down robot task", i)
        # Test exception
    if i == 1:
        raise Exception("Robot task 1 raised an exception")
'''


if __name__ == "__main__":
    
    '''
    futures = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        for i in range(3):
            # Spawn task threads
            future = executor.submit(robot_task, i)
            # Add exception call back
            future.add_done_callback(handle_exception)
            futures.append(future)'''

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        eSensor = executor.submit(sensor_function, sensor_values_bus, 1)
        eInterpreter = executor.submit(interpreter_function,sensor_values_bus, interpreter_bus,1)
        eController = executor.submit(controller_function, interpreter_bus, 1)

        eSensor.add_done_callback(handle_exception)
        eInterpreter.add_done_callback(handle_exception)
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