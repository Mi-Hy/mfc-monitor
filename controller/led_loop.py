from lib.ep_handler import *
from lib.influxdb import *
from lib.tca9554 import TCA9554
from lib.configuration import *

io = TCA9554()

CELLS = 8

value_mapper = {0: 3, 1: 2, 2: 1, 3: 0, 4: 7, 5: 6, 6: 5, 7: 4}

if __name__ == "__main__":

    # Get config file
    config = retrieve_yaml_file()

    while(config['status']['load'] == 1):
        #   Debug message
        print("[Voltage] ⏳ Waiting for load test to complete...")
        
        #   Wait 5 seconds before checking again
        time.sleep(5)

        #   Update config file to indicate voltage test is running
        config = retrieve_yaml_file()

    update_yaml_flag("status", "voltage", 1)

    ep_change_resistance(0)

    time.sleep(3)

    # while True:

    voltage_buffer = []

    while True:

        for i in range(CELLS):
            io.set_output(value_mapper.get(i, i), 1)

            time.sleep(1.5)


            time.sleep(1.5)

            io.set_output(value_mapper.get(i, i), 0)

            time.sleep(1.5)
    

