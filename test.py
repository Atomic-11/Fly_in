import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))  # background

    # draw a filled circle
    pygame.draw.circle(screen, (30, 20, 55), (400, 300), 50)

    # draw an outline circle
    pygame.draw.circle(screen, (255, 0, 0), (200, 300), 60, 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()