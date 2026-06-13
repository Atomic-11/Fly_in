import pygame
from classes.map import Map
from typing import List, Dict, Any
from configs.parser import Parser

SCALE = 300
OFFSET_X = 200
OFFSET_Y = 100
COLORS = {
    None:       (180, 180, 180),  # light gray

    "red":      (255, 80, 80),
    "green":    (80, 220, 100),
    "blue":     (70, 140, 255),

    "yellow":   (255, 220, 50),
    "orange":   (255, 140, 0),
    "cyan":     (0, 220, 220),

    "purple":   (170, 100, 255),
    "pink":     (255, 105, 180),
    "magenta":  (255, 0, 255),

    "lime":     (150, 255, 50),
    "teal":     (0, 180, 180),
    "navy":     (40, 80, 180),

    "brown":    (139, 69, 19),
    "gold":     (255, 215, 0),
    "silver":   (192, 192, 192),

    "olive":    (128, 128, 0),
    "maroon":   (128, 0, 0),
    "violet":   (138, 43, 226),

    "turquoise": (64, 224, 208),
    "coral":     (255, 127, 80),
    "salmon":    (250, 128, 114),

    "white":    (255, 255, 255),
    "black":    (0, 0, 0),
}

class Visualizer:
    def __init__(self, map: Map) -> None:
        pygame.init()
        self.map: Map = map
        self.width: int = 2560
        self.height: int = 1440
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("monospace", 14)
        pygame.display.set_caption("FLY IN") 
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_connections()
        self.draw_hubs()
        pygame.display.flip()
    
    def draw_connections(self):
        for con in self.map.connections.values():
            pygame.draw.line(self.screen, 
                             (255, 255, 255), 
                             (con.hub_a.x * SCALE + OFFSET_X,
                              con.hub_a.y * SCALE + OFFSET_Y), 
                             (con.hub_b.x * SCALE + OFFSET_X,
                              con.hub_b.y * SCALE + OFFSET_Y),
                             16)
    
    def draw_hubs(self):
        for hub in self.map.hubs.values():
            color = COLORS.get(hub.color, COLORS[None])
            pygame.draw.circle(self.screen,
                               color,
                               (hub.x * SCALE + OFFSET_X,
                                hub.y * SCALE + OFFSET_Y),
                               75)
            
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw()
            clock.tick(60)
        pygame.quit()

# p = Parser(map="map.txt")
# map = p.parse()
# v = Visualizer(map)
# v.run()