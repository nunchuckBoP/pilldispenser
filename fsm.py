from transitions import Machine
from threading import Timer

class PillDispenser(object):

    states = [
        'asleep', 'splash_screen', 'wifi_ssid', 'wifi_security', 'loading_liquid_instructions', 'loading_pill_instructions',
        'loading_liquid', 'loading_pill', 'schedule_setup', 'checking_schedule', 'med_time', 'deliver_meds'
        'waiting_cup_present','waiting_cup_clear',
    ]


    def __init__(self, serial_number):

        self.machine = Machine(model=self, states = PillDispenser.states, initial='asleep')

        # add some transitions.
        self.machine.add_transition(trigger='wake_up', source='asleep', dest='splash_screen')
        self.machine.add_transition(trigger='timer_complete', source='splash_screen', dest='wifi_ssid')
        self.machine.add_transition(trigger='wifi_ssid_complete', source='wifi_ssid', dest='wifi_security')
        self.machine.add_transition(trigger='timeout_complete', source='wifi_security', dest='wifi_ssid')

        # instructions
        self.machine.add_transition(trigger='loading_liquid_complete', source='loading_liquid', dest='loading_pill_instructions')
        self.machine.add_transition(trigger='loading_pill_instructions_complete', source='loading_pill_instructions', dest='loading_pill')
        self.machine.add_transition(trigger='loading_pill_complete', source='loading_pill', dest='schedule_setup')

        # go back to config / loading states
        self.machine.add_transition(trigger='schedule_complete', source='schedule_setup', dest='checking_schedule')
        self.machine.add_transition(trigger='load_pressed', source='checking_schedule', dest='loading_pill_instructions')
        self.machine.add_transition(trigger='config_pressed', source='checking_schedule', dest='wifi_ssid')
        
        # medication deliveries
        self.machine.add_transition(trigger='med_time', source='checking_schedule', dest='waiting_cup_present')
        self.machine.add_transition(trigger='cup_on', source='waiting_cup_present', dest='deliver_meds')
        self.machine.add_transition(trigger='meds_delivered', source='deliver_meds', dest='waiting_cup_clear')
        self.machine.add_transition(trigger='cup_clear', source='waiting_for_cup_clear', dest='checking_schedule')
        
    # end init
# end class