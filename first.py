from pygame import *
import random

WIDTH = 478
HEIGHT = 600
FPS = 60

init()
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Fly High')
clock = time.Clock()


class Player(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = Surface((50, 40))
        self.image.fill((200, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = key.get_pressed()
        if keystate[K_LEFT]:
            self.speedx = -8
        if keystate[K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = Surface((30, 40))
        self.image.fill((0, 100, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((10, 20))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


all_sprites = sprite.Group()
bullets = sprite.Group()
mobs = sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(10):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

running = True
while running:
    clock.tick(FPS)
    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.shoot()

    all_sprites.update()
    hits = sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    hits = sprite.spritecollide(player, mobs, False)
    if hits:
        running = False
    bg = image.load("image/фон1.jpg")
    screen.blit(bg, (-3, 0))
    all_sprites.draw(screen)
    display.flip()

quit()
