from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

import numpy as np

import time

class AppSession(ApplicationSession):

    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):

	status = {
                "time" : int(time.time()),
		"control" : False,
		"min_temp" : 20,
		"max_temp" : 25,	
		"upper_temp" : 0,	
		"cur_temp" : 0,
		"power": "NA"
        }

        # SUBSCRIBE to a topic and receive events
        # Listen for temperature Updates

        @inlineCallbacks
        def modulate_temperature():
            print status['control']
            if status['control']:
                if status["upper_temp"] >= status["max_temp"]:
                    if status['power'] != 'OFF':
                        res = yield self.call('com.power.off')
                        self.log.info("Power set to: {res}", res=res)
                        status["power"] = res
                        yield update()
                elif status["cur_temp"] <= status["min_temp"]:
                    if status['power'] != 'ON':
                        res = yield self.call('com.power.on')
                        status["power"] = res
                        self.log.info("Power set to: {res}", res=res)
                        yield update()
                elif status["cur_temp"] >= status["max_temp"]:
                    if status['power'] != 'OFF':
                        res = yield self.call('com.power.off')
                        self.log.info("Power set to: {res}", res=res)
                        status["power"] = res
                        yield update()

        @inlineCallbacks 
        def update():
            status["time"] = int(time.time())
	    yield self.publish('com.brain.update', status)
            self.log.info("published to 'update' with status {status}", status = status)

	@inlineCallbacks
        def onTempUpdate(msg):
            self.log.info("event for 'onTempUpdate' received: {msg}", msg=msg)
	    # Add all the temperatures
            average_temp = np.mean(msg)
            max_temp = np.max(msg)

            status['cur_temp'] = round(average_temp,1)
            status['upper_temp'] = round(max_temp,1)

            yield modulate_temperature()
            update()

        yield self.subscribe(onTempUpdate, 'com.thermo.temp')

        # SUBSCRIBE to a topic and receive events
        # Listen for Setting Min/Max Updates

	@inlineCallbacks
        def onLimitUpdate(msg):
	    status["min_temp"] = msg['min']
	    status["max_temp"] = msg['max']
            self.log.info("event for 'onLimitUpdate' received: {msg}", msg=msg)
	    yield self.publish('com.brain.update', status)
            self.log.info("published to 'update' with status {status}", status = status)
	    
        yield self.subscribe(onLimitUpdate, 'com.thermo.limit')

	@inlineCallbacks
	def onPowerUpdate(msg):
	    status["power"] = msg
            self.log.info("event for 'onPowerUpdate' received: {msg}", msg=msg)
	    yield self.publish('com.brain.update', status)
            self.log.info("published to 'update' with status {status}", status = status)
	    
        yield self.subscribe(onPowerUpdate, 'com.power.update')



        # REGISTER
        # Set new maximum Temperature
	@inlineCallbacks
        def setMax(max):
            self.log.info("setMax called with {max}", max=max)
            status['max_temp'] = int(max)
            yield update()

        yield self.register(setMax, 'com.brain.set_max')
        self.log.info("procedure setMax() registered")

        # REGISTER
        # Set new minimum Temperature
	@inlineCallbacks
        def setMin(min):
            self.log.info("setMin called with {min}", min=min)
	    status["min_temp"] = int(min)
            yield update()

        yield self.register(setMin, 'com.brain.set_min')
        self.log.info("procedure setMin() registered")

        # REGISTER
        # Set Power On
	@inlineCallbacks
        def set_power_on():
            self.log.info("set_power_on called")
            try:
                res = yield  self.call('com.power.on')
                self.log.info("on() called with result: {result}",
                              result=res)
            except ApplicationError as e:
                # ignore errors due to the frontend not yet having
                # registered the procedure we would like to call
                if e.error != 'wamp.error.no_such_procedure':
                    raise e

        yield self.register(set_power_on, 'com.brain.power_on')
        self.log.info("procedure set_power_on() registered")

        # REGISTER
        # Set Power Off

	@inlineCallbacks
        def set_power_off():
            self.log.info("set_power_off called")
            try:
                res = yield self.call('com.power.off')
                self.log.info("off() called with result: {result}",
                              result=res)
            except ApplicationError as e:
                # ignore errors due to the frontend not yet having
                # registered the procedure we would like to call
                if e.error != 'wamp.error.no_such_procedure':
                    raise e

        yield self.register(set_power_off, 'com.brain.power_off')
        self.log.info("procedure set_power_off() registered")

        @inlineCallbacks
        def get_status():
            self.log.info("get_status called")
            yield update()

        yield self.register(get_status, 'com.brain.status')
        self.log.info("procedure get_status() registered")

 
        
        @inlineCallbacks
        def set_control_off():
	    status["control"] = False
            self.log.info("set_control_off called")
            yield update()

        yield self.register(set_control_off, 'com.brain.control_off')
        self.log.info("procedure set_control_off() registered")

        @inlineCallbacks
        def set_control_on():
	    status["control"] = True
            self.log.info("set_control_on called")
            yield update()

        yield self.register(set_control_on, 'com.brain.control_on')
        self.log.info("procedure set_control_on() registered")

