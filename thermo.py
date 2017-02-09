from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

import os
import time

import numpy as np

from DS18B20 import read_temp

#os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

os.system('modprobe w1-gpio pullup=1')
os.system('modprobe w1-therm strong_pullup=1')

class AppSession(ApplicationSession):

    log = Logger()

    ids =  {     "t1": "28-031671265dff",
                 "t2": "28-051673a2a8ff"}

    memory = 0

    @inlineCallbacks
    def onJoin(self, details):
        
        # PUBLISH and CALL every second .. forever
        #
        while True:

            # PUBLISH an event
            #
            #try:
            msg = []
            
            for id in self.ids:
                msg.append(float(read_temp(self.ids[id])))
            

            if abs(np.mean(msg) - self.memory) > 0.25:
                yield self.publish('com.thermo.temp', msg)
                self.log.info("published to 'temp' with message {msg}",
                          msg=msg)
                self.memory = np.mean(msg)

            yield sleep(1)
	    #except:

	    #yield sleep(100)
