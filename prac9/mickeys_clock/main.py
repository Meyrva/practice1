import pygame
import datetime




pygame.init()

WIDTH = 900
HEIGHT = 750

screen = pygame.display.set_mode((WIDTH, HEIGHT))

image = pygame.image.load("images\mickeyclock.jpeg")
right_minut = pygame.image.load("images\mickeyclock.jpeg")
left_secon = pygame.image.load("images\mickeyclock.jpeg")

run = True
angle_m = 0
angle_s = 0

clock = pygame.time.Clock()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    time = datetime.datetime.now()
    for s in time:
        rotated = pygame.transform.rotate(right_minut, angle_m)
        angle_m += 1

        screen.blit(rotated,)

    rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))



    screen.fill((255, 255, 255))
    screen.blit(image,0)

    pygame.display.flip()
    clock.tick(60)
   
pygame.quit()