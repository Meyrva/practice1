import pygame, sys
from datetime import datetime


class Paint:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 15)
        
        
        self.radius = 5
        self.mode = 'blue'
        self.tool = 'brush'

        self.points = [] # a list for storing already completed lines 
        self.cur_points = [] # a list for the points of the line that drawing right now
        

        self.is_erace = False

        self.shapes =[]
        self.draw_shape = False
        self.start_pos = (0,0)
        self.shape_type = 0

        #TSIS 3.3  canvas for the fill tool
        self.canvas = pygame.Surface((640,480))
        self.canvas.fill((0,0,0))

        # TSIS 3.5   text tool
        self.text = ""
        self.text_pos = (0, 0)
        self.is_typing = False
        self.text_font = pygame.font.SysFont("Verdana", 20) 
        
    def drawLineBetween(self, start, end, color_mode, radius):
        
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
            pygame.draw.circle(self.canvas, color,start, radius)
            return 
        
        for i in range(iterations):
            progress = 1.0 * i / iterations
            aprogress = 1 - progress
            x = int(aprogress * start[0] + progress * end[0])
            y = int(aprogress * start[1] + progress * end[1])
            pygame.draw.circle(self.canvas, color, (x, y), radius)

    # TSIS 3.1   1)Pencil tool 
    def drawPencil(self, start, end, color_mode,radius):
        if color_mode == 'blue':
            color = (0, 0, 255)
        elif color_mode == 'red':
            color = (255, 0, 0)
        elif color_mode == 'green':
            color = (0, 255, 0)

        pygame.draw.line(self.canvas, color, start, end, radius)

    # TSIS 3.3  fill tool
    def flood_fill(self,x,y, new_color):
        color = self.canvas.get_at((x,y))
        if color == new_color:
            return

        vals = [(x,y)]
        while vals:
            cur_x, cur_y = vals.pop()

            if cur_x < 0 or cur_x >= 640 or cur_y < 0 or cur_y >= 480:
                continue
            if self.canvas.get_at((cur_x, cur_y)) == color:
                self.canvas.set_at((cur_x, cur_y), new_color)

                vals.append((cur_x + 1, cur_y))
                vals.append((cur_x - 1, cur_y))
                vals.append((cur_x, cur_y + 1))
                vals.append((cur_x, cur_y - 1))

    # TSIS 3.5   text tool
    def render_text_to_canvas(self):
        if self.text:
            color = (0, 0, 255) if self.mode == 'blue' else (255, 0, 0) if self.mode == 'red' else (0, 255, 0)
            text_surf = self.text_font.render(self.text, True, color)
            self.canvas.blit(text_surf, self.text_pos)
        self.is_typing = False
        self.text = ""



    def eraser(self, start, end,radius):
        dx = start[0] - end[0]
        dy = start[1] - end[1]
        iterations = max(abs(dx), abs(dy))
        if iterations == 0: 
            pygame.draw.circle(self.canvas, (0, 0, 0), start, radius)
        
        for i in range(iterations):
            progress = 1.0 * i / iterations
            aprogress = 1 - progress
            x = int(aprogress * start[0] + progress * end[0])
            y = int(aprogress * start[1] + progress * end[1])
            pygame.draw.circle(self.canvas, (0, 0, 0), (x, y), radius)

    def draw_figure(self, screen, type ,start, end,color, radius):
            x1, y1 = start
            x2, y2 = end
            width = x2 - x1
            height = y2 - y1 
            # draw square
            if type == 0:
                pygame.draw.rect(screen, color, (x1, y1, width, height), radius)
            # draw right triangle
            elif type == 1:
                pygame.draw.polygon(screen, color, [(x1, y1), (x1, y2), (x2, y2)], radius)
            # draw equilateral triangle
            elif type == 2:
                pygame.draw.polygon(screen, color, [(x1 + width // 2, y1), (x1, y2), (x2, y2)], radius)
            # draw rhombus
            elif type == 3:
                points_rhomb = [
                    (x1 + width // 2, y1), 
                    (x2, y1 + height // 2),
                    (x1 + width // 2, y2), 
                    (x1, y1 + height // 2)  
                ]
                pygame.draw.polygon(screen, color, points_rhomb, radius)
            # draw cicrle
            elif type == 4:
                radius = int ((x2-x1))
                pygame.draw.circle(screen, color, (x1, y1), radius, radius)
            # draw fixed square
            elif type == 5:
                pygame.draw.rect(screen, color, (x1, y1,  width, height),radius)

            # TSIS 3.1   2)straight line tool 
            elif type == 6:
                pygame.draw.line(screen, color, start, end, radius)

    def run(self):  
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_button = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:

                    # TSIS3.5   text tool
                    if self.is_typing:
                        if event.key == pygame.K_RETURN:
                            self.render_text_to_canvas()
                        elif event.key == pygame.K_ESCAPE:
                            self.is_typing = False
                            self.text = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            if event.unicode.isprintable():
                                self.text += event.unicode
                        continue

                    if event.key == pygame.K_t:
                        self.tool = 'text'
                        self.is_typing = True
                        self.text = ""
                        self.text_pos = pygame.mouse.get_pos() 

                    # if a letter key was pressed
                    if event.key == pygame.K_r:
                        self.mode = 'red'
                    elif event.key == pygame.K_g:
                        self.mode = 'green'
                    elif event.key == pygame.K_b:
                        self.mode = 'blue'
                    elif event.key == pygame.K_w:
                        self.is_erace = not self.is_erace

                    # TSIS 3.1   1)switch to pencil tool 
                    elif event.key == pygame.K_p:
                        self.tool = 'pencil'
                        self.draw_shape = False
                    # TSIS 3.1   2)switch to straight line tool 
                    elif event.key == pygame.K_l:
                        self.draw_shape = True
                        self.shape_type = 6
                        self.start_pos = mouse_pos
                    # switch to brush
                    elif event.key == pygame.K_f:
                        self.tool = 'brush'
                        
                    # TSIS 3.2    switch between sizes
                    elif event.key == pygame.K_1:
                        self.radius = 2
                    elif event.key == pygame.K_2:
                        self.radius = 5
                    elif event.key == pygame.K_3:
                        self.radius = 10

                    # TSIS 3.3   switch to fill tool
                    elif event.key == pygame.K_n: 
                        self.tool = 'fill'
                        self.draw_shape = False
                    # TSIS 3.4   save canvas
                    elif event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        name = f"{now}.png"
                        pygame.image.save(self.canvas, name)
                        print("Canvas saved as", name)


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

                    if event.button == 1 : # left mouse button save drawing shapes
                        color = (0, 0, 255) if self.mode == 'blue' else (255, 0, 0) if self.mode == 'red' else (0, 255, 0)
                        
                        if self.tool == 'fill':
                            self.flood_fill(event.pos[0], event.pos[1],color)
                        elif self.draw_shape:
                            self.draw_figure(self.canvas, self.shape_type, self.start_pos, mouse_pos, color, self.radius)
                            self.draw_shape = False


                    # TSIS 3.5   text tool
                
                        elif self.tool == 'text':
                            if not self.is_typing:
                                self.is_typing = True
                                self.text_pos = event.pos
                                self.text = "" 
                            else:
                                self.render_text_to_canvas()
            

                #TSIS 3.5 character input
                if event.type == pygame.KEYDOWN and self.is_typing:
                    if event.key == pygame.K_RETURN: 
                        self.render_text_to_canvas()
                    elif event.key == pygame.K_ESCAPE: 
                        self.is_typing = False
                        self.text = ""
                    elif event.key == pygame.K_BACKSPACE: 
                        self.text = self.text[:-1]
                    else:
                        if event.unicode.isprintable():
                            self.text += event.unicode


            # getting the state of the mouse buttons (left, middle, right)
            if mouse_button[0] and not self.draw_shape and self.tool != 'fill':
                position = pygame.mouse.get_pos()
                if self.cur_points :
                    if self.is_erace:
                        self.eraser(self.cur_points[-1], position, self.radius)
                    elif self.tool == 'pencil':
                        self.drawPencil(self.cur_points[-1], position, self.mode, self.radius)
                    else:
                        self.drawLineBetween(self.cur_points[-1], position, self.mode, self.radius)
                self.cur_points.append(position)
            else:
                self.cur_points = []
           
            self.screen.fill((0,0,0))
            self.screen.blit(self.canvas, (0,0))


            key = self.font.render("1-small, 2-med, 3-big \nR\G\B - colors \n W - on|off Eraser \n D - Shapes \n P\L - pencil|straight line tool \n N\F\T - fill|brush|text",True, (255,255,255))
            self.screen.blit(key,(10,10))

            if self.draw_shape:
                color = (0, 0, 255) if self.mode == 'blue' else (255, 0, 0) if self.mode == 'red' else (0, 255, 0)
                self.draw_figure(self.screen, self.shape_type, self.start_pos, mouse_pos, color,self.radius)
            

           
            if self.is_typing:
                color = (0, 0, 255) if self.mode == 'blue' else (255, 0, 0) if self.mode == 'red' else (0, 255, 0)
                temp_text = self.text_font.render(self.text + "|", True, color)
                self.screen.blit(temp_text, self.text_pos)

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Paint()
    game.run()

