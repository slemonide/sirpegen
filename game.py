import sys
from os import path
import pygame as pg
from settings import *
from sprites import *
from camera import *
from map import *

class Game():
    def __init__(self):
        self.display = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption(WINDOW_TITLE)

    def load(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        assets_folder = path.join(path.dirname(__file__), 'assets')
        self.map = Map(path.join(assets_folder, 'maps/map1.txt'))

        wall_img = pg.image.load(path.join(assets_folder, 'wall.png'))
        player_img = pg.image.load(path.join(assets_folder, 'player.png'))

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row, wall_img)
                elif tile == 'P':
                    self.player = Player(self, col, row, player_img)

        self.camera = Camera(self.map.width_screen, self.map.height_screen)

    def update(self):
        for sprite in self.all_sprites:
            sprite.update(self.dt)

        self.camera.update(self.player)

    def draw(self):
        self.display.fill(BG_COLOR)

        for sprite in self.all_sprites:
            self.display.blit(sprite.image, self.camera.transform(sprite))

        # pg.draw.rect(self.display, (0,255,0), self.player.hit_rect, 1)
        # pg.draw.rect(self.display, (255, 255, 255), self.player.rect, 1)
        pg.display.flip()

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()