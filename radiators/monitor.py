"""
Monitor radiators using tinytuya and append to log file.
"""

import json
from time import sleep
from datetime import datetime
import tinytuya # pylint: disable=import-error


def run():
    """Start monitoring radiator temperatures and append to log file."""
    display = True
    logfile = 'temperatures.csv'
    sampling_interval = 60.0

    # Get stored devices list and filter for thermostats
    with open('devices.json', 'r', encoding='utf-8') as file:
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
                logstr = (f"{now},"
                          f"{device['name']},"
                          f"{target_temp},"
                          f"{current_temp},"
                          f"{radiator_on}")
                with open(logfile, 'a', encoding='utf-8') as myfile:
                    myfile.write(logstr + "\n")
                if display:
                    print(logstr)
            except 'dps': # pylint: disable=catching-non-exception
                if display:
                    print(f"{now},{device['name']} - fail")
        sleep(sampling_interval)


if __name__ == "__main__":
    run()
