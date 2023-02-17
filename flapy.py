import pygame
from random import randint
pygame.init()

WIDTH, HEIGHT = 800, 600
pygame.display.set_caption('FlappyDog')
programIcon = pygame.image.load('images/icon.ico')
pygame.display.set_icon(programIcon)
fps = 60

font = pygame.font.Font(None, 80)
score = 0
frame = 0
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

imgplayer = pygame.image.load('images/pngegg.png')

py, sy, ay = HEIGHT // 2, 0, 0
player = pygame.Rect(WIDTH // 3, py, 44, 34)        

state = 'start'
timer = 10

pipes = []
pipesScore = []
pipesSpeed = 3
pipesSize = 200
pipesPos = HEIGHT // 2

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
            
    press = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    click = press[0] or keys[pygame.K_SPACE]
    
    frame = (frame + 0.2) % 4
    pipesSpeed = 3 + score // 100
    
    for i in range (len(pipes)-1, -1, -1):
        pipe = pipes[i]
        pipe.x -= pipesSpeed
        
        if pipe.right  < 0:
            pipes.remove(pipe)
            if pipe in pipesScore:
                pipesScore.remove(pipe)
    
    if timer > 0:
        timer -= 1
        
    if state == 'start':
        if click and timer == 0 and len(pipes) == 0: 
            state = 'play'
            
        py += (HEIGHT // 2 - py) * 0.1
        player.y = py
    elif state == 'play':
        if click:
            ay = -2
        else:
            ay = 0
            
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py
        
        if len(pipes) == 0 or pipes[len(pipes)-1].x < WIDTH - 200:
            pipes.append(pygame.Rect(WIDTH, 0, 50, pipesPos - pipesSize // 2))
            pipes.append(pygame.Rect(WIDTH, pipesPos + pipesSize // 2, 50, HEIGHT - pipesPos + pipesSize))
            
            pipesPos += randint(-100, 100)
            if pipesPos < pipesSize:
                pipesPos = pipesSize
            elif pipesPos > HEIGHT - pipesSize:
                pipesPos = HEIGHT - pipesSize
                
        if player.top < 0 or player.bottom > HEIGHT:
            state == 'fall'
            
        for pipe in pipes:
            if player.colliderect(pipe):
                state = 'fall'
                
            if pipe.right < player.right and pipe not in pipesScore:
                pipesScore.append(pipe)
                score += 5 
            
    elif state == 'fall':
        sy, ay = 0, 0
        pipesPos = HEIGHT // 2
        state = 'start'
        score = 0
        timer = 60
    else:
        pass
            
    window.fill(pygame.Color('black'))
    for pipe in pipes:
        pygame.draw.rect(window, pygame.Color('orange'), pipe) 
    
    image = imgplayer.subsurface(0, 0, 44, 34)
    image = pygame.transform.rotate(image, -sy * 2)
    window.blit(image, player)
    
    text = font.render('ОЧКИ: ' + str(score), 1, pygame.Color('white'))
    window.blit(text, (10, 10))
            
    pygame.display.update()
    clock.tick(fps)
pygame.quit()