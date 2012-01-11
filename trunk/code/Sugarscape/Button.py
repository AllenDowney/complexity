"""Written by Dan Kearney, Natalie Mattison, and Theodore Thompson
for Olin College Computational Modeling 2011."""

import pygame

class Button:

    def __init__(self, (x, y), gui, start_image, func = None, stay_depressed = False):
        '''a button that calls a function when pressed'''
        self.x = x
        self.y = y
        self.text = start_image
        self.stay_depressed = stay_depressed
        self.func = func
        self.height, self.width = 70,70
        self.gui = gui
        self.gui.clicked[self] = False
        self.gui.buttons.append(self)
        self.draw_button()
        
    def click_button(self, x, y):
        '''handles a button's click'''
        if x >= self.x and x <= self.x + self.width:
            if y >= self.y and y <= self.y + self.height:
                self.gui.clicked[self] = not self.gui.clicked[self]
                if self.gui.clicked:
                    self.func()
                self.draw_button()
        
    def unclick_button(self):
        '''unclicks the button'''
        if not self.stay_depressed:
            self.gui.clicked[self] = False
            if not self.gui.clicked:
                self.func()
            self.draw_button()
            return True

    def draw_text(self, x, y, value, color=(255,255,255), fontsize=20):
        '''draws the text associated with the slider
        next to the slider'''
        self.msg_object = pygame.font.SysFont('verdana', fontsize).render(str(value), False, color)
        self.msg_rect = self.msg_object.get_rect()
        self.msg_rect.center = (x,y)
        self.gui.window.blit(self.msg_object, self.msg_rect)

    def draw_button(self):
        '''draws an image of a button'''
        pressed = (255,255,255)
        unpressed = (0,0,0)
        if not self.gui.clicked[self]:
            color = pressed
            negative = unpressed
        else:
            color = unpressed
            negative = pressed
        pygame.draw.rect(self.gui.window, (50,50,75), (self.x, self.y, self.width, self.height))            
        pygame.draw.rect(self.gui.window, color, (self.x+2, self.y+2, self.width-4, self.height-4))     
        self.draw_text(self.x + self.width/2,self.y+self.height/2,self.text,color=negative)
    
