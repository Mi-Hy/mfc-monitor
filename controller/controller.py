import subprocess
import time
from datetime import datetime, timedelta, timezone
import yaml
import os
from lib.scheduler import Scheduler
from filelock import FileLock
from lib.influxdb import *
from lib.configuration import *

import socket
import threading
import json

# Booleans
socket_server_started = False

# Config
system_script_path = "system.py"
voltage_script_path = "voltages.py"
load_script_path = "load.py"

# Initial start time
start_time = datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

# Initial interval
system_interval = timedelta(hours=0, minutes=1, seconds=0)
voltage_interval = timedelta(hours=0, minutes=1, seconds=0)
load_interval = timedelta(hours=0, minutes=1, seconds=0)

# Countdown variables in YAML
system_countdown_vars = ["temp_countdown_hour", "temp_countdown_minute", "temp_countdown_second"]
voltage_countdown_vars = ["voltage_countdown_hour", "voltage_countdown_minute", "voltage_countdown_second"]
load_countdown_vars = ["load_countdown_hour", "load_countdown_minute", "load_countdown_second"]

# Init schedulers
system_scheduler = Scheduler("System", system_script_path, start_time, system_interval, system_countdown_vars, False)
voltage_scheduler = Scheduler("Voltage", voltage_script_path, start_time, voltage_interval, voltage_countdown_vars, False)
load_scheduler = Scheduler("Load", load_script_path, start_time, load_interval, load_countdown_vars, False)

# def wait_for_network(host="8.8.8.8", port=53, timeout=3, retry_interval=5, max_wait=300):
#     """
#     Wacht tot netwerk beschikbaar is of tot max_wait seconden verstreken zijn.
#     """
#     start_time = time.time()
    
#     while True:
#         try:
#             socket.setdefaulttimeout(timeout)
#             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#                 sock.connect((host, port))
#             print("✅ Netwerkverbinding is beschikbaar.")
#             return True
#         except socket.error:
#             elapsed = time.time() - start_time
#             if elapsed > max_wait:
#                 print("❌ Timeout: netwerk niet beschikbaar binnen de toegestane tijd.")
#                 return False
#             print(f"⏳ Geen verbinding. Probeer opnieuw in {retry_interval} seconden...")
#             time.sleep(retry_interval)


def update_system_timer_settings(settings):
    system_interval = timedelta(hours=settings["system_interval_hour"], minutes=settings["system_interval_minute"], seconds=settings["system_interval_second"])

    system_scheduler.update_parameters(start_time, system_interval)

def update_voltage_timer_settings(settings):
    voltage_interval = timedelta(hours=settings["voltage_interval_hour"], minutes=settings["voltage_interval_minute"], seconds=settings["voltage_interval_second"])

    voltage_scheduler.update_parameters(start_time, voltage_interval)

def update_load_timer_settings(settings):
    load_interval = timedelta(hours=settings["load_interval_hour"], minutes=settings["load_interval_minute"], seconds=settings["load_interval_second"])

    load_scheduler.update_parameters(start_time, load_interval)

def main_loop():

    #   Load YAML config file
    config = retrieve_yaml_file()

    #   Init auto measurement settings
    update_system_timer_settings(config["timer_settings"])
    update_voltage_timer_settings(config["timer_settings"])
    update_load_timer_settings(config["timer_settings"])

    #   Check device mode and change power settings
    # check_device_mode(config)

    #   Initialisation done
    print("Init done")

    system_scheduler.start()
    voltage_scheduler.start()
    load_scheduler.start()

    while 1:
        print(f"System remaining time: {system_scheduler.get_remaining_time()}")
        print(f"Voltage remaining time: {voltage_scheduler.get_remaining_time()}")
        print(f"Load remaining time: {load_scheduler.get_remaining_time()}")
        time.sleep(10)


if __name__ == "__main__":

    # threading.Thread(target=start_server, daemon=True).start()
    
    main_loop()