# import pygame

# pygame.init()

# screen = pygame.display.set_mode((800, 600))
# clock = pygame.time.Clock()

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     screen.fill((30, 30, 30))  # background

#     # draw a filled circle
#     pygame.draw.circle(screen, (30, 20, 55), (400, 300), 50)

#     # draw an outline circle
#     pygame.draw.circle(screen, (255, 0, 0), (200, 300), 60, 3)

#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()



[
    Hub(
        name="start",
        x=0,
        y=0,
        zone_type="normal",
        color=None,
        max_drones="8",
        is_start=True,
        is_end=False,
        connections=0,
        current_drones=[],
    ),
    Hub(
        name="maze_a1",
        x=1,
        y=0,
        zone_type="normal",
        color="blue",
        max_drones=1,
        is_start=False,
        is_end=False,
        connections=0,
        current_drones=[],
    ),
    Hub(
        name="maze_a2",
        x=2,
        y=0,
        zone_type="normal",
        color="blue",
        max_drones=1,
        is_start=False,
        is_end=False,
        connections=0,
        current_drones=[],
    ),
    Hub(
        name="maze_b1",
        x=1,
        y=1,
        zone_type="normal",
        color="blue",
        max_drones=1,
        is_start=False,
        is_end=False,
        connections=0,
        current_drones=[],
    ),
    Hub(
        name="maze_b2",
        x=2,
        y=1,
        zone_type="normal",
        color="blue",
        max_drones=1,
        is_start=False,
        is_end=False,
        connections=0,
        current_drones=[],
    ),
    Hub(
        name="maze_c1",
        x=1,
        y=2,
        zone_type="normal",
        color="blue",
        max_drones=1,
        is_start=False,
        is_end=False,
        connections=0,
        current_drones=[],
    ),
    Hub(
        name="maze_c2",
        x=2,
        y=2,
        zone_type="normal",
        color="blue",
        max_drones=1,
        is_start=False,
        is_end=False,
        connections=0,
        current_drones=[],
    ),
    Hub(
        name="dead_end1",
        x=0,
        y=1,
        zone_type="normal",
        color="red",
        max_drones=1,
        is_start=False,
        is_end=False,
        connections=0,
        current_drones=[],
    ),
    Hub(
        name="dead_end2",
        x=0,
        y=2,
        zone_type="normal",
        color="red",
        max_drones=1,
        is_start=False,
        is_end=False,
        connections=0,
        current_drones=[],
    ),
    Hub(
        name="dead_end3",
        x=3,
        y=1,
        zone_type="normal",
        color="red",
        max_drones=1,
        is_start=False,
        is_end=False,
        connections=0,
        current_drones=[],
    ),
    Hub(
        name="trap_loop1",
        x=3,
        y=0,
        zone_type="restricted",
        color="orange",
        max_drones=1,
        is_start=False,
        is_end=False,
        connections=0,
        current_drones=[],
    ),
    Hub(
        name="trap_loop2",
        x=3,
        y=2,
        zone_type="restricted",
        color="orange",
        max_drones=1,
        is_start=False,
        is_end=False,
        connections=0,
        current_drones=[],
    ),
    Hub(
        name="bottleneck",
        x=4,
        y=1,
        zone_type="normal",
        color="yellow",
        max_drones="2",
        is_start=False,
        is_end=False,
        connections=0,
        current_drones=[],
    ),
    Hub(
        name="final_stretch1",
        x=5,
        y=0,
        zone_type="priority",
        color="cyan",
        max_drones=1,
        is_start=False,
        is_end=False,
        connections=0,
        current_drones=[],
    ),
    Hub(
        name="final_stretch2",
        x=5,
        y=1,
        zone_type="priority",
        color="cyan",
        max_drones=1,
        is_start=False,
        is_end=False,
        connections=0,
        current_drones=[],
    ),
    Hub(
        name="final_stretch3",
        x=5,
        y=2,
        zone_type="priority",
        color="cyan",
        max_drones=1,
        is_start=False,
        is_end=False,
        connections=0,
        current_drones=[],
    ),
    Hub(
        name="goal",
        x=6,
        y=1,
        zone_type="normal",
        color="green",
        max_drones="8",
        is_start=False,
        is_end=True,
        connections=0,
        current_drones=[],
    ),
]

{
    "start": [],
    "maze_a1": [],
    "maze_a2": [],
    "maze_b1": [],
    "maze_b2": [],
    "maze_c1": [],
    "maze_c2": [],
    "dead_end1": [],
    "dead_end2": [],
    "dead_end3": [],
    "trap_loop1": [],
    "trap_loop2": [],
    "bottleneck": [],
    "final_stretch1": [],
    "final_stretch2": [],
    "final_stretch3": [],
    "goal": [],
}
None
