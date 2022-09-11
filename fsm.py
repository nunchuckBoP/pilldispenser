from transitions import Machine
from threading import Timer

class PillDispenser(object):

    states = [
        'asleep', 'splash_screen', 'wifi_ssid', 'wifi_security', 'loading_liquid_instructions', 'loading_pill_instructions',
        'loading_liquid', 'loading_pill', 'schedule_setup', 'checking_schedule', 'med_time', 'deliver_meds'
        'waiting_cup_present','waiting_cup_clear',
    ]

    def __init__(self, serial_number):

        self.timer = None
        self.timeout_timer = None
        self.timer_pre = 10.0
        self.timeout_pre = 300.0

        self.machine = Machine(model=self, states=PillDispenser.states, initial='asleep')

        # add some transitions.
        self.machine.add_transition(trigger='wake_up', source='asleep', dest='splash_screen', before=self.reset_timers, after=self.start_timer)
        self.machine.add_transition(trigger='timer_complete', source='splash_screen', dest='wifi_ssid', before=self.reset_timers)
        self.machine.add_transition(trigger='wifi_ssid_complete', source='wifi_ssid', dest='wifi_security', before=self.reset_timers, after=self.start_timeout)
        self.machine.add_transition(trigger='timeout_complete', source='wifi_security', dest='wifi_ssid', before=self.reset_timers)
        self.machine.add_transition(trigger='wifi_security_complete', source='wifi_security', dest='loading_liquid', before=self.reset_timers)

        # instructions
        self.machine.add_transition(trigger='loading_liquid_complete', source='loading_liquid', dest='loading_pill_instructions', before=self.reset_timers)
        self.machine.add_transition(trigger='loading_pill_instructions_complete', source='loading_pill_instructions', dest='loading_pill', before=self.reset_timers)
        self.machine.add_transition(trigger='loading_pill_complete', source='loading_pill', dest='schedule_setup', before=self.reset_timers)

        # go back to config / loading states
        self.machine.add_transition(trigger='schedule_complete', source='schedule_setup', dest='checking_schedule', before=self.reset_timers)
        self.machine.add_transition(trigger='load_pressed', source='checking_schedule', dest='loading_pill_instructions', before=self.reset_timers)
        self.machine.add_transition(trigger='config_pressed', source='checking_schedule', dest='wifi_ssid', before=self.reset_timers)
        
        # medication deliveries
        self.machine.add_transition(trigger='med_time', source='checking_schedule', dest='waiting_cup_present', before=self.reset_timers)
        self.machine.add_transition(trigger='cup_on', source='waiting_cup_present', dest='deliver_meds',before=self.reset_timers)
        self.machine.add_transition(trigger='meds_delivered', source='deliver_meds', dest='waiting_cup_clear', before=self.reset_timers)
        self.machine.add_transition(trigger='cup_clear', source='waiting_for_cup_clear', dest='checking_schedule', before=self.reset_timers)
        
    # end init

    def reset_timers(self):
        
        if self.timer is not None:

            print("Canceling self.timer")
            self.timer.cancel()
            self.timer = None
        
        if self.timeout_timer is not None:

            print("Canceling self.timeout_timer")
            self.timeout_timer.cancel()
            self.timeout_timer = None

    def start_timer(self):

        # reset the running timers if they
        # exist
        self.reset_timers()
        
        print("FSM: Starting %s second timer..." % self.timer_pre)
        self.timer = Timer(interval=self.timer_pre, function=self.timer_complete_delegate)
        self.timer.start()

    def start_timeout(self):

        # reset the running timers if they 
        # exist
        self.reset_timers()
        
        print("FSM: Starting %s second timeout timer..." % self.timeout_pre)
        self.timeout_timer = Timer(interval=self.timeout_pre, function=self.timeout_complete_delegate)
        self.timeout_timer.start()

    def timer_complete_delegate(self):
        self.timer = None
        self.timer_complete()

    def timeout_complete_delegate(self):
        self.timeout_timer = None
        self.timeout_complete()

    def set_timer(self, interval):
        print("Setting timer to %s seconds." % interval)
        self.timer_pre = interval

    def set_timeout(self, interval):
        print("Setting timeout timer to %s seconds." % interval)
        self.timeout_pre = interval

# end class