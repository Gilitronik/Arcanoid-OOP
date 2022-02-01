import pygame
from random import choice, random

FPS = 60
 

pygame.init()
screen = pygame.display.set_mode((1920, 1000))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)


# colors
GRAY = (155, 155, 155)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
PUMPKIN_COLOR = (255, 117, 24)

# other things
score = 0
PLATFORM_SIZE_XY = (100, 30)
right_panel_width = 200

class Platform:
    def __init__(self, pos: tuple[2], size: tuple[2]) -> None:
        self.pos = pos
        self.size = size
        self.dir = 0
        self.draw()

    def draw(self) -> None:
        pygame.draw.rect(screen, WHITE, (*self.pos, *self.size))
    
    def move(self) -> None:
        x, y = self.pos
        x += 7 * self.dir
        if x <= 0:
            x = 0
        elif x + self.size[0] > screen.get_width() - right_panel_width:
            x = screen.get_width() - self.size[0] - right_panel_width

        self.pos = (x, y)
        self.draw()

    def handle_event(self, down: bool, key: str):
        if down:
            if key == 'right':
                self.dir += 1
            elif key == 'left':
                self.dir -= 1
            else:
                raise Exception('ЧТО ЗА КЛАВИШУ ТЫ МНЕ ДАЛ!!!!?????')
        else:
            if key == 'right':
                self.dir -= 1
            elif key == 'left':
                self.dir += 1
            else:
                raise Exception('ЧТО ЗА КЛАВИШУ ТЫ МНЕ ДАЛ!!!!?????')

    def collision(self, obj):
        if obj.pos[1] + obj.size >= self.pos[1] and obj.pos[0] + obj.size >= self.pos[0] and self.pos[0] + self.size[0] >= obj.pos[0]: 
            obj.pos = (obj.pos[0], self.pos[1] - obj.size)
            obj.speed = (obj.speed[0], -obj.speed[1])


            
class Square:
    def __init__(self, pos: tuple[2], size, speed=(10, 3)) -> None:
        self.pos = pos
        self.size = size
        self.speed = speed
        self.draw()

    def draw(self) -> None:
        pygame.draw.rect(screen, choice((RED, GREEN, BLUE, YELLOW, PUMPKIN_COLOR)), (*self.pos, self.size, self.size))
    
    def move(self, objects) -> None:
        x, y = self.pos
        vx, vy = self.speed
        x += vx
        y += vy

        if x <= 0:
            x = 0
            vx = -vx
        elif x + self.size > screen.get_width() - right_panel_width:
            x = screen.get_width() - self.size - right_panel_width
            vx = -vx

        if y <= 0:
            y = 0
            vy = -vy
        elif y + self.size > screen.get_height():
            y = screen.get_height() - self.size
            vy = -vy
            objects.remove(obj)
            return

        self.pos = (x, y)
        self.speed = (vx, vy)
        self.draw()


def draw_background():
    screen.fill(BLACK)
    pygame.draw.rect(screen, GRAY, (screen.get_width() - right_panel_width, 0, screen.get_width(), screen.get_height()))


objects = set()
for i in range(30):
    objects.add(Square((0, 0), 20, (random() * 10, random() * 10)))

platform = Platform((30, screen.get_height() - 50), PLATFORM_SIZE_XY)

while True:
    clock.tick(FPS)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                platform.handle_event(True, 'right')
            elif event.key == pygame.K_a:
                platform.handle_event(True, 'left')
 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                platform.handle_event(False, 'right')
            elif event.key == pygame.K_a:
                platform.handle_event(False, 'left')
 
    
    draw_background()
    for obj in set(objects):
        obj.move(objects)
        platform.collision(obj)
    score += len(objects)
    text1 = font.render(f'Очки: {(score)//100}', True, (255, 0, 0))
    text2 = font.render(f'Живых: {(len(objects))}', True, (255, 0, 0))
    screen.blit(text1, (screen.get_width() - right_panel_width, 0))
    screen.blit(text2, (screen.get_width() - right_panel_width, 100))
    platform.move()
    pygame.display.update()
