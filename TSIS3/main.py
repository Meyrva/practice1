import pygame, sys
from pygame.locals import *
import random, time, json

pygame.init()

WIDTH = 400
HEIGHT = 600
SPEED = 5
SCORE = 0
AMOUNT_COINTS = 0
DISTANCE = 0
FINISH = 5000
USER_NAME = ''


BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

font_over = pygame.font.SysFont("Verdana", 60)
game_over = font_over.render("Game Over", True, BLACK)

font_score = pygame.font.SysFont("Verdana", 40)
font_small = pygame.font.SysFont("Verdana", 20)

run = True
FPS = pygame.time.Clock()


back = pygame.image.load(r"materials\дорога.jpg")
background = pygame.transform.scale(back, (400,800))
screen = pygame.display.set_mode((WIDTH, HEIGHT))

screen.blit(background, (0,0))
pygame.display.set_caption("Game racer")

SOUND_ON = True
CAR_COLOR = YELLOW
DIFFICULT = "EASY"
STATE = 'MENU'

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
            self.rect.center = (random.randint(40, WIDTH - 40),-100)
            self.kill()

# TSIS 3.1   1) Lane hazards and safe paths
class obstacles(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.obst = pygame.image.load(r"materials\spikes.png")
        self.image = pygame.transform.scale(self.obst,(70,60) )

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,WIDTH-40),0)
    def move(self):
        self.rect.move_ip(0,4)
        if(self.rect.bottom > 600):
            self.kill()

    def spawn(self, enemies, coins, strips, obstacl):
        while True:
            self.rect.center = (random.randint(40, WIDTH - 40),-100)

            # check for a collision 
            col_enemies = pygame.sprite.spritecollideany(self, enemies)
            col_coins = pygame.sprite.spritecollideany(self, coins)
            col_strips = pygame.sprite.spritecollideany(self, strips)
            
            # TSIS 3.2 safe spawn logic 
            too_close_horizontally = False
            for o in obstacl:
                if o != self: 
                    if abs(self.rect.centerx - o.rect.centerx) < 120:
                        too_close_horizontally = True
            if not col_enemies and not col_coins and not col_strips and not too_close_horizontally:
                break


# TSIS 3.1  2) Road events
class SpeedStrip(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((random.randint(50, 100),100))

        if self.type == 'boost':
            self.image.fill(GREEN)
            self.speed_change = 2
        else:
            self.image.fill((255,165,0))
            self.speed_change = -2
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, 100),-100)

    def move(self):
        self.rect.move_ip(0,3)
        if self.rect.top > 600:
            self.kill()


# TSIS 3.3  Power-Ups and Boosts

class Powerup(pygame.sprite.Sprite):
    def __init__(self, p_type):
        super().__init__()
        self.type = p_type

        if self.type == 'nitro':
            self.image = pygame.Surface((30,30))
            self.image.fill((0,255,255))#blue
        elif self.type == 'shield':
            self.image = pygame.Surface((30,30))
            self.image.fill((255,255,0))#yellow
        elif self.type == 'repair':
            self.image = pygame.Surface((30,30))
            self.image.fill((255,0,255))#purple

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,WIDTH - 40), -50)

    def move(self):
        self.rect.move_ip(0,P1.curr_speed)
        if self.rect.top > 600:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        if CAR_COLOR == YELLOW:
            path = r"materials\main_car.png"
        else:
            path = r"materials\green.png"
        self.image1 = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image1,(60,80) ) 

        self.rect = self.image.get_rect()
        self.rect.center = (160,520)

        self.speed = 5  
        self.curr_speed = self.speed
        
        self.acrive_power = None
        self.pow_time = 0
        self.shield = False
        self.health = 3
    def move(self):
        pressed_key = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_key[K_LEFT]:
                self.rect.move_ip(-self.curr_speed,0)
        if self.rect.right < WIDTH:
            if pressed_key[K_RIGHT]:
                self.rect.move_ip(self.curr_speed,0)
    
    

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
            if not pygame.sprite.spritecollideany(self,obstacl):
                break


# TSIS 3.5 Game Screens and Settings
def save_score(score, name, distan):
    try:
        with open("scores.json", "r") as f:
            data = json.load(f)
    except:
        data = []
    
    data.append({"name": name, "score": int(score), "distance": int(distan)})
    data.sort(key=lambda x: x['score'], reverse=True)
    data = data[:10]
    
    with open("scores.json", "w") as f:
        json.dump(data, f)

def load_scores():
    try:
        with open("scores.json", "r") as f:
            return json.load(f)
    except:
        return []

