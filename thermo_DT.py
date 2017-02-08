from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

import os
import time

import DHT11

os.system('modprobe w1-gpio')

class AppSession(ApplicationSession):

    
    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):
        old_t = 0
        old_h  = 0
        # PUBLISH and CALL every second .. forever
        #
        while True:

            # PUBLISH an event
            #
            try:
                res = DHT11.check_tmp()
                if "Error" in res: 
                    pass
                    #self.log.info("DHT11 read error {res}", res =res)
                elif res['t'] != old_t or res['h'] != old_h:
                    yield self.publish('com.thermo.temp', res)
                    self.log.info("published to 'temp' with value {t}",t=res)
                    old_t = res['t']
                    old_h = res['h']
                yield sleep(1)
	    except:
		yield self.publish('com.thermo.error')
                self.log.info("published to 'error'")
		yield sleep(10)
