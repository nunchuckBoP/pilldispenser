
# i2c load cell using adafruit adc
# https://www.adafruit.com/product/4538
from cedargrove_nau7802 import NAU7802

# adafruit motor kit library
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

class BaseDevice(object):
    def __init__(self, address):
        self.address = address

    def setup(self):pass
    def loop(self):pass

# Load cell for reading cup / pill weight
class LoadCell(BaseDevice):

    def __init__(self, address=0x2a):
        super(LoadCell, self).__init__(address)
        self.device = NAU7802(board.I2C(), address=self.address, active_channels=2)
        self.value = 0.0

    def setup(self):
        super(LoadCell, self).setup()
        self.zero_scale()
    
    def read_raw_value(self, channel=1, samples=100):
        count = 0
        sample_sum = 0
        
        if channel == 1:
            self.device.channel = 1
        elif channel == 2:
            self.device.channel = 2
        else:
            print("Channel requested: %s" % channel)
            raise ValueError("Invalid channel number.")

        while count <= samples:
            if self.device.available:
                sample_sum = sample_sum + self.device.read()
                count = count + 1
            # end if
        # end loop
        return int(sample_sum / samples)

    def zero_scale(self):

        self.device.channel = 1
        self.read_raw_value(channel=1, samples=100)
        self.device.channel = 2
        self.read_raw_value(channel=2, samples=100)

    def loop(self):
        
        # read and update the value
        self.value = self.read_raw_value(samples=100)


# pill motor and pump are controlled via an
# adafruit motor control hat
class PillMotor(BaseDevice):
    pass


class MotorControl(BaseDevice):
    
    def __init__(self, address=0x60):
        super(MotorControl, self).__init__(address)
        self.kit = MotorKit(self.address, i2c=board.I2C())

class PillWheel(object):
    def __init__(self, motor_control_class, motor_number=1, steps_per_rev=200):

        self.control = motor_control_class
        if motor_number == 1:
            self.device = self.control.kit.stepper1
        elif motor_number == 2:
            self.device = self.control.kit.stepper2
        else:
            raise ValueError("Invalid motor number.")

        self.direction = stepper.FORWARD # set the initial direction to forward
        self.steps_per_rev = steps_per_rev
        
        # private variables
        self.__step_count__ = 0
        self.__count_total__ = 0
        self.__moving__ = False
        self.__motor_number__ = motor_number

    def isMoving(self):
        return self.__moving__

    def setup(self):
        # releases power to the stepper motor
        self.device.release()
        self.direction = stepper.FORWARD

    def move(self, revolutions):
        # revolutions can be positive, negative, or a fraction
        # of 

        # calculates the number of steps to move
        steps = self.revolutions / self.steps_per_rev

        # if the steps are negative set the direction to backward
        if steps < 0:
            direction = stepper.BACKWARD
            steps = steps * -1 # turn steps back to positive
        else:
            direction = stepper.FORWARD
        # end if

        # actually move the motor
        for i in range(steps):
            self.device.onestep(style=stepper.MICROSTEP)

    def move(self, revolutions):

        if not self.isMoving():
            step_total = revolutions / self.steps_per_rev
            
            if step_total < 1:
                self.direction = stepper.BACKWARD
            else:
                self.direction = stepper.FORWARD
            # end if
            
            self.__count_total__ = abs(step_total)
            self.__moving__ = True

    def __move_complete__(self):
        self.__step_count__ = 0
        self.__count_total__ = 0
        self.__moving__ = False

    def status(self):
        status =  {
            "Motor":"Motor" + self.__motor_number__,
            "isMoving":self.isMoving(),
        }
        print(status)
        return status

    def loop(self):
        super(PillMotor, self).loop()

        if self.isMoving() and self.__step_count__ < self.__count_total__:
            self.device.onestep(direction=self.direction, style=stepper.MICROSTEP)
            self.__step_count__ = self.__step_count__ + 1

        elif self.isMoving() and self.__step_count__ == self.__count_total__:
            self.device.onestep(direction=self.direction, style=stepper.MICROSTEP)
            self.__move_complete__()

        else:
            pass # nothing to do
        # end if


class Pump(object):

    def __init__(self, motor_control_class, motor_number=1, throttle=0.75, dribble=0.25):
        
        # sets the control object to the given motor
        # control class
        self.control = motor_control_class
        
        # determines the device bases off of the motor
        # number given
        if motor_number == 1:
            self.device = self.control.kit.motor1
        elif motor_number == 2:
            self.device = self.control.kit.motor2
        elif motor_number == 3:
            self.device = self.control.kit.motor3
        elif motor_number == 4:
            self.device = self.control.kit.motor4
        else:
            raise ValueError("Invalid motor number")

        self.throttle = throttle
        self.dribble = dribble

        self.__liquid_total__ = 0.0
        self.__liquid_count__ = 0.0
        self.__liquid_preact__ = 1.0
        self.__full_rate_sec_per_mL__ = 20
        self.__dribble_sec_per_mL__ = 300
        self.__on_time__ = 0
        self.__running__ = False
        self.__full_rate_time__ = 0
        self.__dribble_time__ = 0
        self.__total_deliver_time__ = 0

    def setup(self, fast_rate_sec_to_ml=20, dribbe_rate_sec_to_mL=300):

        # to start, make the throttle zero
        self.device.throttle = 0.0

        self.__full_rate_sec_per_mL__ = fast_rate_sec_to_ml
        self.__dribble_sec_per_mL__ = dribbe_rate_sec_to_mL

    def isRunning(self):
        return self.__running__

    def deliver_liquid(self, mL):

        # calculate how many seconds (milliseconds)
        # to run the pump at full speed, and how many
        # seconds to run the pump at dribble speed
        if not self.isRunning():
            self.__liquid_total__ = mL
            
            full_rate_liquid = self.__liquid_total__ - self.__liquid_preact__
            
            # full rate time in milliseconds
            self.__full_rate_time__ = (self.__full_rate_sec_per_mL__ / full_rate_liquid) * 1000

            # dribble time in milliseconds
            self.__dribble_time__ = (self.__dribble_sec_per_mL__ / self.__liquid_preact__) * 1000

            # total deliver time
            self.__total_deliver_time__ = self.__full_rate_time__ + self.__dribble_time__

            # saves the time that the pump was started
            self.__on_time__ = time.time()

            self.__running__ = True

    def loop(self):

        if self.isRunning():
            
            # calculate the delta time
            delta_time = time.time() - self.__on_time__

            # if the delta time is less than the full rate time, then run the pump
            # at full rate throttle. If it is between full rate time and total time,
            # run the pump at the dribble time.
            # If it is at or past the full deliver time, than shut the pump off.
            if delta_time < self.__full_rate_time__:
                self.device.throttle = self.throttle
            elif delta_time >= self.__full_rate_time__ and delta_time < self.__total_deliver_time__:
                self.device.throttle = self.dribble
            elif delta_time >= self.__total_deliver_time__:
                self.device.throttle = 0.0

        else:
            self.device.throttle = 0.0

if __name__ == '__main__':

    b1 = MotorControl(address=0x60)
    b2 = MotorControl(address=0x61)
    lc = LoadCell()

    p1 = Pump(b1, 1)
    s2 = PillWheel(b1, 2, 200)

    p3 = Pump(b2, 1)
    s4 = PillWheel(b2, 2, 200)

    lc.setup()
    p1.setup()
    s2.setup()
    p3.setup()
    s4.setup()

    t1 = time.time()
    r = lc.read_raw_value()
    t2 = time.time()
    print("Raw Value: %s\tTTR: %s" % (r, t2-t1))
