import pygame, sys


class Paint:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 15)
        
        
        self.radius = 15
        self.mode = 'blue'
        self.points = []

        self.draw_circle = False
        self.draw_rect = False
    def drawLineBetween(self, start, end, width, color_mode):
        
        if color_mode == 'blue':
            color = (0, 0, 255)
        elif color_mode == 'red':
            color = (255, 0, 0)
        elif color_mode == 'green':
            color = (0, 255, 0)
        
        dx = start[0]
        dy = start[1]
        iterations = max(abs(dx), abs(dy))
        
        for i in range(iterations):
            progress = 1.0 * i / iterations
            aprogress = 1 - progress
            x = int(aprogress * start[0] + progress * end[0])
            y = int(aprogress * start[1] + progress * end[1])
            pygame.draw.circle(self.screen, color, (x, y), width)

    def circle(self):
        pygame.draw.circle(self.screen, self.mode,(320,240), 50 ) 

    def rectangle(self):
        pygame.draw.rect(self.screen, self.mode,(300,240,100,100), 50 ) 

    def run(self):  
        while True:
            
            mouse_button = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                
                # determin if X was clicked, or Ctrl+W or Alt+F4 was used
                if event.type == pygame.QUIT:
                    return
                
                
                if event.type == pygame.KEYDOWN:
                
                    # if a letter key was pressed
                    if event.key == pygame.K_r:
                        self.mode = 'red'
                    elif event.key == pygame.K_g:
                        self.mode = 'green'
                    elif event.key == pygame.K_b:
                        self.mode = 'blue'
                    elif event.key == pygame.K_c:
                        self.draw_circle = not self.draw_circle
                    elif event.key == pygame.K_e:
                        self.draw_rect = not self.draw_rect

            # Getting the state of the mouse buttons (left, middle, right)
            if mouse_button[0]:
                position = pygame.mouse.get_pos()
                if not self.points or self.points[-1] != position:
                    self.points.append(position)
                    self.points = self.points[-256:]


            self.screen.fill((0, 0, 0))
            key = self.font.render("press to change color\n'r' to red\n'g' to green\n'b' to blue",True, (255,255,255))
            self.screen.blit(key,(10,10))
            shapes = self.font.render("press to draw\n'c' cicrle\n'e' rectangle",True, (255,255,255))
            self.screen.blit(shapes,(530, 10))

            if self.draw_circle:
                self.circle()
            if self.draw_rect:
                self.rectangle()
            # draw all points
            i = 0
            while i < len(self.points) - 1:
                self.drawLineBetween( self.points[i], self.points[i + 1], self.radius, self.mode)
                i += 1
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Paint()
    game.run()

