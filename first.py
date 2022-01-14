from pygame import *
from os import path
import random

images = path.join(path.dirname(__file__), 'image')

WIDTH = 478
HEIGHT = 600
FPS = 60

init()
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Fly High')
clock = time.Clock()

font_name = font.match_font('britannic bold')


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 45 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_text(surf, text, size, x, y):
    font1 = font.Font(font_name, size)
    text_surface = font1.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 150
    BAR_HEIGHT = 30
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = Rect(x, y, fill, BAR_HEIGHT)
    draw.rect(surf, (0, 255, 0), fill_rect)
    draw.rect(surf, (0, 0, 0), outline_rect, 2)


class Player(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(player_img1, (90, 78))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.health = 100
        self.shoot_delay = 250
        self.last_shot = time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = time.get_ticks()

    def update(self):
        if self.hidden and time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        keystate = key.get_pressed()
        if keystate[K_LEFT]:
            self.speedx = -8
        if keystate[K_RIGHT]:
            self.speedx = 8
        if keystate[K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = time.get_ticks()

        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

    def hide(self):
        self.hidden = True
        self.hide_timer = time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Mob(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey((0, 0, 0))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    def rotate(self):
        now = time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


class Bullet(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        sprite.Sprite.__init__(self)
        self.image = bullet_img1
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(sprite.Sprite):
    def __init__(self, center, size):
        sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Игровая графика
player_img1 = image.load(path.join(images, 'Player3.jpg')).convert()
bullet_img1 = image.load(path.join(images, 'laser1.png')).convert()
player_mini_img = transform.scale(player_img1, (40, 30))
player_mini_img.set_colorkey((0, 0, 0))
meteor_images = []
meteor_list = ['asteroid1.png', 'asteroid2.png', 'asteroid3.png', 'asteroid4.png', 'asteroid5.png']
for img in meteor_list:
    meteor_images.append(image.load(path.join(images, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = image.load(path.join(images, filename)).convert()
    img.set_colorkey((0, 0, 0))
    img_lg = transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = image.load(path.join(images, filename)).convert()
    img.set_colorkey((0, 0, 0))
    explosion_anim['player'].append(img)

all_sprites = sprite.Group()
bullets = sprite.Group()
mobs = sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(10):
    newmob()
score = 0

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
        score += 50 - hit.radius
        ex = Explosion(hit.rect.center, 'lg')
        all_sprites.add(ex)
        newmob()

    hits = sprite.spritecollide(player, mobs, True, sprite.collide_circle)
    for hit in hits:
        player.health -= hit.radius * 2
        ex = Explosion(hit.rect.center, 'sm')
        all_sprites.add(ex)
        newmob()
        if player.health <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.health = 100

    if player.lives == 0 and not death_explosion.alive():
        running = False

    bg = image.load("image/фон1.jpg")
    screen.blit(bg, (-3, 0))
    all_sprites.draw(screen)
    draw_text(screen, 'Score:' + ' ' + str(score), 40, 80, 10)
    draw_shield_bar(screen, 320, 5, player.health)
    draw_lives(screen, WIDTH - 140, 50, player.lives,
               player_mini_img)
    display.flip()

quit()
