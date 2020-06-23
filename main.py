from classes import *
import random

WIDTH = 500
HEIGHT = 500
SCORE = 0
PART = "menu"

pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Starman Invaders")

pygame.display.set_icon(icon)

clock = pygame.time.Clock()

player = Player(WIDTH / 2, HEIGHT / 2, p_img, 12)

run = True
shots = []
aliens = []
explosions = []
boxes = []
star_slow = []
star_med = []
star_fast = []
btn = []
coins = []
last_spawn = pygame.time.get_ticks()
prev_tick = pygame.time.get_ticks()
bbl = None

#make stars
for i in range(15):  # fast stars
    star_fast.append(Star(random.randrange(0, WIDTH), random.randrange(0, HEIGHT),4,  (255,255,255), 1))
for i in range(35): #medium stars
    star_med.append(Star(random.randrange(0, WIDTH), random.randrange(0, HEIGHT), 3,  (255,255,255), 2))
for i in range(35): #small stars
    star_slow.append(Star(random.randrange(0, WIDTH), random.randrange(0, HEIGHT), 2, (255,255,255), 3))

#make score font
font = pygame.font.Font("res/arcfont.ttf", 25)

def event_check():
    global PART
    global run
    start = pygame.Rect((215, 262),(65, 15))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP and PART == "menu":
            x, y = event.pos
            #print(x,y)
            if start.collidepoint(x, y):
                PART = "game_mode"
                pygame.mixer.stop()
                game_music = pygame.mixer.Sound("res/music_a.wav")
                pygame.mixer.Sound.set_volume(game_music,0.03)
                pygame.mixer.Sound.play(game_music, -1)

def menu_draw(win,btn):
        win.blit(menu, menu.get_rect())
        #pygame.draw.rect(win,(0,255,0),(215, 262, 65, 15),2) start button hitbox
        btn.append(win.blit(start, (155, 200)))
        btn.append(win.blit(options, (170, 225)))
        btn.append(win.blit(exit, (160, 250)))

def update_obj():
    global last_spawn
    global SCORE
    global prev_tick

    for star in star_slow:
        star.y += star.velocity
        if star.y > HEIGHT:
            star.x = random.randrange(0, WIDTH)
            star.y = random.randrange(-20, -5)

    for star in star_med:
        star.y += star.velocity
        if star.y > HEIGHT:
            star.x = random.randrange(0, WIDTH)
            star.y = random.randrange(-20, -5)

    for star in star_fast:
        star.y += star.velocity
        if star.y > HEIGHT:
            star.x = random.randrange(0, WIDTH)
            star.y = random.randrange(-20, -5)

    if ((pygame.time.get_ticks() - last_spawn) >= 3000):
        aliens.append(Enemy(random.randrange(105, WIDTH - 100), 20, e_img, 3))
        last_spawn = pygame.time.get_ticks()

    for shot in shots:
        shot.move(shots)

    for box in boxes:
        box.move(boxes)

    for enemy in aliens:
        if (enemy.shot == False and pygame.time.get_ticks() - enemy.birth > 250):
            enemy.shoot(boxes)
            enemy.img = e_nobox
            pass

        # check if collided with player shot
        col_status = enemy.check_col(shots)
        if col_status != None and col_status[0]:
            if (col_status[1].img == rocket):
                explosions.append(Anim(col_status[1].rect.center,explosion_anim))
                pygame.mixer.Sound.play(explosion_sfx)

            if (col_status[1].img == laser):
                explosions.append(Anim(col_status[1].rect.center, drone_exl_anim))
                pygame.mixer.Sound.play(explosion_sfx)

            coins.append(Collectable(enemy.x, enemy.y, chip, "coin"))
            aliens.remove(enemy)
            shots.remove(col_status[1])
            SCORE += 100
        enemy.move()

    col_status = player.check_col(coins)
    if col_status != None and col_status[0]:
        coins.remove(col_status[1])
        player.coin += 1

    col_status = player.check_col(boxes)
    if col_status != None and col_status[0] and pygame.time.get_ticks() - prev_tick > 1000:
        player.lives = player.lives - 1
        prev_tick =  pygame.time.get_ticks()
        player.respawn = True

    if player.lives == 0:
        exit()

    for coin in coins:
        if(pygame.time.get_ticks() - coin.birth >= 2500):
            coins.remove(coin)

    for expl in explosions:
        expl.update(explosions)

    player.check_col(boxes)

    key = pygame.key.get_pressed()

    player.move(key)
    player.shoot(shots, key)

def draw():
    #draw background
    win.fill((0,0,0))
    for star in star_fast:
        star.draw(win)
    for star in star_med:
        star.draw(win)
    for star in star_slow:
        star.draw(win)
    win.blit(mars_img,(53,80))
    score = font.render('Score: ' + str(SCORE), 3, (255, 255, 255))
    coin_text = font.render('Coins: ' + str(player.coin), 3, (255,255,255))
    life_txt = font.render('Lives: ' + str(player.lives), 3, (255, 255, 255))
    bbl = None
    win.blit(score, (0, 0))
    win.blit(coin_text, (0,30))
    win.blit(life_txt, (0,60))
    #draw game images
    for enemy in aliens:
        enemy.draw(win)
    for coin in coins:
        coin.draw(win)
    for shot in shots:
        shot.draw(win)
    for box in boxes:
        box.draw(win)
    for expl in explosions:
        expl.draw(win)
    if player.respawn == True:
        bbl = OBJ(player.x + 90,player.y + 100,bubble,0)
        player.respawn = False

    player.draw(win)

    if bbl != None:
        bbl.draw(win)


pygame.mixer.Sound.set_volume(music,0.01)
pygame.mixer.Sound.play(music,-1)

while (run):
    pygame.time.delay(40)

    event_check()

    if(PART == "menu"):
        menu_draw(win,btn)

    else:
        update_obj()

        draw()

    pygame.display.flip()
    pygame.display.update()

    clock.tick(60)
