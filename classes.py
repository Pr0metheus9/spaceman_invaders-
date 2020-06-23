import pygame

pygame.mixer.init()

WIDTH = 500
HEIGHT = 500
p_img = pygame.image.load("res/player.png")
e_img = pygame.image.load("res/enemy.png")
eb_img = pygame.image.load("res/blimp.png")
mars_img = pygame.image.load("res/mars.png")
e_nobox = pygame.image.load("res/enemy_nobox.png")
icon = pygame.image.load("res/logo.png")
menu = pygame.image.load('res/menu.png')
start = pygame.image.load("res/start.png")
options = pygame.image.load("res/options.png")
exit = pygame.image.load("res/exit.png")

music = pygame.mixer.Sound("res/menu_music.wav")
laser = pygame.image.load("res/laser.png")
rocket = pygame.image.load("res/rocket.png")
box = pygame.image.load("res/box.png")
chip = pygame.image.load("res/chip.png")
bubble = pygame.image.load("res/bubble.png")
explosion_anim = [rocket, pygame.image.load("res/explode.png")]
drone_exl_anim = [laser,pygame.image.load("res/exl_drone.png")]
laser_shot = pygame.mixer.Sound("res/shot.wav")
explosion_sfx = pygame.mixer.Sound("res/Explosion.wav")
explosion_sfx.set_volume(0.02)
laser_shot.set_volume(0.04)

class OBJ:
    def __init__(self, x, y, img, v):
        self.x = x
        self.y = y
        self.img = img
        self.v = v
        self.rect = img.get_rect()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.birth = pygame.time.get_ticks()
        self.hitbox = (self.x - 67, self.y - 85, 35, 60)  # default is for the car: x,y,width,height

    def draw(self, window, ):
        self.rect.center = self.x - 0.5 * self.width, self.y - 0.5 * self.height
        #self.hitbox = (self.x-67, self.y-85, 35,60)
        #pygame.draw.rect(window, (0,0,255), self.hitbox, 2) #use for hitbox testing!
        window.blit(self.img, self.rect)


# Player Class
class Player(OBJ):
    def __init__(self, x, y, img, v):
        super().__init__(x, y, img, v)
        self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()
        self.hitbox = (self.x-72, self.y-89, 40,63)
        self.coin = 0
        self.lives = 3
        self.respawn = False

    def move(self, key):
        if key[pygame.K_LEFT] and self.x > 105:
            self.x -= self.v

        if key[pygame.K_RIGHT] and self.x < WIDTH - 100:
            self.x += self.v

        if key[pygame.K_UP] and self.y > 105:
            self.y -= self.v

        if key[pygame.K_DOWN] and self.y < HEIGHT - 5:
            self.y += self.v

        self.hitbox = (self.x-72, self.y-89, 40,63)

    def shoot(self, shots, key):
        if key[pygame.K_SPACE] and pygame.time.get_ticks() - self.last_shot > self.shoot_delay:
            shots.append(Projectile(round(self.x), round(self.y - self.height / 2 + 10), laser, 9, "laser"))
            pygame.mixer.Sound.play(laser_shot)
            self.last_shot = pygame.time.get_ticks()

        if key[pygame.K_RSHIFT] and pygame.time.get_ticks() - self.last_shot > self.shoot_delay:
            shots.append(Projectile(round(self.x + 50), round(self.y - self.height / 2 + 10), rocket, 9, "rocket"))
            self.last_shot = pygame.time.get_ticks()

    def check_col(self, objects):
        for obj in objects:
            if (self.hitbox[0] + self.hitbox[2] >= obj.hitbox[0] and self.hitbox[0] <= obj.hitbox[0] + obj.hitbox[2]
                    and self.hitbox[1] + self.hitbox[3] >= obj.hitbox[1] and self.hitbox[1] <= obj.hitbox[1] +
                    obj.hitbox[3]):
                return [True, obj]


class Enemy(OBJ):
    def __init__(self, x, y, img, v):
        super().__init__(x, y, img, v)
        self.right = True
        self.shot = False
        self.hitbox = (self.x - 67, self.y - 85, 30, 40)
        self.hp = 100

    def move(self):
        self.y += self.v
        self.hitbox = (self.x - 77, self.y - 75, 50, 30)

    def check_col(self, shots):
        for shot in shots:
            if (self.hitbox[0] + self.hitbox[2] >= shot.hitbox[0] and self.hitbox[0] <= shot.hitbox[0] + shot.hitbox[2]
                    and self.hitbox[1] + self.hitbox[3] >= shot.hitbox[1] and self.hitbox[1] <= shot.hitbox[1] +
                    shot.hitbox[3]):
                return [True, shot]

    def shoot(self, boxes):
        boxes.append(Projectile(round(self.x), round(self.y), box, self.v + 2, "box"))
        self.shot = True


# Projectile Class
class Projectile(OBJ):
    def __init__(self, x, y, img, v, type):
        super().__init__(x, y, img, v)
        self.right = True
        self.shot = False
        self.type = type

    def move(self, projectiles):
        if self.x < WIDTH and self.x > 5:
            if self.type == "laser":
                self.y -= self.v
                self.hitbox = (self.x - 67, self.y - 85, 20, 40)

            elif self.type == "rocket":
                self.y -= self.v
                self.hitbox = (self.x - 113, self.y - 195, 20, 190)

            else:
                self.y += self.v
                self.hitbox = (self.x - 66, self.y - 65, 25, 20)
        else:
            projectiles.pop(projectiles.index(self))


class Anim(pygame.sprite.Sprite):
    def __init__(self, center, explosion_anim):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100

    def update(self, animations):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                animations.remove(self)
                self.kill()
            elif (self.frame < len(explosion_anim)):
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

    def draw(self, window, ):
        window.blit(self.image, self.rect)

class Star:
    def __init__(self, x, y, velocity, color,radius):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.color = color
        self.radius = radius

    def draw(self, window):
        pygame.draw.circle(window, self.color,(self.x, self.y), self.radius)


class Collectable (OBJ):
    def __init__(self, x, y, img, type):
        super().__init__(x, y, img, 0)
        self.type = type
        if(self.type == "coin"):
            self.hitbox = (self.x - 75, self.y - 80, 50, 44)
