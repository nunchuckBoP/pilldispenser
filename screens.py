import pygame
import os
import time
from pygame_vkeyboard import *
from components import *

# CONSTANTS
SCREEN_SIZE = (480,320)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)

# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Pill Dispenser")
clock = pygame.time.Clock()

class BaseScreen(object):
    name = "General Screen"

    def on_enter(self):
        print("Entering %s screen..." % self.name)

    def on_exit(self):
        print("Exiting %s screen..." % self.name)

    def input(self, sm, events):
        pass

    def update(self, sm, events):
        pass

    def draw(self, sm):
        pass


class ScreenManager(object):
    def __init__(self):
        self.screens = []

    def is_empty(self):
        if len(self.screens) == 0:
            return True
        else:
            return False

    def enter_screen(self):
        if len(self.screens) > 0:
            self.screens[-1].on_enter()

    def exit_screen(self):
        if len(self.screens) > 0:
            self.screens[-1].on_exit()

    def input(self, events):

        if len(self.screens) > 0:
            self.screens[-1].input(self, events)

    def update(self, events):

        if len(self.screens) > 0:
            self.screens[-1].update(self, events)

    def draw(self):

        if len(self.screens) > 0:
            self.screens[-1].draw(self)

    def push(self, screen):
        self.exit_screen()
        self.screens.append(screen)
        self.enter_screen()

    def pop(self):
        self.exit_screen()
        self.screens.pop()
        self.enter_screen()

    def set(self, screen):
        # pop all of the scenes, and then
        # push the single new screen.
        while len(self.screens) > 0:
            self.pop()
        self.push(screen)

    def clear(self):
        # gets all of the screens off of the board
        while len(self.screens) > 0:
            self.pop()

class SplashScreen(BaseScreen):
    name = "Splash Screen"

    def __init__(self):
        self.timer = OnLoopTimer(self.timer_complete, 5)
        self.image = pygame.image.load(os.path.join('resource','img','logo.jpg'), "logo").convert()
        self.screen_manager = None
    
    def input(self, sm, events):
        pass
    
    def update(self, sm, events):
        pass
    
    def draw(self, sm):

        # loop the timer class to see
        # if the timer has been completed
        self.timer.loop()
        self.screen_manager = sm

        pygame.display.flip()
        screen.blit(self.image, (0,0))
    
    def timer_complete(self):
        print("Timer Complete!")
        if self.screen_manager is not None:
            self.screen_manager.push(Wifi_SSID_Screen())
        else:
            raise Exception("timer_complete has no screen manager...")


class Wifi_SSID_Screen(BaseScreen):
    name = "WiFi SSID Input Screen"

    def __init__(self):

        layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
        self.keyboard = VKeyboard(screen, self.keyboard_consumer, layout)
        self.screen_shown = False
        self.ssid_field = InputField(width=200, height=32, justification="center", y=50, border_width=2)

        self.next_button = Button(
            callback=self.next_clicked, x=(SCREEN_SIZE[0] / 2) - 60, y=100, width=120, height=40, text="Next"
        )

        self.ssid_field.label_text = "Enter SSID for WiFi Connection"
        self.screen_manager = None

    def on_enter(self):
        pass

    def input(self, sm, events):

        self.ssid_field.input(events)
        self.next_button.input(events)

    def update(self, sm, events):
        
        #update the internal variables for the keyboard
        self.keyboard.update(events)
        self.ssid_field.update(events)
        self.next_button.update(events)

        pygame.display.update()

    def keyboard_consumer(self, text):
        if self.ssid_field.active:
            self.ssid_field.set_user_text(text)
        else:
            self.keyboard.set_text("")

    def next_clicked(self):
        if self.screen_manager is not None:
            self.screen_manager.push(Wifi_PSK_Screen(ssid=self.ssid_field.user_text))

    def draw(self, sm):

        # save the screen manager object
        self.screen_manager = sm

        if not self.screen_shown:
            # fills the screen with white
            screen.fill(COLOR_WHITE)

        # draw the input field
        self.ssid_field.draw(screen)

        # draw the next button
        self.next_button.draw(screen)

        # draw the keyboard
        self.keyboard.draw()

        # flip the display. Can only flip
        # the screen once otherwise the 
        # on-screen keyboard goes away
        if not self.screen_shown:
            pygame.display.flip()
            self.screen_shown = True


class Wifi_PSK_Screen(BaseScreen):
    name = "WiFi PSK Input Screen"

    def __init__(self, **kwargs):

        layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
        self.keyboard = VKeyboard(screen, self.keyboard_consumer, layout)
        self.screen_shown = False
        self.psk_field = InputField(width=200, height=32, justification="center", y=50, border_width=2)

        self.next_button = Button(
            callback=None, x=(SCREEN_SIZE[0] / 2) - 60, y=100, width=120, height=40, text="Next"
        )

        self.psk_field.label_text = "Enter Passphrase for WiFi Connection"

        if "ssid" in kwargs:
            self.ssid = kwargs['ssid']
            print("SSID = %s" % self.ssid)
        else:
            self.ssid = None

    def on_enter(self):
        pass

    def input(self, sm, events):

        self.psk_field.input(events)
        self.next_button.input(events)

    def update(self, sm, events):
        
        #update the internal variables for the keyboard
        self.keyboard.update(events)
        self.psk_field.update(events)
        self.next_button.update(events)

        pygame.display.update()

    def keyboard_consumer(self, text):
        if self.psk_field.active:
            self.psk_field.set_user_text(text)
        else:
            self.keyboard.set_text("")

    def next_clicked(self):
        pass

    def draw(self, sm):

        if not self.screen_shown:
            # fills the screen with white
            screen.fill(COLOR_WHITE)

        # draw the input field
        self.psk_field.draw(screen)

        # draw the next button
        self.next_button.draw(screen)

        # draw the keyboard
        self.keyboard.draw()

        # flip the display. Can only flip
        # the screen once otherwise the 
        # on-screen keyboard goes away
        if not self.screen_shown:
            pygame.display.flip()
            self.screen_shown = True

class MainScreen(BaseScreen):

    def __init__(self, **kwargs):
        
        self.components = []

    def input(self, events):
        for i in self.components:
            i.input(events)

    def update(self, events):
        for i in self.components:
            i.update(events)

    def nav_clicked(self):
        pass

    def draw(self, screen_manager):
        for i in self.components:
            i.draw(screen_manager)

if __name__ == '__main__':

    Running = True

    sm = ScreenManager()

    # push the initial screen to the system
    sm.push(SplashScreen())

    while Running:

        # allows use for the "X" button to quit.
        events = pygame.event.get()

        sm.input(events)
        sm.update(events)
        sm.draw()

        # if the screen manager is empty, then the system
        # automatically quits
        if sm.is_empty():
            Running = False

        # looks for the quit event
        for event in events:
            if event.type == pygame.QUIT:
                sm.clear()

        #print("sleeping...")
        time.sleep(0.1)
