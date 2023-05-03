from pygame import *
from random import *
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
img_bullet = 'bullet.png'

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))
font2 = font.Font(None, 36)

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'

win_widht = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_widht, win_height))
background = transform.scale(image.load(img_back), (win_widht, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.centerx-25, self.rect.top))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x< win_widht - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_widht - 80)
            self.rect.y = 0
            lost= lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_widht - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

score = 0
lost = 0
max_lost = 3
goal = 10
num_fire = 0 

ship = Player(img_hero,5, win_height - 80,65,65,10)

finish = False
run = True

rel_time = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1 
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

                
    
    if not finish:
        window.blit(background, (0,0))

        text = font2.render('Счет:' + str(score), 1, (255,255, 255))
        window.blit(text, (10,20))

        text_lose = font2.render('Пропущено:' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))
    
        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()

        ship.reset()
        ship.update()

        if rel_time == True:
                now_time = timer()
                if now_time - last_time <3:
                    reload = font2.render('Wait, reload..', 1, (150,0,0))
                    window.blit(reload, (260,460))
                else:
                    num_fire = 0
                    rel_time = False   

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for i in collides:
            score = score +1
            monster = Enemy(img_enemy, randint(80, win_widht - 80), -40,80,50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))
        if score == goal:
            finish = True
            window.blit(win, (200,200))
        display.update()
    time.delay(50)