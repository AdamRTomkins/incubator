from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

import os
import time

#os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

os.system('modprobe w1-gpio pullup=1')
os.system('modprobe w1-therm strong_pullup=1')

class AppSession(ApplicationSession):

    
    log = Logger()


    def temp_raw(self):
    	temp_sensor = "/sys/bus/w1/devices/28-051673a2a8ff/w1_slave"

        f = open(temp_sensor, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.temp_raw()
        temp_output = lines[1].find('t=')

        if temp_output != -1:
            temp_string = lines[1].strip()[temp_output+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c


    @inlineCallbacks
    def onJoin(self, details):

        # PUBLISH and CALL every second .. forever
        #
        while True:

            # PUBLISH an event
            #
            try:
                t = self.read_temp()
                yield self.publish('com.thermo.temp', t)
                self.log.info("published to 'temp' with value {t}",
                          t=t)
                yield sleep(1)
	    except:
		yield sleep(100)
