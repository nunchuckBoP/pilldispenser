import time
import pygame

# CONSTANTS
SCREEN_SIZE = (480,320)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)


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
                    if self.callback is not None:
                        self.callback()
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

class AlertPopup(object):
    pass

class TextBanner(object):
    pass

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
        