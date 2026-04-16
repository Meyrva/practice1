import pygame

pygame.init()
screen = pygame.display.set_mode((400,300))

songs = [r'music\1.mp3', r'music\2.mp3',r'music\3.mp3']
cur = 0
pygame.mixer.music.load(songs[cur])

run = True
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p: 
                pygame.mixer.music.play()

            if event.key == pygame.K_s:
                pygame.mixer.music.stop()

            if event.key == pygame.K_n: 
                cur = (cur+1) % len(songs)
                pygame.mixer.music.load(songs[cur])
                pygame.mixer.music.play()

            if event.key == pygame.K_b:
                cur = (cur-1) % len(songs)
                pygame.mixer.music.load(songs[cur])
                pygame.mixer.music.play()
            
            if event.key == pygame.K_q:
                run = False
    
    screen.fill("black")
    font = pygame.font.SysFont("Verdana", 20)
    screen.blit(font.render("P = Play, S = Stop, N = Next track ", True, "white"), (30, 80))
    screen.blit(font.render("B = Previous, Q = Quit", True, "white"), (60, 100))
    screen.blit(font.render(f'{songs[cur][6:]} is playing now', True, "blue"), (80, 140))
    pygame.display.flip()

pygame.quit()