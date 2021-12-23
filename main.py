from pygame import *

init()

width = 478
height = 600
size = width, height
screen = display.set_mode(size)
display.set_caption('Fly High')

ARIAL_50 = font.SysFont('britannic bold', 50)


class Menu:
    def __init__(self):
        self.surfaces = []
        self.callbacks = []
        self.current_index = 0

    def append_option(self, option, callback):
        self.surfaces.append(ARIAL_50.render(option, True, '#FFE86E'))
        self.callbacks.append(callback)

    def switch(self, direction):
        self.current_index = max(0, min(self.current_index + direction, len(self.surfaces) - 1))

    def select(self):
        self.callbacks[self.current_index]()

    def draw(self, surf, x, y, padding):
        for i, option in enumerate(self.surfaces):
            rect_o = option.get_rect()
            rect_o.topleft = (x + 70, y + 120 + i * 50)
            if i == self.current_index:
                draw.rect(surf, (239, 130, 13), (list(rect_o)[0], list(rect_o)[1] + 30, list(rect_o)[2], 10))
            surf.blit(option, rect_o)


running = True
menu = Menu()
menu.append_option('Играть', lambda: print('Play'))
menu.append_option('Выход', quit)

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                menu.switch(-1)
            elif e.key == K_s:
                menu.switch(1)
            elif e.key == K_SPACE:
                menu.select()

    bg = image.load("image/main_menu1.bmp")
    screen.blit(bg, (-3, 0))

    menu.draw(screen, 100, 100, 75)
    display.flip()
quit()
