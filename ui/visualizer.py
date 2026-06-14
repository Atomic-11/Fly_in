import pygame
from classes.map import Map
from typing import List, Dict, Any
from configs.parser import Parser

SCALE = 200
OFFSET_X = 130
OFFSET_Y = 600
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
        self.width: int = 3000
        self.height: int = 1440
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("monospace", 20)
        self.drone_font = pygame.font.SysFont("monospace", 16)
        pygame.display.set_caption("FLY IN") 
    
    def draw(self, state: Dict[int, str]) -> None:
        self.screen.fill((0, 0, 0))
        self.draw_connections()
        self.draw_hubs()
        self.draw_drones(state)
        pygame.display.flip()
    
    def draw_connections(self) -> None:
        for con in self.map.connections.values():
            pygame.draw.line(self.screen, 
                             (255, 255, 255), 
                             (con.hub_a.x * SCALE + OFFSET_X,
                              con.hub_a.y * SCALE + OFFSET_Y), 
                             (con.hub_b.x * SCALE + OFFSET_X,
                              con.hub_b.y * SCALE + OFFSET_Y),
                             16)
    
    def draw_hubs(self) -> None:
        for hub in self.map.hubs.values():
            color = COLORS.get(hub.color, COLORS[None])
            pygame.draw.circle(self.screen,
                               color,
                               (hub.x * SCALE + OFFSET_X,
                                hub.y * SCALE + OFFSET_Y),
                               75)
            
    def draw_drones(self, state: Dict[int, str]) -> None:
        from collections import defaultdict
        hub_drones: Dict[str, List[int]] = defaultdict(list)
        for drone_id, hub_name in state.items():
            hub_drones[hub_name].append(drone_id)
        
        for hub_name, drone_ids in hub_drones.items():
            hub = self.map.hubs[hub_name]
            hx, hy = hub.x * SCALE + OFFSET_X, hub.y * SCALE + OFFSET_Y
            for i, drone_id in enumerate(drone_ids):
                offset_x = (i % 3) * 35 - 35
                offset_y = (i // 3) * 35 - 15
                x, y = hx + offset_x, hy + offset_y
                pygame.draw.circle(self.screen, (255, 255, 0), (x, y), 20)
                label = self.font.render(f"D{drone_id}", True, (0, 0, 0))
                self.screen.blit(label, (x - 12, y - 8))
            
    def run(self, state) -> None:
        current_turn = 0
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if current_turn < len(state) - 1:
                            current_turn += 1
            self.draw(state[current_turn])
            clock.tick(60)
        pygame.quit()

# just to test:
# p = Parser(map="map.txt")
# map = p.parse()
# v = Visualizer(map)
# v.run()