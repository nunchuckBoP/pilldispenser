from fsm import PillDispenser
import time

if __name__ == '__main__':

        # instantiate the state machine
        fsm = PillDispenser("1")

        # prints the initial state of the machine
        print("Current State: %s" %fsm.state)

        # wake up the state machine
        fsm.wake_up()

        # keeps track of the last state
        last_state = None

        # start comparing states
        while True:

                # This if statement prints out the state every time the 
                # state of the machine changes.
                if last_state != fsm.state:
                        print("Current State: %s" % fsm.state)
                        last_state = fsm.state
                # end if

                if fsm.is_wifi_ssid():

                        # set the timeout time for the next state,
                        # not the current one
                        fsm.set_timeout(10.0)

                        # simulate the ssid complete
                        fsm.wifi_ssid_complete()

        # end while
        
        print("System Completed.")