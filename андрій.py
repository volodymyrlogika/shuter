from pygame import *
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
img_back = "galaxy.jpg"
img_hero = "rocket.png"
class  GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x,  self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
        if keys[K_SPACE]:
            self.fire()

    def fire(self):
        b = Bullet("bullet.png", self.rect.centerx - 8, self.rect.y, 15, 20, 15)
        bullets.add(b)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_widht - 80)
            self.rect.y = 0
            

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
ship = Player (img_hero, 300, win_height-100, 80, 100, 5)
monsters = sprite.Group()
bullets = sprite.Group()
finish = False
game = True

while game:
    for e in even.get():
        if   e.type ==  QUIT:
            game = False
    if  not finish:
        window.blit(background, (0,  0))
        ship.update()
        ship.reset()
        display.update()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)

