"""Written by Dan Kearney, Natalie Mattison, and Theodore Thompson
for Olin College Computational Modeling 2011."""

from Sugarscape import Sugarscape
from DataCollect import DataCollect
from Slider import *
from Button import *
from pygame.locals import *
import pygame,sys
import matplotlib
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as pyplot
matplotlib.rc('xtick', labelsize=2) 
matplotlib.rc('ytick', labelsize=2)

class Gui:
    
    def __init__(self,sugarscape):
        '''graphical representation of the sugarscape object'''
        pygame.init()
        self.scape = sugarscape
        #window sizing
        self.square_length=10
        self.options_width = 200
        self.buffer = 1
        self.graph_buffer = 5
        self.graph_panel_length = (self.scape.length*(self.square_length + self.buffer))/2
        self.background_color = (0,0,0)
        self.sliders = []
        self.buttons = []

        self.clicked = {}
        self.started = False
        self.reset = False
        
        self.window=pygame.display.set_mode(((self.square_length+self.buffer)*self.scape.length + self.graph_panel_length + self.graph_buffer*2,(self.square_length+self.buffer)*self.scape.width + self.options_width))
        pygame.display.set_caption("Sugarscape")
        self.agent_color = pygame.Color(0,180,0)
        self.event_loop(self.scape)
    
    def event_loop(self,scape):
        '''displays the sugarscape'''
        self.initialize_graph()
        self.draw_controls()
        while True:
            if self.started:
                scape.nextstep() 
                self.update_graph(self.scape.timestamp)
            self.draw_scape_info()
            for event in pygame.event.get():
                self.handle_events(event)               
            for i in range(scape.length):
                for j in range(scape.width):
                    loc=scape.get_location(i,j)
                    health=loc.get_sugar_amt()/float(loc.get_max_sugar())
                    healthColor=pygame.Color(0, 0, int(250*health))
                    pygame.draw.rect(self.window,healthColor,((self.square_length + self.buffer)*i,(self.square_length + self.buffer)*j,self.square_length,self.square_length))
                    if loc.get_has_agent():
                        pygame.draw.circle(self.window,self.agent_color,(int((self.square_length+self.buffer)*i)+int((self.square_length + self.buffer)/2.),
                                                                          int((self.square_length+self.buffer)*j)+int((self.square_length + self.buffer)/2.) ),
                                                                         int(self.square_length/3.14))
            pygame.display.update()
    
    
    
    def handle_events(self, event):
        '''deals with clicks, unclicks, etc'''
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==MOUSEBUTTONDOWN:
            self.handle_click(*event.pos)
        if event.type==MOUSEMOTION:
            self.handle_slider_motion(*event.pos)
        if event.type==MOUSEBUTTONUP:
            self.release_all_sliders()
            self.release_all_buttons()
        return True
                
    def release_all_buttons(self):
        '''releases all buttons'''
        for button in self.buttons:
            button.unclick_button()
    
    def handle_click(self,x,y):
        '''handles all possible click events'''
        for slider in self.sliders:
            slider.click_slider(x,y)
        for button in self.buttons:
            button.click_button(x,y)
        return False
    
    def handle_slider_motion(self, x, y):
        '''handles slider motion'''
        for slider in self.sliders:
            slider.move_slider(x,y)
        return False
    
    def update_graph(self,timestamp):
        '''this updates the histogram. 
        It alternately clears the axes
        and actually displays the new histogram.'''
        if timestamp % 5 == 0:
            x,y = [],[]
            num_agents = self.scape.num_agents
            wealths = self.scape.agent_wealths()
            if len(wealths)==0: wealths = [0]    
            self.ax.hist(wealths, 20, normed=False)
            self.canvas.draw()
            renderer = self.canvas.get_renderer()
            raw_data = renderer.tostring_rgb()
            surf = pygame.image.fromstring(raw_data, self.canvas_width_height, "RGB")
            self.screen.blit(surf, ((self.square_length+self.buffer)*self.scape.length + self.graph_buffer,self.graph_buffer))
        else:
            self.ax.cla()
        return True
    
    def initialize_graph(self):
        '''displays the histogram.  It instantiates the graph 
        and is optimized so that update_graph runs a little faster'''
        #graph making section
        fig = pyplot.figure(figsize=[1, 1], dpi=self.graph_panel_length)
        self.ax = fig.gca()
        wealths = self.scape.agent_wealths()
        self.ax.hist(wealths, 20, normed=False)
        pyplot.suptitle('Wealth Histogram', fontsize=4)
        
        #rendering
        self.canvas = agg.FigureCanvasAgg(fig)
        self.canvas.draw()
        renderer = self.canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        self.screen = pygame.display.get_surface()
        self.canvas_width_height = self.canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, self.canvas_width_height, "RGB")
        self.screen.blit(surf, ((self.square_length+self.buffer)*self.scape.length + self.graph_buffer,self.graph_buffer))
        return True
    
    
    def draw_controls(self):
        '''draws sliders and buttons'''
        offset = (self.scape.length*(self.square_length + self.buffer))
        coords = [(150,40+offset),(150,120+offset),(375,40+offset),(375,120+offset),(600,40+offset),(600,120+offset)]
        button_coords = [(25, 20+offset), (25, 100+offset)]
        Slider(coords[0], 'metabolism', self, self.scape.set_agent_metabolism,self.scape.agent_metabolism, field_range=4)
        Slider(coords[1], 'vision', self, self.scape.set_agent_vision,self.scape.agent_vision, field_range=5, min_val = 1, is_int = True)
        Slider(coords[2], 'num. agents', self, self.scape.set_num_agents,self.scape.num_agents, field_range=500, min_val = 1, is_int = True)
        Slider(coords[3], 'max sugar', self, self.scape.set_max_sugar,self.scape.max_sugar, field_range=5, min_val = .1)
        Slider(coords[4], 'sugar growth', self, self.scape.set_sugar_growth_rate,self.scape.sugar_growth_rate, field_range=.5, min_val = .01)
        Slider(coords[5], 'tax rate', self, self.scape.set_tax_rate,self.scape.tax_rate, field_range=.5, is_percent = True)
        Button(button_coords[0], self, 'Start!', func = self.pause, stay_depressed = True)
        Button(button_coords[1], self, 'Reset', func = self.scape.reset)


    def release_all_sliders(self):
        '''set all sliders to not grabbed'''
        for slider in self.sliders:
            slider.unclick_slider()

    def pause(self):
        '''pauses the scape'''
        self.started = not self.started
    
    def draw_scape_info(self):
        '''draws the text about the scape'''
        if self.scape.timestamp % 10 != 0:
            return True
        data = DataCollect(self.scape).Pack()
        value_dict = { "Standard deviation: " : round(data[1],1),
                    "Mean wealth: " : round(data[2],1),
                    "Median wealth: " : round(data[3],1),
                    "Total wealth: " : round(data[7],1),
                    "Number of agents: ": len(self.scape.agents),
                    "Gini coefficient: " : round(data[8],2),
                    "Timestep: " : self.scape.timestamp,
                    "Bottom quartile: " : round(data[9],2)
                    }
        scape_width = ((self.square_length+self.buffer)*self.scape.length + self.graph_buffer) + 10
        for (i, key) in enumerate(value_dict.keys()):
            self.write_text(scape_width, scape_width/2 + 30*i + 10, key + str(value_dict[key]))
        return True
        
        
    def write_text(self, x, y, text):
        '''writes text on the scape. 
        puts a black box behind to erase last text'''
        msg_object = pygame.font.SysFont('verdana', 18).render(text, False, (255,255,255))
        msg_rect = msg_object.get_rect()
        msg_rect.topleft = (x, y)
        pygame.draw.rect(self.window, self.background_color, (0, y, 10000, msg_rect.height))
        self.window.blit(msg_object, msg_rect)
        
        
    
if __name__=='__main__':
    a = Sugarscape()
    l=Gui(a)
