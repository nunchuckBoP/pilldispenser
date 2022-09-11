from fsm import PillDispenser
import time

if __name__ == '__main__':

        # instantiate the state machine
        fsm = PillDispenser("1")

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

        # end while
        
        print("System Completed.")