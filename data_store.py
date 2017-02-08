from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError


class AppSession(ApplicationSession):

    log = Logger()

   

    @inlineCallbacks
    def onJoin(self, details):

        # create structure for incoming data
        # create a file writing

        # subscribe to updates

        # register a retrieve data update
        data = {}

        def onUpdate(msg):
            # add update status to a list depending on its name
            if "exp_name" not in msg:
                msg["exp_name"] = "default"
            exp = msg["exp_name"]

            #iif exp not in data:
            #    data[exp] = []

            #data[exp].append(msg)
             
            self.log.debug("event for 'onUpdate' received: {msg}", msg=msg)

        yield self.subscribe(onUpdate, 'com.brain.update')


        # REGISTER
        # get_data
        def get_data():
            self.log.debug("get_data called")
            return data

        yield self.register(get_data, 'com.data.get_data')
        self.log.info("procedure get_data() registered")

        @inlineCallbacks
        def set_recording_on():
            pass

        yield self.register(set_recording_on, 'com.data.recording_on')
        self.log.info("procedure set_recording_on() registered")


        @inlineCallbacks
        def set_recording_off():
            pass

        yield self.register(set_recording_off, 'com.data.recording_off')
        self.log.info("procedure set_recording_off() registered")


