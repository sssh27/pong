import sys
import pygame
from pygame.locals import QUIT
import random
import time

pygame.init()
    
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLDEN = (255, 215, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

width = 700
height = 500
    
window = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
    

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.surf = pygame.Surface([width, height])
        self.rect = self.surf.get_rect()
        self.color = color
    
    def moveup(self, pixels):
        self.rect.y -= pixels
        if self.rect.y <= 0:
            self.rect.y = 0
            
    def movedown(self, pixels):
        self.rect.y += pixels
        if self.rect.y >= 400:
            self.rect.y = 400
    def update(self):
        pygame.draw.rect(window, self.color, self.rect)

        
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.surf = pygame.Surface([width, height])
        self.color = color
        self.rect = self.surf.get_rect()
        self.dirc = [random.choices([-1,1])[0]*random.randint(4,8), random.choices([-1,1])[0]*random.randint(4,8)]
    
    def bounce(self):
        self.dirc[0] = -self.dirc[0]*1.03
        self.dirc[1] = self.dirc[1]*1.03
        
    def update(self):
        self.rect.x += self.dirc[0]
        self.rect.y += self.dirc[1]
        pygame.draw.rect(window, self.color, self.rect)
    
    def ball_reset(self):
        super().__init__()
        self.rect.x = width/2 
        self.rect.y = height/2 
        time.sleep(1.5)
        self.dirc = [random.choices([-1,1])[0]*random.randint(4,8), random.choices([-1,1])[0]*random.randint(4,8)]
        
    
paddle1 = Paddle(RED, 15, 100) 
paddle1.rect.x = 4
paddle1.rect.y = 200

paddle2 = Paddle(BLUE, 15, 100)
paddle2.rect.x = 682
paddle2.rect.y = 200

ball = Ball(GOLDEN, 13, 13)
ball.rect.x = 345
ball.rect.y = 195

scoreA = 0
scoreB = 0
winning_score = 10

while True:
    for event in pygame.event.get():     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1.moveup(10)
    if keys[pygame.K_s]:
        paddle1.movedown(10)
    if keys[pygame.K_UP]:
        paddle2.moveup(10)
    if keys[pygame.K_DOWN]:
        paddle2.movedown(10)
    
        
    if ball.rect.x >= 680:
        ball.dirc[0] = -ball.dirc[0]
        scoreA += 1
        ball.ball_reset()
        
    if ball.rect.x <= 0:
        ball.dirc[0] = -ball.dirc[0]
        scoreB += 1
        ball.ball_reset()
    
    if ball.rect.y >= 480 or ball.rect.y <= 0:
        ball.dirc[1] = -ball.dirc[1]
    
    if pygame.sprite.collide_rect(ball, paddle1) or pygame.sprite.collide_rect(ball, paddle2):
        ball.bounce()
    
    window.fill((100, 100, 100))
    
    paddle1.update()
    paddle2.update()
    ball.update()
    
    font = pygame.font.Font(None, 60)
    text = font.render(str(scoreA), 1, WHITE)
    window.blit(text, (250,10))
    text = font.render(str(scoreB), 1, WHITE)
    window.blit(text, (420,10))
 
    won = False
    if scoreA >= winning_score:
        won = True
        win_text = 'RED WON!!'
    if scoreB >= winning_score:
        won = True
        win_text = 'BLUE WON!!'
         
    if won:        
        font = pygame.font.Font(None, 120)
        text = font.render(win_text, 1, WHITE)
        window.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pygame.display.update()
        time.sleep(6)
        ball.ball_reset()
        scoreA = 0
        scoreB = 0

    clock.tick(50)        
    pygame.display.flip()