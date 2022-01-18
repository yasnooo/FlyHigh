from pygame import *
from os import path
import random


WIDTH = 478
HEIGHT = 600
FPS = 60
time_for_powerup = 5000

init()
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Fly High')
watch = time.Clock()

images = path.join(path.dirname(__file__), 'image')

font1 = font.SysFont('britannic bold', 50)
font2 = font.match_font('britannic bold')


def lives_d(surface, x, y, li, image):
    # отрисовка жизней
    for i in range(li):
        img_rect = img.get_rect()
        img_rect.x = x + 45 * i
        img_rect.y = y
        surface.blit(image, img_rect)


def text_d(surface, t, size, x, y):
    # отрисовка текста
    font1 = font.Font(font2, size)
    text_surface = font1.render(t, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def newmob():
    # новый астероид
    m = Mob()
    sprites.add(m)
    asteroids_sp.add(m)


def health_stripe_d(surface, x, y, pc):
    # отрисовка шкалы xp
    if pc < 0:
        pc = 0
    height = 30
    length = 150
    f = (pc / 100) * length
    outer = Rect(x, y, length, height)
    internal = Rect(x, y, f, height)
    draw.rect(surface, (0, 255, 0), internal)
    draw.rect(surface, (0, 0, 0), outer, 2)


def main_menu():
    # главное меню
    global running
    screen.blit(background1, (-3, 0))
    text_d(screen, 'Удерживайте пробел для выстрелов', 30, WIDTH / 2, 237)
    text_d(screen, 'Нажимайте на стрелочки', 30, WIDTH / 2, 255)
    text_d(screen, 'для движения вправо или влево', 30, WIDTH / 2, 273)
    text_d(screen, 'Нажмите любую клавишу для начала игры', 20, WIDTH / 2, 400)
    display.flip()
    waiting = True
    while waiting:
        watch.tick(FPS)
        for ev in event.get():
            if ev.type == QUIT:
                waiting = False
                running = False
                # quit()
                # running = False
            if ev.type == KEYUP:
                waiting = False


def end_game():
    # меню окончания игры
    global running
    global game_start
    global score
    screen.blit(background, r_back1)
    text_d(screen, 'Game over', 64, WIDTH / 2, HEIGHT / 4)
    text_d(screen, 'Ваш счет:{}'.format(score), 40, 250, 250)
    text_d(screen, 'Нажмите любую клавишу для возвращения в главное меню', 20, WIDTH / 2, 400)
    display.flip()
    waiting = True
    while waiting:
        watch.tick(FPS)
        for ev in event.get():
            if ev.type == QUIT:
                waiting = False
                # quit()
                running = False
            if ev.type == KEYUP:
                game_start = True
                waiting = False


class Menu:
    def __init__(self):
        self.surfaces = []
        self.callbacks = []
        self.current_index = 0

    def append_option(self, option, callback):
        self.surfaces.append(font1.render(option, True, '#FFE86E'))
        self.callbacks.append(callback)

    def switch(self, direction):
        self.current_index = max(0, min(self.current_index + direction, len(self.surfaces) - 1))

    def select(self):
        self.callbacks[self.current_index]()

    def draw(self, surface, x, y, padding):
        for i, option in enumerate(self.surfaces):
            rect_o = option.get_rect()
            rect_o.topleft = (x + 70, y + 120 + i * 50)
            if i == self.current_index:
                draw.rect(surface, (239, 130, 13), (list(rect_o)[0], list(rect_o)[1] + 30, list(rect_o)[2], 10))
            surface.blit(option, rect_o)


class Player(sprite.Sprite):
    # класс игрока
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(player_img1, (90, 78))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.spdx = 0
        self.health = 100
        self.shoot_d = 250
        self.last_shoot = time.get_ticks()
        self.lives = 3
        # переменная для того, чтобы "спрятать" корабль после смерти
        self.hid = False
        self.hide_time = time.get_ticks()
        # переменная для того, чтобы повышать силу, когда игрок ловит улучшение
        self.force = 1
        self.force_time = time.get_ticks()

    def update(self):
        if self.force >= 2 and time.get_ticks() - self.force_time > time_for_powerup:
            self.force -= 1
            self.force_time = time.get_ticks()

        if self.hid and time.get_ticks() - self.hide_time > 1000:
            self.hid = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.spdx = 0
        keystate = key.get_pressed()
        if keystate[K_LEFT]:
            self.spdx = -8
        if keystate[K_RIGHT]:
            self.spdx = 8
        if keystate[K_SPACE]:
            self.shoot()
        self.rect.x += self.spdx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def power_rais(self):
        # повышение силы, когда игрок ловит улучшение
        self.force += 1
        self.force_time = time.get_ticks()

    def shoot(self):
        # выстрел
        now = time.get_ticks()

        if now - self.last_shoot > self.shoot_d:
            self.last_shoot = now

            if self.force == 1:
                bull = Bullet(self.rect.centerx, self.rect.top)
                sprites.add(bull)
                lasers.add(bull)

            if self.force >= 2:
                bull1 = Bullet(self.rect.left, self.rect.centery)
                bull2 = Bullet(self.rect.right, self.rect.centery)
                sprites.add(bull1)
                sprites.add(bull2)
                lasers.add(bull1)
                lasers.add(bull2)

    def hide(self):
        # скрытие игрока после смерти
        self.hid = True
        self.hide_time = time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Mob(sprite.Sprite):
    # класс астероидов
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image_orig = random.choice(asteroid_img)
        self.image_orig.set_colorkey((0, 0, 0))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .75 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.spdy = random.randrange(1, 20)
        self.spdx = random.randrange(-6, 6)
        self.rotation = 0
        self.rotation_spd = random.randrange(-7, 7)
        self.last_upd = time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.x += self.spdx
        self.rect.y += self.spdy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.spdy = random.randrange(1, 8)

    def rotate(self):
        # поворот атероидов
        now = time.get_ticks()
        if now - self.last_upd > 50:
            self.last_upd = now
            self.rotation = (self.rotation + self.rotation_spd) % 360
            new_img = transform.rotate(self.image_orig, self.rotation)
            old = self.rect.center
            self.image = new_img
            self.rect = self.image.get_rect()
            self.rect.center = old


class Bullet(sprite.Sprite):
    # класс лазера
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        sprite.Sprite.__init__(self)
        self.image = bullet_img1
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.spd = -10

    def update(self):
        self.rect.y += self.spd
        if self.rect.bottom < 0:
            self.kill()


class Explosion(sprite.Sprite):
    # класс анимации взрыва
    def __init__(self, center, size):
        sprite.Sprite.__init__(self)
        self.size = size
        self.image = animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.fr = 0
        self.last_upd = time.get_ticks()
        self.fr_rate = 50

    def update(self):
        now = time.get_ticks()
        if now - self.last_upd > self.fr_rate:
            self.last_upd = now
            self.fr += 1
            if self.fr == len(animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = animation[self.size][self.fr]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Improve(sprite.Sprite):
    # класс улучшений
    def __init__(self, cen):
        sprite.Sprite.__init__(self)
        self.improve = random.choice(['health', 'weapon'])
        self.image = power_rais_img[self.improve]
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = cen
        self.spdy = 2

    def update(self):
        self.rect.y += self.spdy
        if self.rect.top > HEIGHT:
            self.kill()


# Игровая графика
background1 = image.load(path.join(images, 'main_menu1.bmp')).convert()
r_back = background1.get_rect()
background = image.load(path.join(images, 'фон1.jpg')).convert()
r_back1 = background.get_rect()
player_img1 = image.load(path.join(images, 'Player3.jpg')).convert()
bullet_img1 = image.load(path.join(images, 'laser1.png')).convert()
# маленькие кораблики для отображения жизней
mini_img = transform.scale(player_img1, (40, 30))
mini_img.set_colorkey((0, 0, 0))
power_rais_img = {}
power_rais_img['health'] = image.load(path.join(images, 'health.png')).convert()
power_rais_img['weapon'] = image.load(path.join(images, 'weapon.png')).convert()
asteroid_img = []
asteroids = ['asteroid1.png', 'asteroid2.png', 'asteroid3.png', 'asteroid4.png', 'asteroid5.png']
for img in asteroids:
    asteroid_img.append(image.load(path.join(images, img)).convert())

animation = {}
animation['kl'] = []
animation['po'] = []
animation['player'] = []

for i in range(8):
    filename = f'ordinary0{i}.png'
    img = image.load(path.join(images, filename)).convert()
    img.set_colorkey((0, 0, 0))
    img_lg = transform.scale(img, (75, 75))
    animation['po'].append(img_lg)
    img_sm = transform.scale(img, (32, 32))
    animation['kl'].append(img_sm)

for i in range(9):
    filename = f'other0{i}.png'
    img = image.load(path.join(images, filename)).convert()
    img.set_colorkey((0, 0, 0))
    animation['player'].append(img)

power_rais_img = {}
power_rais_img['health'] = image.load(path.join(images, 'health.png')).convert()
power_rais_img['weapon'] = image.load(path.join(images, 'weapon.png')).convert()


power_rais = sprite.Group()

sprites = sprite.Group()
lasers = sprite.Group()
asteroids_sp = sprite.Group()
player = Player()
sprites.add(player)
score = 0
for i in range(20):
    newmob()

game_start = True
game_over = False
running = True
while running:
    if game_start:
        main_menu()
        game_start = False
        sprites = sprite.Group()
        asteroids_sp = sprite.Group()
        lasers = sprite.Group()
        power_rais = sprite.Group()
        player = Player()
        sprites.add(player)
        for i in range(8):
            newmob()
        score = 0

    if game_over:
        end_game()
        game_over = False
        sprites = sprite.Group()
        asteroids_sp = sprite.Group()
        lasers = sprite.Group()
        power_rais = sprite.Group()
        player = Player()
        sprites.add(player)
        for i in range(20):
            newmob()
        score = 0

    watch.tick(FPS)
    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.shoot()

    sprites.update()

    hit_m = sprite.groupcollide(asteroids_sp, lasers, True, True)
    for hit in hit_m:
        score += 70 - hit.radius
        explosion = Explosion(hit.rect.center, 'po')
        sprites.add(explosion)
        if random.random() > 0.87:
            impr = Improve(hit.rect.center)
            sprites.add(impr)
            power_rais.add(impr)
        newmob()

    hit_m2 = sprite.spritecollide(player, asteroids_sp, True, sprite.collide_circle)
    for hit in hit_m2:
        player.health -= hit.radius * 4
        explosion = Explosion(hit.rect.center, 'kl')
        sprites.add(explosion)
        newmob()
        if player.health <= 0:
            d_ex = Explosion(player.rect.center, 'player')
            sprites.add(d_ex)
            player.hide()
            player.lives -= 1
            player.health = 100

    hit_m3 = sprite.spritecollide(player, power_rais, True)
    for hit in hit_m3:
        if hit.improve == 'health':
            player.health += random.randrange(5, 20)
            if player.health >= 100:
                player.health = 100
        if hit.improve == 'weapon':
            player.power_rais()

    if player.lives == 0 and not d_ex.alive():
        game_over = True

    bg = image.load("image/фон1.jpg")
    screen.blit(bg, (-3, 0))
    sprites.draw(screen)
    text_d(screen, 'Score:' + ' ' + str(score), 40, 80, 10)
    health_stripe_d(screen, 320, 5, player.health)
    lives_d(screen, WIDTH - 140, 50, player.lives,
            mini_img)
    display.flip()

quit()
