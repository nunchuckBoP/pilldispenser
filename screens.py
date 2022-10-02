import pygame
import time
from threading import Timer

# CONSTANTS
SCREEN_SIZE = (480,320)


# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Pill Dispenser")
clock = pygame.time.Clock()

class OnLoopTimer(object):
    # interval is in seconds
    def __init__(self, callback=None, interval=10):
        self.interval = interval
        self.started = None
        self.callback = callback
    def loop(self):
        if self.started is None:
            self.started = time.time()
        
        if (time.time() - self.started) >= self.interval:
            if self.callback is not None:
                self.callback()
        else:
            print(time.time() - self.started)
            
        

class BaseScreen(object):
    name = "General Screen"
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager

    def input(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class ScreenManager(object):
    def __init__(self):
        self.screens = []

    def input(self):

        if len(self.screens) > 0:
            self.screens[-1].input()

    def update(self):

        if len(self.screens) > 0:
            self.screens[-1].update()

    def draw(self):

        if len(self.screens) > 0:
            self.screens[-1].draw()

    def push(self, screen):
        self.screens.append(screen)

    def pop(self, screen=None):
        if screen is None and len(self.screens) > 0:
            self.screens.pop()
        elif screen is not None and len(self.screens) > 0:
            self.screens.pop(screen)

    def set(self, screen):
        self.screens = [screen]

    def clear(self):
        self.screens = []

class SplashScreen(BaseScreen):
    name = "Splash Screen"

    def __init__(self, screen_manager):
        super(SplashScreen, self).__init__(screen_manager)
        self.timer = OnLoopTimer(self.timer_complete, 15)
    
    def input(self):
        print("Splash screen input")
    
    def update(self):
        print("Splash screen update")
    
    def draw(self):
        self.timer.loop()
        print("Splash screen draw")
    
    def timer_complete(self):
        print("Timer Complete!")
        self.screen_manager.push(Wifi_SSID_Screen(self.screen_manager))


class Wifi_SSID_Screen(BaseScreen):
    name = "WiFi SSID Input Screen"
    def input(self):
        print("%s Input" % self.name)
    def update(self):
        print("%s Update" % self.name)
    def draw(self):
        print("%s Draw" % self.name)

if __name__ == '__main__':

    sm = ScreenManager()
    sm.push(SplashScreen(sm))

    while True:
        sm.input()
        sm.update()
        sm.draw()

        print("sleeping...")
        time.sleep(1)
