#!/usr/bin/env python3
import os
from ina219 import INA219, DeviceRangeError
from time import sleep
from datetime import datetime

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 2.0
ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V)

time_stamp = 0
with open('log_file.csv', 'w') as log_file:
    print('time (h),bus_voltage (V),bus_current (mA),power (mW)',
          file=log_file)

while 1:
    if datetime.now().hour < 5:
        sleep(30*60)

    elif datetime.now().hour > 13:
        day_file = "mesures-" + datetime.today().strftime("%d-%m-%y") + ".csv"
        if os.path.isfile('log_file.csv') and not os.path.isfile(day_file):
            os.popen('cp log_file.csv '+day_file)
            with open('log_file.csv', 'w') as log_file:
                print('time (h),bus_voltage (V),bus_current (mA),power (mW)',
                      file=log_file)
        time_stamp = 0
        sleep(30*60)

    else:

        with open("log_file.csv", 'a') as log_file:
            try:
                print(time_stamp, end=',', file=log_file)
                print('{0:0.2f}'.format(ina.voltage()), end=',', file=log_file)
                print('{0:0.2f}'.format(ina.current()), end=',', file=log_file)
                print('{0:0.2f}'.format(ina.power()), file=log_file)
            except DeviceRangeError as e:
                # Current out of device range with specified shunt resister
                print(e, file=log_file)
                exit()

            time_stamp += 0.25
        sleep(15*60)
