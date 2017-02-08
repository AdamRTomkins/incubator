from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
from smartplug import SmartPlug

class AppSession(ApplicationSession):

    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):

        # create plug object for plug with IP 172.16.100.75, login admin and password 1234
        p = SmartPlug("192.168.1.96", ('admin', '1234'))

        self.log.info("power plug state: {state}",state=p.state)

        # REGISTER a procedure for remote calling
        #
        def on():
            p.state = "ON"
            return p.state

        yield self.register(on, 'com.power.on')
        self.log.info("procedure on() registered")

        # REGISTER a procedure for remote calling
        #
        def state():
            return p.state

        yield self.register(state, 'com.power.state')
        self.log.info("procedure state() registered")

        # REGISTER a procedure for remote calling
        #
        def off():
            p.state = "OFF"
            return p.state

        yield self.register(off, 'com.power.off')
        self.log.info("procedure off() registered")

        old_state = p.state

        while True:
            power_state = p.state
            if old_state != power_state:
                yield self.publish('com.power.update',power_state)
                self.log.info("published to 'state' with state {state}", state=power_state)
                old_state = power_state
            yield sleep (5)	
