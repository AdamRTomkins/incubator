import os
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


def read_temp(temp_id):
    def temp_raw(temp_sensor):

        f = open(temp_sensor, 'r')
        lines = f.readlines()
        f.close()
        return lines

    temp_sensor = "/sys/bus/w1/devices/%s/w1_slave" % temp_id

    lines = temp_raw(temp_sensor)
    print lines[0].strip()[-3:]
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw(temp_sensor)
    temp_output = lines[1].find('t=')

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

if __name__ == "__main__":
    while True:
        print(read_temp("28-051673a2a8ff"))
        time.sleep(1)


