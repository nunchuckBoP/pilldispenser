import pygame
import time
import os
from pygame_vkeyboard import *
from threading import Timer

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

class BaseComponent(object):
    def input(self, events):
        pass
    def update(self, events):
        pass
    def draw(self, screen_manager):
        pass

class Button(BaseComponent):

    # private variables
    __border_width__ = 2

    def __init__(self, callback=None, x=0, y=0, width=120, height=40, text="Button"):
        
        # public variables
        self.x = int(x)
        self.y = int(y)
        self.width = width
        self.height = height
        self.base_font = pygame.font.Font(None, 21)
        self.text = text
        self.pressed = False
        self.callback = callback

        self.black_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.border_rect = pygame.Rect(self.x + 1, self.y + 1, self.width-2, self.height-2)

        self.button_rect = pygame.Rect(self.x + 1 + self.__border_width__, \
            self.y + 1 + self.__border_width__, \
            self.width - 2 - (self.__border_width__ * 2), \
            self.height - 2 - (self.__border_width__ * 2) \
        )

        self.text_surface = self.base_font.render(text, True, pygame.Color(COLOR_BLACK))

    def input(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(e.pos):
                    self.pressed = True
                else:
                    self.pressed = False
            elif e.type == pygame.MOUSEBUTTONUP:
                self.pressed = False

    def draw(self, surface):

        # draw the black rectangle
        pygame.draw.rect(surface, pygame.Color(COLOR_BLACK), self.black_rect)
        
        # draw the inner rect
        if not self.pressed:
            pygame.draw.rect(surface, pygame.Color('azure4'), self.border_rect)
            pygame.draw.rect(surface, pygame.Color('azure3'), self.button_rect)
        else:
            pygame.draw.rect(surface, pygame.Color('blue'), self.border_rect)
            pygame.draw.rect(surface, pygame.Color('blue'), self.button_rect)

        # blit the text surface
        text_x = self.button_rect.x + (self.button_rect.width / 2) - (self.text_surface.get_rect().width / 2)
        text_y = (self.button_rect.y + (self.button_rect.height / 2)) - (self.text_surface.get_rect().height / 2)
        surface.blit(self.text_surface, (text_x, text_y))

class InputField(object):
    def __init__(self, width=200, height=32, justification="center", y=40, border_width=2):

        self.x = int((SCREEN_SIZE[0] / 2) - (width / 2))
        self.y = y
        self.base_font = pygame.font.Font(None, 21)
        self.width = width
        self.height = height
        self.active_color = pygame.Color('lightskyblue3')
        self.passive_color = pygame.Color('aliceblue')
        self.active = True
        self.user_text = ''
        self.border_width = border_width
        self.label_text = ''

        self.border_rect = pygame.Rect(self.x - self.border_width, self.y - self.border_width, \
                                        self.width + (self.border_width*2), self.height + (self.border_width*2))

        self.input_rect = pygame.Rect(self.x, self.y, \
                                        self.width, self.height)

    def set_label_text(self, text):
        self.label_text = text

    def set_user_text(self, text):
        self.user_text = text
    
    def input(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(e.pos):
                    self.active = True

    def update(self, events):
        pass

    def draw(self, surface):
        
        # draws the label
        label = self.base_font.render(self.label_text, True, pygame.Color(COLOR_BLACK))
        label_x = (SCREEN_SIZE[0] / 2) - (label.get_rect().width / 2)
        label_y = self.y - self.height
        surface.blit(label, (label_x, label_y))

        # draws the border rectangle
        pygame.draw.rect(surface, pygame.Color(COLOR_BLACK), self.border_rect)

        # draws the input rectangle
        if self.active:
            pygame.draw.rect(surface, self.active_color, self.input_rect)
        else:
            pygame.draw.rect(surface, self.passive_color, self.input_rect)
        
        # draws the text surface
        self.text_surface = self.base_font.render(self.user_text, True, pygame.Color(COLOR_BLACK))
        surface.blit(self.text_surface, (self.input_rect.x+5, self.input_rect.y+5))

class OnLoopTimer(object):
    # OnLoopTimer, is not on a separate thread
    # as the main. Every time "loop" is called it
    # compares the start time with the current time
    # If the delta is greater than the interval, it
    # calls the callback function. The interval
    # is in seconds.
    def __init__(self, callback=None, interval=10):
        self.interval = interval
        self.started = None
        self.callback = callback
    
    def reset (self):
        self.started = time.time()

    def loop(self):
        if self.started is None:
            self.started = time.time()
        
        if (time.time() - self.started) >= self.interval:
            if self.callback is not None:
                self.callback()

    def destroy(self):
        self = None            
        

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
        self.timer = OnLoopTimer(self.timer_complete, 15)
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
        super(Wifi_SSID_Screen, self).__init__()

        layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
        self.keyboard = VKeyboard(screen, self.keyboard_consumer, layout)
        self.screen_shown = False
        self.ssid_field = InputField(width=200, height=32, justification="center", y=50, border_width=2)

        self.next_button = Button(
            callback=None, x=(SCREEN_SIZE[0] / 2) - 60, y=100, width=120, height=40, text="Next"
        )

        self.ssid_field.label_text = "Enter SSID for WiFi Connection"

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
        pass

    def draw(self, sm):

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
