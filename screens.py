import pygame
import time
import os
from threading import Timer

# CONSTANTS
SCREEN_SIZE = (480,320)


# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Pill Dispenser")
clock = pygame.time.Clock()

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

    def input(self, sm):
        pass

    def update(self, sm):
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

    def input(self):

        if len(self.screens) > 0:
            self.screens[-1].input(self)

    def update(self):

        if len(self.screens) > 0:
            self.screens[-1].update(self)

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
    
    def input(self, sm):
        pass
    
    def update(self, sm):
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
        self.screen_manager.push(Wifi_SSID_Screen())


class Wifi_SSID_Screen(BaseScreen):
    name = "WiFi SSID Input Screen"
    def input(self, sm):
        pass
    def update(self, sm):
        pass
    def draw(self, sm):
        pass

if __name__ == '__main__':

    Running = True

    sm = ScreenManager()

    # push the initial screen to the system
    sm.push(SplashScreen())

    while Running:

        # allows use for the "X" button to quit.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sm.clear()

        # if the screen manager is empty, then the system
        # automatically quits
        if sm.is_empty():
            Running = False

        sm.input()
        sm.update()
        sm.draw()

        #print("sleeping...")
        time.sleep(0.1)
