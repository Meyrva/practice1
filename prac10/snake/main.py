import pygame, random

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 30   

colorWHITE = (255, 255, 255)
colorGRAY = (200, 200, 200)
colorBLACK = (0, 0, 0)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorBLUE = (0, 0, 255)
colorYELLOW = (255, 255, 0)

screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption('Snake Game Levels')

font = pygame.font.SysFont("Verdana", 20)


def draw_grid():
    for i in range(HEIGHT // 2):
        for j in range(WIDTH // 2):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

def draw_grid_chess():
    colors = [colorWHITE, colorGRAY]

    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"

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
    def __init__(self, snake_body):
        self.pos = Point(0,0)
        self.generate(snake_body)

    def generate(self, snake_body):
        while True:
            self.pos.x = random.randint(0,(WIDTH//CELL) - 1)
            self.pos.y = random.randint(0,(WIDTH//CELL) - 1)
            colision_with_snake = False

            for part in snake.body:
                if part.x == self.pos.x and part.y == self.pos.y:
                    colision_with_snake = True
            if not colision_with_snake:
                break
    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))


FPS = 5
clock = pygame.time.Clock()

snake = Snake()
food = Food(snake.body)


score = 0
level =1
food_on_lev = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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

    snake.move()
    if snake.check_border():
        over = font.render(f'Score: {score} Level: {level}', True, colorBLACK)
        screen.blit(over, (10,10))
        running = False

    head = snake.body[0]
    if head.x == food.pos.x and head.y == food.pos.y:
        score += 1
        food_on_lev += 1
        snake.body.append(Point(head.x,head.y))
        food.generate(snake.body)

        if food_on_lev >= 3:
            level += 1
            food_on_lev = 0
            FPS += 2

    draw_grid_chess()
    snake.draw()
    food.draw()

    score_srf = font.render(f'Score: {score} Level: {level}', True, colorBLACK)
    screen.blit(score_srf, (10,10))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()