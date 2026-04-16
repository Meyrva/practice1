import pygame

WIDTH = 800
HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

x = 30
y = 30
RADIUS = 25
run = True

clock = pygame.time.Clock()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: 
        y -= 20
    if pressed[pygame.K_DOWN]:
        y += 20
    if pressed[pygame.K_LEFT]: 
        x -= 20
    if pressed[pygame.K_RIGHT]:
        x += 20

    if x - RADIUS < 0:
        x = RADIUS
    if x + RADIUS > WIDTH:
        x = WIDTH - RADIUS
    if y - RADIUS < 0:
        y = RADIUS
    if y + RADIUS > HEIGHT:
        y = HEIGHT - RADIUS


    screen.fill((255, 255, 255))
    color = (255, 0 , 0)
    pygame.draw.circle(screen, color,(x, y), RADIUS ) 

    pygame.display.flip()
    clock.tick(60)
pygame.quit()