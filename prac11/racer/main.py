import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

WIDTH = 400
HEIGHT = 600
SPEED = 5
SCORE = 0
AMOUNT_COINTS = 0


BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font_over = pygame.font.SysFont("Verdana", 60)
game_over = font_over.render("Game Over", True, BLACK)

font_score = pygame.font.SysFont("Verdana", 40)

run = True
FPS = pygame.time.Clock()


back = pygame.image.load(r"materials\дорога.jpg")
background = pygame.transform.scale(back, (400,800))
screen = pygame.display.set_mode((WIDTH, HEIGHT))

screen.blit(background, (0,0))
pygame.display.set_caption("Game racer")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image1 = pygame.image.load(r"materials\2car.png")
        self.image = pygame.transform.scale(self.image1,(60,80) )

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,WIDTH-40),-100)

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        # If the car has gone beyond the lower border of the screen:
        if(self.rect.bottom > 600):
            SCORE += 1 # Award a point for a successful dodge
            self.rect.top = 0 # Bringing the car back up
            self.rect.center = (random.randint(40, WIDTH - 40),-100)

    

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image1 = pygame.image.load(r"materials\main_car.png")
        self.image = pygame.transform.scale(self.image1,(60,80) ) 

        self.rect = self.image.get_rect()
        self.rect.center = (160,520)
        
    def move(self):
        pressed_key = pygame.key.get_pressed()
        # if pressed_key[K_UP]:
        #     self.rect.move_ip(0,-5)
        # if pressed_key[K_DOWN]:
        #     self.rect.move_ip(0,5)
        
        if self.rect.left > 0:
            if pressed_key[K_LEFT]:
                self.rect.move_ip(-5,0)
        if self.rect.right < WIDTH:
            if pressed_key[K_RIGHT]:
                self.rect.move_ip(5,0)
    
    

class Coins(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image1 = pygame.image.load(r"materials\coin.png")
        self.image = pygame.transform.scale(self.image1,(55,40) )

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,WIDTH-40),0)
    def move(self):
        global AMOUNT_COINTS
        self.rect.move_ip(0,3)
        if(self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40),-100)
    def spawn(self):
        while True:
            self.rect.center = (random.randint(40, WIDTH - 40),-100)
            if not pygame.sprite.spritecollideany(self,enemies):
                break


P1 = Player()
E1 = Enemy()
C = Coins()

enemies = pygame.sprite.Group()
enemies.add(E1)

coin = pygame.sprite.Group()
coin.add(C)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while run:
    for event in pygame.event.get():
        # if event.type == INC_SPEED:
        #     SPEED += 0.5

        if event.type == pygame.QUIT:
            run = False
            sys.exit()

    screen.blit(background,(0,0))
    scores = font_score.render(str(SCORE), True, RED)
    screen.blit(scores, (10,10))

    amounn_coin = font_score.render(str(AMOUNT_COINTS), True, GREEN)
    screen.blit(amounn_coin,(WIDTH - 60,10))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    # Checking the coin collection
    collided_coins = pygame.sprite.spritecollide(P1, coin, False)
    for c in collided_coins:
        # Randomly generating coins with different weights on the road
         AMOUNT_COINTS += random.randint(1, 10)
         c.spawn()
         c.rect.top = 0  # Move the coin so that it doesn't count twice
         c.rect.center = (random.randint(40, WIDTH - 40),-100)
        # The speed of Enemy increases every 2 coins
         if AMOUNT_COINTS % 2 ==0:
             SPEED += 0.5

    # Crash check (collision of player and enemy)
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound(r'materials\crash.mp3').play()
        time.sleep(0.5)

        screen.fill(RED)
        screen.blit(game_over,(30,250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()
    # P1.update()
    # E1.move()

    # screen.fill(WHITE)
    # P1.draw(screen)
    # E1.draw(screen)


    pygame.display.update()
    # pygame.display.flip()
    FPS.tick(60)
