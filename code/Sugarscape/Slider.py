"""Written by Dan Kearney, Natalie Mattison, and Theodore Thompson
for Olin College Computational Modeling 2011."""

import pygame

class Slider:

    def __init__(self, (x, y), text, gui, sug_func, sug_field, field_range, min_val = 0, is_int = False, is_percent = False):
        '''a slider that calls a function when it has moved'''
        self.min_val = min_val
        self.is_int = is_int
        self.is_percent = is_percent
        self.sug_func = sug_func
        self.sug_field = sug_field
        self.sug_field_initial = self.sug_field
        self.field_range = field_range
        self.gui = gui
        self.text = text
        
        self.slider_width, self.slider_height = 16,54
        self.back_width, self.back_height = 150,18
        self.slider_x = x-self.slider_width/2+self.back_width/2
        self.slider_y = y-self.slider_height/2 + self.back_height/2

        self.slider_coords = [self.slider_x, self.slider_y, self.slider_x+self.slider_width, self.slider_y+self.slider_height]
        self.background_coords =  [x,y,x+self.back_width,y+self.back_height]
        
        self.gui.sliders.append(self)
        self.unclick_slider()
        self.draw_slider()
        
    
    def draw_text(self, x, y, value, color=(255,255,255), fontsize=20):
        '''draws the text associated with the slider
        next to the slider'''
        self.msg_object = pygame.font.SysFont('verdana', fontsize).render(str(value), False, color)
        self.msg_rect = self.msg_object.get_rect()
        self.msg_rect.topleft = (x + self.back_width + 2, y - 6)
        self.gui.window.blit(self.msg_object, self.msg_rect)
        
        
    def click_slider(self, x, y):
        '''grabs the slider'''
        if x >= self.slider_coords[0] and x <= self.slider_coords[2]:
            if y >= self.slider_coords[1] and y <= self.slider_coords[3]:
                self.gui.clicked[self] = True
    
    def unclick_slider(self):
        '''releases the slider'''
        self.gui.clicked[self] = False
    
    def move_slider(self, x, y):
        '''moves the slider along the base'''
        if not self.gui.clicked[self]:
            #get outta here
            return False
            
        width = self.slider_width
        if x < (self.background_coords[0] + width/2): 
            x = self.background_coords[0] + width/2
        if x > (self.background_coords[2] - width/2): 
            x = self.background_coords[2] - width/2

        self.slider_coords[0] = x - width/2
        self.slider_coords[2] = x + width/2
        offset = width/2 + self.slider_coords[0] - (self.background_coords[2] + self.background_coords[0])/2
        
        percent = round(offset / float(self.background_coords[2] - self.background_coords[0] - width) + 1/2.,4) - .0001
        new_val = (percent - .50) * (2*self.field_range) + self.sug_field_initial
        if new_val < self.min_val:
            new_val = self.min_val
        if self.is_percent:
            new_val = int(new_val * 100)/100.
        if self.is_int:
            new_val = int(new_val)
            
        self.sug_field = new_val
        self.sug_func(self.sug_field)
        self.draw_slider()
        return True

    def draw_slider(self):
        '''draws the slider, its background,
        and the text on the gui'''
        x,y = self.background_coords[0], self.background_coords[1]
        if self.is_percent:
            value = str(int(self.sug_field * 100)) + "%s" %"%"
            width_boost = 20
        elif self.is_int:
            value = int(self.sug_field)
        else:
            value = round(self.sug_field,2)
        pygame.draw.rect(self.gui.window,self.gui.background_color,(x,self.slider_y, self.back_width, self.slider_height))            
        pygame.draw.rect(self.gui.window, self.gui.background_color, (x+self.back_width, y-self.slider_height/2 + self.back_height/2, 50, self.slider_height))             
        self.draw_text(x,y, str(value))
        pygame.draw.rect(self.gui.window, (0,150,250), (self.slider_coords[0], self.slider_coords[1], self.slider_width, self.slider_height))
        pygame.draw.rect(self.gui.window, (0,25,250), (self.slider_coords[0]+2, self.slider_coords[1]+2, self.slider_width-4, self.slider_height-4))
        pygame.draw.rect(self.gui.window, (0,150,250), (self.background_coords[0], self.background_coords[1], self.back_width, self.back_height))
        pygame.draw.rect(self.gui.window, (255,255,255), (self.background_coords[0]+2, self.background_coords[1]+2, self.back_width-4, self.back_height-4))
        self.draw_text(x-self.back_width/2-len(self.text)*3.3, y+self.back_height/3+1,self.text,color = (0,0,0), fontsize=11)       

