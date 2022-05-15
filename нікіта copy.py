#Створи власний Шутер!

from random import randint
from pygame import *
mixer.init()
font.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)
fire_sound = mixer.Sound('fire.ogg')

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'

win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

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
        b = Bullet("bullet.png", self.rect.centerx - 7, self.rect.y, 15, 20, 15)
        bullets.add(b)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -100
            lost = lost +1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Button():
    def __init__(self, text, font, text_color, handler, x, y):
        self.text = font.render(text, True, text_color)
        self.handler = handler
        self.rect = self.text.get_rect() 
        self.rect.x = x
        self.rect.y = y       
        self.fill_color = (255,255,255)

    def update(self):
        draw.rect(window, self.fill_color, self.rect)
        window.blit(self.text, self.rect)

        click = mouse.get_pressed()
        if click[0]:
            x, y = mouse.get_pos()
            if self.rect.collidepoint(x, y):
                self.handler()



def run_game():
    
    lost = 0
    count = 0
    finish =False
    run = True
    menu = True
    game = False

    def start_game():
        global game, menu, finish
        menu, finish, game = False, False, True

    background = transform.scale(image.load(img_back), (win_width, win_height))
    ship = Player(img_hero, 300, win_height - 150, 80, 100, 10)
    monsters = sprite.Group()
    bullets = sprite.Group()

    for i in range(5):
        rand_x = randint(0, win_width - 100 )
        rand_v = randint(3,8)
        rand_y = randint(50, 300)
        nlo = Enemy("ufo.png", rand_x, rand_y*-1, 80, 50, rand_v)
        monsters.add(nlo)
        
    

    font1 = font.SysFont("Impact", 70)
    font2 = font.SysFont("Impact", 30)
    score = 0
    score_text  = font2.render("Рахунок: " + str(score), True, (255,0,0))
    play_btn  = Button("Почати гру", font2, (255,0,0), start_game, 200, 200)

    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
        if menu:
            window.blit(background, (0, 0))

            play_btn.update()
            display.update()


        if game and not finish:
            window.blit(background, (0, 0))

            ship.update()
            monsters.update()
            bullets.update()
            bullets.draw(window)
            monsters.draw(window)
            ship.reset()

            if sprite.spritecollide(ship, monsters, False):
                finish = True
                lose = font1.render("YOU LOSE!", True, (255,0,0))
                window.blit(lose, (win_width/2 - 100, win_height/2 - 50))

            collides = sprite.groupcollide(bullets, monsters, True, True)
            
            for c in collides:
                score+=1
                score_text  = font2.render("Рахунок: " + str(score), True, (255,0,0))

            if score >= 3:
                finish = True
                lose = font1.render("YOU WIN!", True, (255,0,0))
                window.blit(lose, (win_width/2 - 100, win_height/2 - 50))

            window.blit(score_text, (20, 20))
        
            display.update()
        time.delay(50)

run_game()