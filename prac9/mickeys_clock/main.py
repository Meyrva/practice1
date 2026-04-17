import pygame
import datetime

pygame.init()

WIDTH = 900
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
center = (WIDTH // 2, HEIGHT // 2)

main_clock = pygame.image.load(r"images\mickeyclock.jpeg")
hand = pygame.image.load(r"images\right.jpeg") 

new_w = 160
new_h = 400
new_size = (new_w, new_h)

hand_min = pygame.transform.scale(hand, new_size)
hand_sec = pygame.transform.flip(hand_min, True, False)

def rotate_and_draw(surface, angle, pos):
   
    rotated_surface = pygame.transform.rotate(surface, angle)
    
    rect = rotated_surface.get_rect(center=pos)
    screen.blit(rotated_surface, rect)

clock = pygame.time.Clock()
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    now = datetime.datetime.now()
    second = now.second
    minute = now.minute
    
    angle_s = - (second * 6) 
    angle_m = - (minute * 6) 


    screen.fill((255, 255, 255))
    
   
    clock_rect = main_clock.get_rect(center=center)
    screen.blit(main_clock, clock_rect)

    rotate_and_draw(hand_min, angle_m, center)
    rotate_and_draw(hand_sec, angle_s, center)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()