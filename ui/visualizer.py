import pygame
from classes.map import Map
from typing import List, Dict, Tuple

COLORS = {
    None:       (180, 180, 180),

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
        pygame.display.set_caption("FLY IN")

        xs = [hub.x for hub in self.map.hubs.values()]
        ys = [hub.y for hub in self.map.hubs.values()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        padding = 150
        map_w = max(max_x - min_x, 1)
        map_h = max(max_y - min_y, 1)

        self.scale_x = (self.width - 2 * padding) / map_w
        self.scale_y = (self.height - 2 * padding) / map_h
        self.offset_x = padding - min_x * self.scale_x
        self.offset_y = padding - min_y * self.scale_y

        effective_scale = min(self.scale_x, self.scale_y)
        self.hub_radius = max(15, min(80, int(effective_scale * 0.3)))

    def hub_pos(self, hub) -> Tuple[int, int]:
        return (
            int(hub.x * self.scale_x + self.offset_x),
            int(hub.y * self.scale_y + self.offset_y)
        )

    def draw(self, state: Dict[int, str]) -> None:
        self.screen.fill((0, 0, 0))
        self.draw_connections()
        self.draw_hubs()
        self.draw_drones(state)
        pygame.display.flip()

    def draw_connections(self) -> None:
        for con in self.map.connections.values():
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                self.hub_pos(con.hub_a),
                self.hub_pos(con.hub_b),
                max(4, self.hub_radius // 5)
            )

    def draw_hubs(self) -> None:
        for hub in self.map.hubs.values():
            color = COLORS.get(hub.color, COLORS[None])
            pygame.draw.circle(
                self.screen,
                color,
                self.hub_pos(hub),
                self.hub_radius
            )

    def draw_drones(self, state: Dict[int, str]) -> None:
        from collections import defaultdict
        positions: Dict[str, List[int]] = defaultdict(list)
        for drone_id, position in state.items():
            positions[position].append(drone_id)

        for position, drone_ids in positions.items():
            if '-' in position:
                parts = position.split('-')
                hub_a = self.map.hubs[parts[0]]
                hub_b = self.map.hubs[parts[1]]
                ax, ay = self.hub_pos(hub_a)
                bx, by = self.hub_pos(hub_b)
                x, y = (ax + bx) // 2, (ay + by) // 2
            else:
                hub = self.map.hubs[position]
                x, y = self.hub_pos(hub)

            space = max(15, self.hub_radius // 2)
            drone_radius = max(16, self.hub_radius // 8)
            for i, drone_id in enumerate(drone_ids):
                ox = (i % 3) * space - space
                oy = (i // 3) * space - space // 2
                pygame.draw.circle(self.screen,
                                   (110, 255, 0),
                                   (x + ox, y + oy),
                                   drone_radius)
                label = self.font.render(f"D{drone_id}", True, (0, 0, 0))
                self.screen.blit(label, (x + ox - 12, y + oy - 8))

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
