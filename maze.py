from pygame import *


class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale( image.load(player_image), (50,50))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        windown.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)

    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < 450:
            self.rect.y += self.speed
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 650:
            self.rect.x += self.speed

class Enemy(GameSprite):

    def __init__(self, player_image, player_x, player_y, player_speed, direction):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.direction = "left"
        
    def update(self):

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        
        if self.rect.x >= 620:
            self.direction = "left"

        if self.rect.x <= 520:
            self.direction = "right"


class Wall(sprite.Sprite):

    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_widht, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.widht = wall_widht
        self.height = wall_height
        self.image = Surface((self.widht, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def reset(self):
        windown.blit(self.image, (self.rect.x, self.rect.y))


h = 700
w = 500

windown = display.set_mode((h, w))
display.set_caption("МегаЛабиринт 2к23")
background = transform.scale( image.load("background.jpg"), (h, w))

sprite1 = Player(("hero.png"), 0, 420, 10)
sprite2 = Enemy(("cyborg.png"), 620, 310, 2, "left")
sprite3 = GameSprite(("treasure.png"), 640, 420, 0)

wall1 = Wall(13, 54, 25, 100, 90, 15, 500)
wall2 = Wall(13, 54, 25, 200, 0, 15, 400)
wall3 = Wall(13, 54, 25, 200, 400, 200, 15)
wall4 = Wall(13, 54, 25, 385, 0, 15, 400)
wall5 = Wall(13, 54, 25, 500, 90, 15, 500)


mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play()

kick = mixer.Sound("kick.ogg")
money = mixer.Sound("money.ogg")

font.init()
font = font.SysFont("Arial", 70)
fail = font.render("YOU LOSE!", True, (255, 215, 10))

win = font.render("YOU WIN!", True, (255, 215, 10))

clock = time.Clock()
FPS = 60

game = True
finish = False

while game:

    clock.tick(FPS)

    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:

        windown.blit(background, (0, 0))

        sprite1.reset()
        sprite2.reset()
        sprite3.reset()

        sprite1.update()
        sprite2.update()

        wall1.reset()
        wall2.reset()
        wall3.reset()
        wall4.reset()
        wall5.reset()

        if sprite.collide_rect(sprite1, sprite2) or sprite.collide_rect(sprite1, wall1) or sprite.collide_rect(sprite1, wall2) or sprite.collide_rect(sprite1, wall3) or sprite.collide_rect(sprite1, wall4) or sprite.collide_rect(sprite1, wall5):
            windown.blit(fail, (200, 200))
            finish = True
            kick.play()

        if sprite.collide_rect(sprite1, sprite3):
            windown.blit(win, (200, 200))
            finish = True
            money.play()

    display.update()