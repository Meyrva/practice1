import pygame, sys, random


class Paint:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 15)
        
        
        self.radius = 15
        self.mode = 'blue'
        

        self.points = [] # A list for storing already completed lines 
        self.cur_points = [] # A list for the points of the line that drawing right now
        
        self.circle_x, self.circle_y = 320, 240
        self.rect_x, self.rect_y = 300, 240

        self.is_erace = False
        self.draw_circle = False
        self.draw_rect = False

    def drawLineBetween(self, start, end, width, color_mode):
        
        if color_mode == 'blue':
            color = (0, 0, 255)
        elif color_mode == 'red':
            color = (255, 0, 0)
        elif color_mode == 'green':
            color = (0, 255, 0)
        
        dx = start[0] - end[0]
        dy = start[1] - end[1]
        iterations = max(abs(dx), abs(dy))
        
        if iterations == 0:
            pygame.draw.circle(self.screen, color, (x, y), width)
            return 
        
        for i in range(iterations):
            progress = 1.0 * i / iterations
            aprogress = 1 - progress
            x = int(aprogress * start[0] + progress * end[0])
            y = int(aprogress * start[1] + progress * end[1])
            pygame.draw.circle(self.screen, color, (x, y), width)

    def circle(self):
        pygame.draw.circle(self.screen, self.mode, (self.circle_x, self.circle_y), 50)

    def rectangle(self):
        pygame.draw.rect(self.screen, self.mode, (self.rect_x, self.rect_y, 100, 100))
    
    def eraser(self, start, end, width):
        dx = start[0] - end[0]
        dy = start[1] - end[1]
        iterations = max(abs(dx), abs(dy))
        if iterations == 0: 
            pygame.draw.circle(self.screen, (0, 0, 0), start, width)
        
        for i in range(iterations):
            progress = 1.0 * i / iterations
            aprogress = 1 - progress
            x = int(aprogress * start[0] + progress * end[0])
            y = int(aprogress * start[1] + progress * end[1])
            pygame.draw.circle(self.screen, (0, 0, 0), (x, y), width)

    def run(self):  
        while True:
            mouse_button = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                
                    # if a letter key was pressed
                    if event.key == pygame.K_r:
                        self.mode = 'red'
                    elif event.key == pygame.K_g:
                        self.mode = 'green'
                    elif event.key == pygame.K_b:
                        self.mode = 'blue'
                    elif event.key == pygame.K_w:
                        self.is_erace = not self.is_erace
                    elif event.key == pygame.K_c:
                        self.draw_circle = not self.draw_circle
                        if self.draw_circle: 
                            self.circle_x = random.randint(50, 590)
                            self.circle_y = random.randint(50, 430)
                    elif event.key == pygame.K_e:
                        self.draw_rect = not self.draw_rect
                        if self.draw_rect: 
                            self.rect_x = random.randint(0, 540)
                            self.rect_y = random.randint(0, 380)
                    

            # Getting the state of the mouse buttons (left, middle, right)
            if mouse_button[0]:
                position = pygame.mouse.get_pos()
                if not self.cur_points or self.cur_points[-1] != position:
                    self.cur_points.append(position)
            else:
                if self.cur_points:
                    self.points.append({
                        'line_points': self.cur_points,
                        'line_mode': self.mode,
                        'line_erace': self.is_erace,
                        'line_radius': self.radius
                    })
                    self.cur_points = []


            self.screen.fill((0, 0, 0))

            key = self.font.render("R\G\B - colors \n W - Eraser \n C\E - Shapes",True, (255,255,255))
            self.screen.blit(key,(10,10))
           

            if self.draw_circle:
                self.circle()
            if self.draw_rect:
                self.rectangle()

            # draw lines
            
            for line in self.points:
                pts = line['line_points']
                for i in range(len(pts) - 1):
                    if line['line_erace']:
                        self.eraser(pts[i], pts[i+1], line['line_radius'])
                    else:
                        self.drawLineBetween(pts[i], pts[i+1], line['line_radius'], line['line_mode'])

            # draw the line that are drawing now
            if self.cur_points:
                for i in range(len(self.cur_points) - 1):
                    if self.is_erace:
                        self.eraser(self.cur_points[i], self.cur_points[i+1], self.radius)
                    else:
                        self.drawLineBetween(self.cur_points[i], self.cur_points[i+1], self.radius, self.mode)
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Paint()
    game.run()

