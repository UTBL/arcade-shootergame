from pygame import *
from random import *
lost = 0
count = 0
num_fire = 0
live = 3
window = display.set_mode((700,500))
display.set_caption("galaxy")
background = transform.scale(image.load("galaxy.jpg"), (700,500))
window.blit(background,(0, 0))
sprite1 = transform.scale(image.load("asteroid.png"),(100,100))
window.blit(sprite1, (100, 100))
sprite2 = transform.scale(image.load("ufo.png"),(100,100))
window.blit(sprite2, (200, 200))
sprite3 = transform.scale(image.load("bullet.png"),(10,15))
window.blit(sprite3, (200, 400))
sprite4 = transform.scale(image.load("rocket.png"),(100,100))
window.blit(sprite4, (400, 200))

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed,x,y):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(x,y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self,player_image,player_x,player_y,player_speed):
        super().__init__(player_image,player_x,player_y,player_speed,65,65)
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
        if keys_pressed[K_SPACE]:
            self.fire()
    def fire(self):
        bullet1 = Bullet('bullet.png',self.rect.centerx,self.rect.top,6)
        bullets.add(bullet1)
    def reload(self):
        if keys_pressed[K_SPACE]:
            num_fire = num_fire + 1
                        
class Enemy(GameSprite):
    def __init__(self,player_image,player_x,player_y,player_speed):
        super().__init__(player_image,player_x,player_y,player_speed,65,65)
    def update(self): 
        global lost
        if self.rect.y >= 5:
            self.rect.y += self.speed
        if self.rect.y >= 490:
            self.rect.y = 5
            self.rect.x = randint(100,590)
            self.speed = randint(1,3)
            lost = lost + 1
class Asteroids(GameSprite):
    def __init__(self,player_image,player_x,player_y,player_speed):
        super().__init__(player_image,player_x,player_y,player_speed,75,85)
    def update(self):
        if self.rect.y >= 5:
            self.rect.y += self.speed
        if self.rect.y >= 490:
            self.rect.y = 5
            self.rect.x = randint(100,590)
            self.speed = randint(1,3)
class Bullet(GameSprite):
    def __init__(self,player_image,player_x,player_y,player_speed):
        super().__init__(player_image,player_x,player_y,player_speed,15,20)
    def update(self): 
        if self.rect.y > 0:
            self.rect.y -= self.speed
        else:
            self.kill()

e1 = Enemy('ufo.png',randint(100,550),10,randint(1,2))
e2 = Enemy('ufo.png',randint(100,550),10,randint(1,2))
e3 = Enemy('ufo.png',randint(100,550),10,randint(1,2))
e4 = Enemy('ufo.png',randint(100,550),10,randint(1,2))
e5 = Enemy('ufo.png',randint(100,550),10,randint(1,2))
monsters = sprite.Group()
monsters.add(e1,e2,e3,e4,e5)
bullets = sprite.Group()
d1 = Asteroids('asteroid.png',randint(100,550),10,randint(1,2))
d2 = Asteroids('asteroid.png',randint(100,550),10,randint(1,2))
d3 = Asteroids('asteroid.png',randint(100,550),10,randint(1,2))
asteroids = sprite.Group()
asteroids.add(d1,d2,d3)

clock = time.Clock()
FPS = 120
clock.tick(FPS)
mixer.init()
fire = mixer.Sound('fire.ogg')
mixer.music.load('space.ogg')
mixer.music.play()
font.init()
font2 = font.SysFont("Arial",36)
font1 = font.SysFont("Arial",36)
font3 = font.SysFont("Arial",76)
font4 = font.SysFont("Arial",76)
game = True
finish = False
rocket = Player('rocket.png',100,430,10)
while game:
    if finish != True:
        text_lose = font2.render("Пропущено: " + str(lost), 1 ,(255,255,255))
        text_count = font1.render("Счет: " + str(count), 1 ,(255,255,255))
        text_win = font3.render("YOU WIN!", 1,(255,0,0))
        text_lost = font4.render("YOU LOSE!", 1,(255,0,0))
        rocket.update()
        window.blit(background,(0, 0))
        window.blit(text_lose,(10,50))
        window.blit(text_count,(10,20))
        window.blit(rocket.image, (rocket.rect.x, rocket.rect.y))
        window.blit(rocket.image, (rocket.rect.x, rocket.rect.y))
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        sprite_list = sprite.spritecollide(rocket,monsters, False)
        sprite_list1 = sprite.groupcollide(monsters,bullets, True,True)
        sprite_list2 = sprite.spritecollide(rocket,asteroids, False)
        if live <= 0:
            finish = True
            window.blit(text_lost,(250,250))
        for i in sprite_list1:
            count = count + 1
            b1 = Enemy('ufo.png',randint(100,550),10,randint(1,2))
            monsters.add(b1)
        if count >= 35:
            finish = True
            window.blit(text_win,(250,250))
            break
        if lost >= 10:
            finish = True
            window.blit(text_lost,(250,250))
            break
        for i in event.get():
            if i.type == QUIT:
                game = False
    display.update()