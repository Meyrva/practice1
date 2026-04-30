import pygame, sys, random


class Paint:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 15)
        
        
        self.radius = 15
        self.mode = 'blue'
        

        self.points = [] # a list for storing already completed lines 
        self.cur_points = [] # a list for the points of the line that drawing right now
        

        self.is_erace = False

        self.shapes =[]
        self.draw_shape = False
        self.start_pos = (0,0)
        self.shape_type = 0
        
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
            pygame.draw.circle(self.screen, color,start, width)
            return 
        
        for i in range(iterations):
            progress = 1.0 * i / iterations
            aprogress = 1 - progress
            x = int(aprogress * start[0] + progress * end[0])
            y = int(aprogress * start[1] + progress * end[1])
            pygame.draw.circle(self.screen, color, (x, y), width)

    
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
    def draw_figure(self, screen, type ,start, end,color):
            x1, y1 = start
            x2, y2 = end
            width = x2 - x1
            height = y2 - y1 
            # draw square
            if type == 0:
                pygame.draw.rect(screen, color, (x1, y1, width, height), 2)
            # draw right triangle
            elif type == 1:
                pygame.draw.polygon(screen, color, [(x1, y1), (x1, y2), (x2, y2)], 2)
            # draw equilateral triangle
            elif type == 2:
                pygame.draw.polygon(screen, color, [(x1 + width // 2, y1), (x1, y2), (x2, y2)], 2)
            # draw rhombus
            elif type == 3:
                points_rhomb = [
                    (x1 + width // 2, y1), 
                    (x2, y1 + height // 2),
                    (x1 + width // 2, y2), 
                    (x1, y1 + height // 2)  
                ]
                pygame.draw.polygon(screen, color, points_rhomb, 2)
            # draw cicrle
            elif type == 4:
                radius = int ((x2-x1))
                pygame.draw.circle(screen, color, (x1, y1), radius,2)
            # draw fixed square
            elif type == 5:
                pygame.draw.rect(screen, color, (x1, y1,  width, height),2)

    def run(self):  
        while True:
            mouse_pos = pygame.mouse.get_pos()
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
                    
                    # shape mode switching
                    elif event.key == pygame.K_d:
                        if not self.draw_shape:
                            self.draw_shape = True
                            self.start_pos = mouse_pos
                        else:
                            # switching the shape type
                            self.shape_type = (self.shape_type + 1)% 6
                if  event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 3: # right mouse button cancel drawing shapes
                        self.draw_shape = False

                    if event.button == 1 and self.draw_shape: # left mouse button save drawing shapes
                        color = (0, 0, 255) if self.mode == 'blue' else (255, 0, 0) if self.mode == 'red' else (0, 255, 0)
                        self.shapes.append({
                            'type': self.shape_type,
                            'start': self.start_pos,
                            'end': mouse_pos,
                            'color': color
                        })
                        self.draw_shape = False

            self.screen.fill((0, 0, 0))
            
            for sh in self.shapes:
                self.draw_figure(self.screen, sh['type'], sh['start'], sh['end'], sh['color'])

            for line in self.points:
                pts = line['line_points']
                for i in range(len(pts) - 1):
                    if line['line_erace']:
                        self.eraser(pts[i], pts[i+1], line['line_radius'])
                    else:
                        self.drawLineBetween(pts[i], pts[i+1], line['line_radius'], line['line_mode'])

            # getting the state of the mouse buttons (left, middle, right)
            if mouse_button[0] and not self.draw_shape:
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
           

            if self.cur_points:
                for i in range(len(self.cur_points) - 1):
                    if self.is_erace:
                        self.eraser(self.cur_points[i], self.cur_points[i+1], self.radius)
                    else:
                        self.drawLineBetween(self.cur_points[i], self.cur_points[i+1], self.radius, self.mode)



            key = self.font.render("R\G\B - colors \n W - Eraser \n clicl D - choose Shape",True, (255,255,255))
            self.screen.blit(key,(10,10))

            if self.draw_shape:
                color = (0, 0, 255) if self.mode == 'blue' else (255, 0, 0) if self.mode == 'red' else (0, 255, 0)
                self.draw_figure(self.screen, self.shape_type, self.start_pos, mouse_pos, color)
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Paint()
    game.run()

