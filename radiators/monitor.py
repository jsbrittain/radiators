import tinytuya
import json
from time import sleep
from datetime import datetime

display = True
logfile = 'temperatures.csv'
sampling_interval = 60.0

# Get stored devices list and filter for thermostats
with open("devices.json", "r") as file:
    devices = json.load(file)
devices = [d for d in devices if d['product_name'] == 'Smart RM']

while True:
    for device in devices:
        try:
            d = tinytuya.OutletDevice(
                    device['id'],
                    device['ip'],
                    device['key'],
                    )
            d.set_version(3.3)
            data = d.status()
            now = datetime.now()
            info = data['dps']
            current_temp = info['3']/10
            target_temp = info['2']/10
            radiator_on = info['102']
            '''
            entry = {
                    'datetime': now,
                    'device_name': device['name'],
                    'current_temp': current_temp,
                    'target_temp': target_temp,
                    'data': data,
                    }
            '''
            logstr = f"{now},{device['name']},{target_temp},{current_temp},{radiator_on}"
            with open(logfile, "a") as myfile:
                myfile.write(logstr + "\n")
            if display:
                print(logstr)
        except:
            if display:
                print(f"{now},{device['name']} - fail")
    sleep(sampling_interval)
