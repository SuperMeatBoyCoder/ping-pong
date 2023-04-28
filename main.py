from pygame import *
from random import randint


class GameSprite(sprite.Sprite): # Родительский класс для спрайтов
    def __init__(self, player_image, speed, player_x, player_y,\
                 size_x, size_y):
        super().__init__()
        
        self.image_name = player_image
        self.image = transform.scale(image.load(self.image_name), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self): # Обновление
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite): # Игрок
    def left_update(self): # Движение по WASD
        keys_pressed = key.get_pressed()
        if keys_pressed[K_s] and self.rect.y < win_height-110:
            self.rect.y += self.speed
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
    def right_update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_DOWN] and self.rect.y < win_height-110:
            self.rect.y += self.speed
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed

class Ball(GameSprite):
    def __init__(self, player_image, speed, player_x, player_y, size_x, size_y):
        super().__init__(player_image, speed, player_x, player_y, size_x, size_y)
        self.direction_y = randint(0, 1)
        self.direction_y = (self.direction_y-0.5)*2
        self.direction_x = randint(0, 1)
        self.direction_x = (self.direction_x-0.5)*2
        
    def update(self):
        global win_l, win_r
        
        self.rect.y += self.speed*self.direction_y
        self.rect.x += self.speed*self.direction_x

        if self.rect.y < 10 or self.rect.y > 460:
            self.direction_y *= -1
        if sprite.collide_rect(ball, player_1) or sprite.collide_rect(ball, player_2):
            self.direction_x *= -1

        if self.rect.x < 0:
            win_r += 1
            self.direction_x *= -1
        elif self.rect.x > 670:
            win_l += 1
            self.direction_x *= -1


# Приложение
win_width, win_height = 700, 500
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('bg.jpg'), (700, 500))
window.blit(background, (0,0))
display.set_caption('Пинг-понг')

# Надписи
font.init()
font = font.Font(None, 36)

# Объекты
player_1 = Player('platform.jpeg', speed=5, player_x=10, player_y=250, size_x=10, size_y=100)
player_2 = Player('platform.jpeg', speed=5, player_x=680, player_y=250, size_x=10, size_y=100)
ball = Ball('ball.png', speed=7, player_x=335, player_y=235, size_x=30, size_y=30)

# Создание предметов
clock = time.Clock()
FPS = 30
game = True
finish = False
win_l = 0
win_r = 0
while game:
    
    # Закрытие приложения по кнопке
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5:
                    fire.play()
                    Hero.fire()
                    # num_fire += 1
                else:
                    num_fire = 0

    if finish != True:
        # Обновление

        window.blit(background, (0,0))
        player_1.left_update()
        player_1.reset()
        player_2.right_update()
        player_2.reset()
        ball.update()
        ball.reset()
        l_font = font.render('Счёт левого: ' + str(win_l), True, (255, 215, 0))
        r_font = font.render('Счёт правого: ' + str(win_r), True, (255, 215, 0))
        window.blit(r_font, (480, 0))
        window.blit(l_font, (30, 0))

        # Выигрыш и проигрыш
        if win_l >= 5 or win_r >= 5:
            if win_l >= 5:
                win_font = font.render('Победа левого!', True, (255, 215, 0))
            else:
                win_font = font.render('Победа правого!', True, (255, 215, 0))
            window.blit(win_font, (250, 200))
            finish = True
    
    display.update()
    clock.tick(FPS)
