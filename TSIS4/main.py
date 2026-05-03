import pygame, random, sys
from connect import save_game_result, get_top_10, get_personal_best
pygame.init()
import json
import os

# TSIS 3.5  Settings (JSON file)
SETTINGS_FILE = "settings.json"
default_settings = {
    "snake_color": [255, 255, 0],  
    "grid_on": True,
    "sound_on": True
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return default_settings.copy()

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

current_settings = load_settings()
colorYELLOW = tuple(current_settings["snake_color"])
GRID_ON = current_settings["grid_on"]
SOUND_ON = current_settings["sound_on"]


# TSIS 3.3  powerups

active_effects = {
    "SPEED_END": 0,
    "SLOW_END": 0,
    "SHIELD": False
}
POWERUP_SPAWN_TIME = 0


FPS = 5
WIDTH = 600
HEIGHT = 600
CELL = 30   

FOOD_SPW = pygame.USEREVENT + 2
# the food disappears after 6 seconds
pygame.time.set_timer(FOOD_SPW, 6000)

colorBLACKRED = (51,0,0)
colorWHITE = (255, 255, 255)
colorGRAY = (200, 200, 200)
colorBLACK = (0, 0, 0)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorBLUE = (0, 0, 255)
colorYELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
font_small = pygame.font.SysFont("Verdana", 20)

STATE = 'MENU'
USER_NAME =''
level = 1
personal_best = 0
score = 0

def draw_grid_chess():
    colors = [colorWHITE, colorGRAY]

    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_border(self):
        head = self.body[0]
        if head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT //CELL:
            return True
        
        for part in self.body[1:]:
            if head.x == part.x and head.y == part.y:
                return True
        return False

class Food:
    def __init__(self):
        self.pos = Point(0,0)

    def generate(self,snake_body, wall_blocks):
        while True:
            self.pos.x = random.randint(0,(WIDTH//CELL) - 1)
            self.pos.y = random.randint(0,(WIDTH//CELL) - 1)
            colision_with_snake = any(p.x == self.pos.x and p.y == self.pos.y for p in snake_body)
            on_wall = any(p.x == self.pos.x and p.y == self.pos.y for p in wall_blocks)
            if not colision_with_snake and not on_wall:
                break

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

# TSIS 3.2 Poison food
class Poison_Food:
    def __init__(self):
        self.pos = Point(0,0)
    
    def generate(self,snake_body, wall_blocks):
        while True:
            self.pos.x = random.randint(0,(WIDTH//CELL) - 1)
            self.pos.y = random.randint(0,(WIDTH//CELL) - 1)
            collision = any(p.x == self.pos.x and p.y == self.pos.y for p in snake_body)
            on_wall = any(p.x == self.pos.x and p.y == self.pos.y for p in wall_blocks)
            if not collision and not on_wall:
                break

    def draw(self):
        pygame.draw.rect(screen, colorBLACKRED, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

# TSIS 3.4 obstacles
class Wall:
    def __init__(self):
        self.blocks = []
    
    def generate(self, level, snake_body, food_pos, poison_pos):
        self.blocks =[]
        if level >= 3:
            num_blocks = 2 + (level -3)
            while len(self.blocks)< num_blocks :
                x = random.randint(0,(WIDTH//CELL) -1)
                y = random.randint(0,(WIDTH//CELL) -1)
                new_block = Point(x,y)

                col_snake = any(p.x == x and p.y == y for p in snake_body)
                col_food = (x == food_pos.x and y == food_pos.y)
                col_poison = (x == poison_pos.x and y == poison_pos.y)

                col_head = abs(x - snake_body[0].x) < 3 and abs(y - snake_body[0].y)<3

                if not ( col_snake or col_food or col_poison or col_head):
                    self.blocks.append(new_block)
            
    def draw(self):
        for block in self.blocks:
            pygame.draw.rect(screen, colorBLACK, (block.x * CELL, block.y * CELL, CELL, CELL))

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
    draw_text(text, font_small, colorBLACK, rect.centerx, rect.centery)
    if rect.collidepoint(mouse) and click[0] == 1:
        pygame.time.delay(150)
        return action_state
    return None

def reset_game():
    global snake, food, poison, wall, score, level, food_on_lev, FPS, powerup, active_effects, POWERUP_SPAWN_TIME
    snake = Snake()
    food = Food()
    poison = Poison_Food()
    wall = Wall()
    powerup = PowerUp()

    active_effects = {"SPEED_END": 0, "SLOW_END": 0, "SHIELD": False}
    POWERUP_SPAWN_TIME = pygame.time.get_ticks()

    food.generate(snake.body,wall.blocks)
    poison.generate(snake.body,wall.blocks)
    wall.generate(level, snake.body, food.pos, poison.pos)

    score = 0
    level = 1
    FPS = 5
    food_on_lev = 0


def menu_screen():
    global STATE 
    screen.fill(colorBLACK)
    draw_text("SNAKE GAME", font_small, colorWHITE, WIDTH//2, 100)
    res = button("START GAME", 250, "INPUT_NAME")
    if res:
        STATE = res
    res = button("LEADERBOARD", 320, "LEADERS")
    if res:
        STATE = res
    res = button("EXIT", 460, "EXIT")
    if res:
        pygame.quit()
        sys.exit()
    # TSIS 3.6   setting 
    res = button("SETTINGS", 390, "SETTINGS")
    if res:
        STATE = res

def input_name_screen():
    screen.fill(colorBLACK)
    draw_text("ENTER YOUR NAME:", font_small, colorWHITE, WIDTH//2, HEIGHT//2 - 50)
    draw_text(USER_NAME, font_small, colorYELLOW, WIDTH//2, HEIGHT//2)
    draw_text("Press ENTER to Start", font_small, colorGREEN, WIDTH//2, HEIGHT//2 + 100)


# TSIS 3.1   3) Leaderboard screen
def leaderboard_screen():
    global STATE
    screen.fill(colorBLACK)
    draw_text("TOP 10", font_small, colorBLUE, WIDTH//2, 50)
    
    scores = get_top_10()
    if scores:
        for i, row in enumerate(scores):
            draw_text(f'{i+1}. {row[0]}: {row[1]}', font_small, colorBLUE, WIDTH//2, 100 + i*30)
    if button("BACK", 500, "MENU"): STATE = "MENU"

def game_over_screen():
    global STATE, personal_best
    screen.fill((100, 0, 0))
    draw_text("GAME OVER",font_small, colorWHITE, WIDTH//2, 150)
    draw_text(f"SCORE: {score}", font_small, colorWHITE, WIDTH//2, 220)
    
    if button("AGAIN", 300, "GAME"): 
        personal_best = get_personal_best(USER_NAME) 
        reset_game()
        STATE = "GAME"
    if button("MAIN MENU", 370, "MENU"): STATE = "MENU"

# TSIS 3.6 settings_screen
def settings_screen():
    global STATE, colorYELLOW, GRID_ON, SOUND_ON, current_settings
    screen.fill(colorBLACK)
    draw_text("SETTINGS", font_small, colorWHITE, WIDTH//2, 50)

   
    c_label = "COLOR: YELLOW" if current_settings["snake_color"] == [255, 255, 0] else "COLOR: BLUE"
    if button(c_label, 150, "CHANGE_COLOR"):
        if current_settings["snake_color"] == [255, 255, 0]:
            current_settings["snake_color"] = [0, 0, 255]
        else:
            current_settings["snake_color"] = [255, 255, 0]
        colorYELLOW = tuple(current_settings["snake_color"])
        save_settings(current_settings)
  
    g_label = f"GRID: {'ON' if GRID_ON else 'OFF'}"
    if button(g_label, 220, "TOGGLE_GRID"):
        GRID_ON = not GRID_ON
        current_settings["grid_on"] = GRID_ON
        save_settings(current_settings)

    s_label = f"SOUND: {'ON' if SOUND_ON else 'OFF'}"
    if button(s_label, 290, "TOGGLE_SOUND"):
        SOUND_ON = not SOUND_ON
        current_settings["sound_on"] = SOUND_ON
        save_settings(current_settings)

    if button("BACK TO MENU", 450, "MENU"):
        STATE = "MENU"

# TSIS 3.3 Power-ups    
class PowerUp:
    def __init__(self):
        self.pos = Point(0,0)
        self.type = None
        self.spawn_time = 0
        self.is_on_field = False
    
    def generate(self, snake_body, wall_blocks):
        self.pos.x = random.randint(0, (WIDTH // CELL) - 1)
        self.pos.y = random.randint(0, (HEIGHT // CELL) - 1)

        col_snake = any(p.x == self.pos.x and p.y == self.pos.y for p in snake_body)
        col_wall = any(p.x == self.pos.x and p.y == self.pos.y for p in wall_blocks)
        
        if col_snake or col_wall:
            self.generate(snake_body, wall_blocks)
        else:
            self.type = random.choice(['SPEED', 'SLOW', 'SHIELD'])
            self.spawn_time = pygame.time.get_ticks()
            self.is_on_field = True

    def draw(self):
        if self.is_on_field:
            color = (31,58,61) if self.type == 'SPEED' else (224, 86,0) if self.type == 'SLOW' else (77,93,83)
            pygame.draw.rect(screen, color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
            

reset_game()
running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # TSIS 3.1  1-4)username entry and personal best
        if STATE == 'INPUT_NAME' :
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and USER_NAME != '':
                    personal_best = get_personal_best(USER_NAME) 
                    STATE = 'GAME'
                elif event.key == pygame.K_BACKSPACE:
                    USER_NAME = USER_NAME[:-1]
                else:
                    USER_NAME += event.unicode
            
   
        if STATE == "GAME":
            if event.type == FOOD_SPW:
                food.generate(snake.body, wall.blocks)
                poison.generate(snake.body, wall.blocks)
        
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_RIGHT and snake.dx!= -1:
                    snake.dx = 1
                    snake.dy = 0
                elif event.key == pygame.K_LEFT and snake.dx!= 1:
                    snake.dx = -1
                    snake.dy = 0
                elif event.key == pygame.K_DOWN and snake.dy!= -1:
                    snake.dx = 0
                    snake.dy = 1
                elif event.key == pygame.K_UP and snake.dy!= 1:
                    snake.dx = 0
                    snake.dy = -1

        
    if STATE == 'MENU':
        menu_screen()
    elif STATE == 'SETTINGS':
        settings_screen()
    elif STATE == 'INPUT_NAME':
        input_name_screen()
    elif STATE == 'LEADERS':
        leaderboard_screen()
    elif STATE == 'GAME_OVER':
        game_over_screen()
    elif STATE == 'GAME':
        # TSIS 3.3 powerups
        current_time = pygame.time.get_ticks()
        if not powerup.is_on_field and current_time - POWERUP_SPAWN_TIME > 10000:
            powerup.generate(snake.body, wall.blocks)
            POWERUP_SPAWN_TIME = current_time

        if powerup.is_on_field and current_time - powerup.spawn_time > 8000:
            powerup.is_on_field = False
            POWERUP_SPAWN_TIME = current_time


        current_fps = FPS
        if current_time < active_effects["SPEED_END"]:
            current_fps += 5
        elif current_time < active_effects["SLOW_END"]:
            current_fps = max(3, current_fps - 3)



        snake.move()
        head = snake.body[0]

        if powerup.is_on_field and head.x == powerup.pos.x and head.y == powerup.pos.y:
            if powerup.type == 'SPEED':
                active_effects["SPEED_END"] = current_time + 5000
                active_effects["SLOW_END"] = 0 
            elif powerup.type == 'SLOW':
                active_effects["SLOW_END"] = current_time + 5000
                active_effects["SPEED_END"] = 0
            elif powerup.type == 'SHIELD':
                active_effects["SHIELD"] = True
            
            powerup.is_on_field = False
            POWERUP_SPAWN_TIME = current_time

        if snake.check_border():
            if active_effects["SHIELD"]:
                active_effects["SHIELD"] = False 
            else:
                save_game_result(USER_NAME, score, level)
                STATE = 'GAME_OVER'

        # TSIS 3.4 obstacles
        for block in wall.blocks:
            if head.x == block.x and head.y == block.y:
                if active_effects["SHIELD"]:
                    active_effects["SHIELD"] = False
                else:
                    save_game_result(USER_NAME, score, level)
                    STATE = 'GAME_OVER'

   
        if head.x == food.pos.x and head.y == food.pos.y:
            # Randomly generating food with different weights
            score += random.randint(1,4)
            food_on_lev += 1
            snake.body.append(Point(head.x,head.y))
            food.generate(snake.body,wall.blocks)

            pygame.time.set_timer(FOOD_SPW, 6000)

            if food_on_lev >= 3:
                level += 1
                food_on_lev = 0
                FPS += 2

                wall.generate(level, snake.body, food.pos, poison.pos)
                food.generate(snake.body, wall.blocks)
                poison.generate(snake.body, wall.blocks)
        
        # TSIS 3.2  poison food
        if head.x == poison.pos.x and head.y == poison.pos.y:
            if len(snake.body) > 2:
                snake.body = snake.body[:-2]
            else:
                STATE = 'GAME_OVER'
            poison.generate(snake.body,wall.blocks)


        screen.fill(colorWHITE)
        if GRID_ON:
            draw_grid_chess()

        wall.draw()
        snake.draw()
        food.draw()
        poison.draw()
        powerup.draw()

        draw_text(f'Score: {score} Lvl: {level} Your_Best: {personal_best}', font_small, colorBLACK, 10, 10, False)
        # TSIS 3.3  powerups
        font2 = pygame.font.SysFont("Verdana", 14)
        draw_text("Speed Boost", font2, (255, 188, 173), 10, 40, False)
        draw_text("Slow Motion", font2, (224, 86, 0), 10, 62, False)
        draw_text("Shield", font2, (77, 93, 83), 10, 84, False)
    pygame.display.flip()
    clock.tick(current_fps if STATE == 'GAME' else 60)

pygame.quit() 