def reset_game():
    global P1, E1, C, enemies, powerups, all_sprites, obstacl, coin, strips, SCORE, AMOUNT_COINTS, SPEED, DISTANCE, USER_NAME
    P1 = Player()
    E1 = Enemy()
    C = Coins()
    
    enemies = pygame.sprite.Group()
    enemies.add(E1)
    
    coin = pygame.sprite.Group()
    coin.add(C)
    
    powerups = pygame.sprite.Group()
    obstacl = pygame.sprite.Group()
    strips = pygame.sprite.Group()
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1, E1, C)
    SPEED = 5
    SCORE = 0
    AMOUNT_COINTS = 0
    DISTANCE = 5

def draw_text(text, font, color, x, y, center=True):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center: 
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)

def button(text, y, action_state):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(WIDTH//2 - 100, y, 200, 50)
    
    if rect.collidepoint(mouse) :
        color = (200, 200, 200) 
    else:
        color = (150, 150, 150)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    draw_text(text, font_small, BLACK, rect.centerx, rect.centery)
    if rect.collidepoint(mouse) and click[0] == 1:
        pygame.time.delay(150)
        return action_state
    return None


def menu_screen():
    global STATE
    screen.blit(background, (0,0))
    draw_text("RACER", font_score, WHITE, WIDTH//2, 100)
    
    res_play = button("PLAY", 250, "INPUT_NAME")
    res_lead = button("LEADERS", 320, "LEADERS")
    res_set = button("SETTINGS", 390, "SETTINGS")
    res_exit = button("EXIT", 460, "EXIT")
    
    if res_play:
        STATE = 'INPUT_NAME'
    elif res_lead:
        STATE = 'LEADERS'
    elif res_set:
        STATE = 'SETTINGS'
    elif res_exit:
        pygame.quit()
        sys.exit()

def settings_screen():
    global STATE, SOUND_ON, CAR_COLOR
    screen.blit(background, (0, 0))
    draw_text("SETTINGS", font_score, WHITE, WIDTH//2, 100)
    
    s_label = f"SOUND: {'ON' if SOUND_ON else 'OFF'}"
    if button(s_label, 200, "TOGGLE_S"): 
        SOUND_ON = not SOUND_ON
    
    c_label = f"COLOR: {'YELLOW' if CAR_COLOR == YELLOW else 'GREEN'}"
    if button(c_label, 270, "TOGGLE_C"):
        CAR_COLOR = GREEN if CAR_COLOR == YELLOW else YELLOW
        
    if button("BACK", 400, "MENU"): 
        STATE = "MENU"

# TSIS 3.4   4)Username entry
def input_name_screen():
    global STATE, USER_NAME
    screen.fill(BLACK)
    draw_text("ENTER YOUR NAME:", font_small, WHITE, WIDTH//2, HEIGHT//2 - 50)
    draw_text(USER_NAME, font_score, YELLOW, WIDTH//2, HEIGHT//2)
    draw_text("Press ENTER to Start", font_small, GREEN, WIDTH//2, HEIGHT//2 + 100)


# TSIS 3.4   3)leaderboard persistence
def leaderboard_screen():
    global STATE
    screen.blit(background, (0, 0))
    draw_text("TOP 10", font_score, YELLOW, WIDTH//2, 50)
    
    scores = load_scores()
    for i, s in enumerate(scores):
        txt = f"{i+1}. {s['name'][:8]:<8} {s['score']:>5} {s['distance']:>5}m"
        draw_text(txt, font_small, WHITE, WIDTH//2, 110 + i * 35)
    
    if button("BACK", 500, "MENU"): STATE = "MENU"

def game_over_screen():
    global STATE
    screen.fill((100, 0, 0))
    draw_text("GAME OVER",font_score, WHITE, WIDTH//2, 150)
    draw_text(f"SCORE: {SCORE}", font_small, WHITE, WIDTH//2, 220)
    
    if button("AGAIN", 300, "GAME"): 
        reset_game()
        STATE = "GAME"
    if button("MAIN MENU", 370, "MENU"): STATE = "MENU"

reset_game()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()
        if STATE == 'INPUT_NAME' and event.type == KEYDOWN:
            if event.key == K_RETURN and USER_NAME != "":
                reset_game()
                STATE = 'GAME'
            elif event.key == K_BACKSPACE:
                USER_NAME = USER_NAME[:-1]
            else:
                if len(USER_NAME) < 10 and event.unicode.isprintable(): 
                    USER_NAME += event.unicode
    # 3.5   Game Screens and Settings
    if STATE == 'MENU':
        menu_screen()
    
    # TSIS 3.4   4)Username entry
    elif STATE == 'INPUT_NAME':
        input_name_screen()


    elif STATE == "SETTINGS":
        settings_screen()
    # TSIS 3.4   3)leaderboard persistence
    elif STATE == "LEADERS":
        leaderboard_screen()

    elif STATE == "GAMEOVER":
        screen.fill(RED)
        draw_text("GAME OVER", font_score, WHITE, WIDTH//2, 200)
        draw_text(f"{USER_NAME}: {SCORE}", font_small, WHITE, WIDTH//2, 260)
        if button("MENU", 350,'MENU'): 
            STATE = 'MENU'

    elif STATE == 'GAME':
        if random.randint(1,100) == 1:
            if len(enemies)<2:
                new_e = Enemy()
                enemies.add(new_e)
                all_sprites.add(new_e)

        # TSIS 3.1-3.2   1) Lane hazards 
        if random.randint(1,100) == 1:
            if len(obstacl)<2:
                new_obt = obstacles()
                obstacl.add(new_obt)
                all_sprites.add(new_obt)
        
        # TSIS 3.1-3.2  2) Road events
        if random.randint(1,200) == 1:
            if len(strips)<2:
                strip_type = random.choice(['boost','slow'])
                new_strip = SpeedStrip(strip_type)
                strips.add(new_strip)
        hit_strip = pygame.sprite.spritecollideany(P1, strips)

        P1.curr_speed = P1.speed + (hit_strip.speed_change if hit_strip else 0)
    


    # TSIS 3.3  Power-Ups and Boosts
        if random.randint(1,400) == 1:
            p_type = random.choice(['nitro', 'shield', 'repair'])
            new_p = Powerup(p_type)
            powerups.add(new_p)
            all_sprites.add(new_p)
        
        hit_power = pygame.sprite.spritecollideany(P1,powerups)

        if hit_power:
            if hit_power.type == 'nitro':
                P1.acrive_power = 'NITRO'
                P1.pow_time = pygame.time.get_ticks() + 5000
                P1.speed = 10
            
            elif hit_power.type == 'shield':
                P1.acrive_power = 'SHIELD'
                P1.shield = True
                P1.pow_time = 0

            elif hit_power.type == 'repair':
                P1.health = min(3,P1.health +1 )

            hit_power.kill()
        if P1.acrive_power =='NITRO':
            if pygame.time.get_ticks()> P1.pow_time:
                P1.speed = 5
                P1.acrive_power = None
        
        hit_enemy = pygame.sprite.spritecollideany(P1,enemies)
            
        if hit_enemy:
            if P1.shield:
                P1.shield = False
                P1.acrive_power = None
                hit_enemy.kill()
            else:
                pass
        # TSIS 3.4   2) distance meter 
        DISTANCE += P1.speed//2
        SCORE = (AMOUNT_COINTS *10) + (DISTANCE // 10)

        screen.blit(background,(0,0))
        scores = font_score.render(str(SCORE), True, RED)
        screen.blit(scores, (10,10))

        dis = FINISH - DISTANCE
        dist_text = font_small.render(f"Distance: {DISTANCE}m\n Remaining ds to finish: {dis}", True, WHITE)
        screen.blit(dist_text, (10, 110))

        for s in strips:
            screen.blit(s.image, s.rect)
            s.move()

        amounn_coin = font_score.render(str(AMOUNT_COINTS), True, GREEN)
        screen.blit(amounn_coin,(WIDTH - 60,10))
        cur_health = font_small.render(f'health {P1.health}', True, BLUE)
        screen.blit(cur_health,(10,60))

        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)
            entity.move()

        if P1.acrive_power:
            text = f"PowerUp: {P1.acrive_power}"

            if P1.acrive_power == 'NITRO':
                timeleft = max(0, (P1.pow_time - pygame.time.get_ticks())//1000)
                text += f' {timeleft} seconds'
            elif P1.acrive_power == 'SHIELD':
                text += ' ACTIVE'
            
            f_text = font_small.render(text, True, (41,171,135))
            screen.blit(f_text, (80,10))


        # Checking the coin collection
        collided_coins = pygame.sprite.spritecollide(P1, coin, False)
        for c in collided_coins:
            # Randomly generating coins with different weights on the road
            AMOUNT_COINTS += random.randint(1, 10)
            c.spawn()
            c.rect.top = 0  # Move the coin so that it doesn't count twice
            c.rect.center = (random.randint(40, WIDTH - 40),-100)
            # TSIS 3.2 Difficulty scaling    
            # the speed of Enemy increases every 2 coins
            if AMOUNT_COINTS % 2 ==0:
                SPEED += 0.5

        # Crash check (collision of player and enemy, obstacl)
        col_enemie =pygame.sprite.spritecollideany(P1, enemies) 
        col_obst = pygame.sprite.spritecollideany(P1, obstacl)

        both = col_enemie or col_obst
        if both:
            if P1.acrive_power == 'SHIELD':
                P1.acrive_power = None
                both.kill()
            else:
                P1.health -= 1
                both.kill()

            if P1.health <= 0:
                if SOUND_ON:
                    pygame.mixer.Sound(r'materials\crash.mp3').play()
                    time.sleep(0.5)

                save_score(SCORE, USER_NAME, DISTANCE) 

                for entity in all_sprites:
                    entity.kill()
                STATE = "GAMEOVER"
                
    pygame.display.update()
    FPS.tick(60)
