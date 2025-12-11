import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode()
(WIDTH, HEIGHT) = pygame.display.get_window_size()
pygame.display.set_caption("snake 2")
print(WIDTH, HEIGHT)

clock = pygame.time.Clock()
FPS = 10

squareN = 80
squareS = WIDTH/squareN
squareNV = int(HEIGHT//squareS)
print(squareNV)

class Snake():
    def __init__(self, x, y, col):
        self.segments = [Segment(x, y), Segment(-50, -50), Segment(-50, -50), Segment(-50, -50)]
        self.dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        self.dirdic = {
            "r":0, "d":1, "l":2, "u":3,
        }
        self.dir = 0
        self.dirpending = 0
        self.appendNext = False
        self.colour = col
    
    def update(self, apples, snake2):
        global running

        for apple in apples:
            if (self.checkApple(apple)):
                self.appendNext = True
        
        if self.checkCollide(snake2):
            pygame.quit()

        self.moveSegments()

        self.render()
    
    def setdir(self, dir):
        newdir = self.dirdic[dir]
        if not (abs(self.dir - newdir) == 2):
            self.dirpending = newdir
    
    def render(self):
        for segment in self.segments:
            pygame.draw.rect(screen, self.colour, (segment.x, segment.y, squareS, squareS))
    
    def checkApple(self, apple):
        if (self.segments[0].x == apple.x and self.segments[0].y == apple.y):
            apple.setApple()
            return True
        return False
    
    def checkCollide(self, snake2):
        head = self.segments[0]
        for o in range (1, len(self.segments)):
            item = self.segments[o]
            if head.x == item.x and head.y == item.y:
                print("COLLIDE")
                return True

        for seg in snake2.segments:
            if seg.x == head.x and seg.y == head.y:
                print("SNAKE COLLIDE")
                return True
        
        if head.x > WIDTH or head.y > HEIGHT or head.y < 0 or head.x < 0:
            print("WALLCOLLIDE")
            return True
        return False

    def moveSegments(self):
        if self.appendNext:
            self.segments.append(Segment(0, 0))
            self.appendNext = False

        nxt = self.segments[len(self.segments)-1]
        c = len(self.segments)-2
        while c > -1:
            item = self.segments[c]
            nxt.x = item.x
            nxt.y = item.y
            nxt = item
            c-=1

        head = self.segments[0]
        head.x += squareS*(self.dirs[self.dirpending][0])
        head.y += squareS*(self.dirs[self.dirpending][1])

        self.dir = self.dirpending


class Segment():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Apple():
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def render(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, squareS, squareS))
    
    def setApple(self):
        global apples

        self.x = random.randint(0, squareN-1)*squareS
        self.y = random.randint(0, squareNV-1)*squareS

        for apple in apples:
            if self.x == apple.x and self.y == apple.y and apple != self:
                self.setApple()



# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

snake = Snake((squareN//3)*squareS, (squareNV//3)*squareS, GREEN)
snake2 = Snake((2*squareN//3)*squareS, (2*squareNV//3)*squareS, BLUE)

applenum = 10
apples = []
for a in range(applenum):
    newapp = Apple()
    apples.append(newapp)
    newapp.setApple()

# --- Main Game Loop ---
running = True
while running:
    clock.tick(FPS)  # Limit FPS

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.setdir("l")
            if event.key == pygame.K_RIGHT:
                snake.setdir("r")
            if event.key == pygame.K_UP:
                snake.setdir("u")
            if event.key == pygame.K_DOWN:
                snake.setdir("d")

            if event.key == pygame.K_a:
                snake2.setdir("l")
            if event.key == pygame.K_d:
                snake2.setdir("r")
            if event.key == pygame.K_w:
                snake2.setdir("u")
            if event.key == pygame.K_s:
                snake2.setdir("d")
    
    # --- Drawing ---
    screen.fill(GREY)  # Clear screen

    for apple in apples:
        apple.render()

    snake.update(apples, snake2)
    snake2.update(apples, snake)

    for i in range (squareN):
        pygame.draw.rect(screen, BLACK, (i*squareS, 0, 5, HEIGHT))
        pygame.draw.rect(screen, BLACK, (0, i*squareS, WIDTH, 5))

    pygame.display.flip()  # Update display

pygame.quit()
sys.exit()