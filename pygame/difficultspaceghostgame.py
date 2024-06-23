import pygame as pg, sys
import random

pg.init()
screen = pg.display.set_mode((800, 600))


##　ゲームクリア画面
img4=pg.image.load("images/root4.png")
img5=pg.image.load("images/root5.png")


## プレイヤーデータ
myimgR = pg.image.load("images/playerR.png")
myimgR = pg.transform.scale(myimgR, (40, 50))
myimgL = pg.transform.flip(myimgR, True, False)
myrect = pg.Rect(0, 500, 40, 50)

## UFOデータ
ufoimg = pg.image.load("images/UFO.png")
ufoimg = pg.transform.scale(ufoimg, (50, 50))
ufos = []
for i in range(10):
    ux = random.randint(0, 800)
    uy = -100 * i
    ufos.append(pg.Rect(ux, uy, 50, 50))

## 星データ
starimg = pg.image.load("images/star.png")
starimg = pg.transform.scale(starimg, (12, 12))
stars = []
for i in range(60):
    star = pg.Rect(random.randint(0, 800), 10 * i, 30, 30)
    star.w = random.randint(5, 8)
    stars.append(star)

## ボタンデータ
replay_img = pg.image.load("images/replaybtn.png")
goalrect = pg.Rect(750, 250, 30, 100)

## オバケデータ
enemyimgR = pg.image.load("images/obake.png")
enemyimgR = pg.transform.scale(enemyimgR, (50, 50))
enemyimgL = pg.transform.flip(enemyimgR, True, False)
enemyrect = pg.Rect(650, 200, 50, 50)

## 弾データ
bulletimg = pg.image.load("images/bullet.png")
bulletimg = pg.transform.scale(bulletimg, (16, 16))
bullets = []

## メインループで使う変数
rightFlag = True

page = 1
score = 0

## btnを押したら、newpageにジャンプする
def button_to_jump(btn, newpage):
    global page, pushFlag
    # 4.ユーザーからの入力を調べる
    mdown = pg.mouse.get_pressed()
    (mx, my) = pg.mouse.get_pos()
    if mdown[0]:
        if btn.collidepoint(mx, my) and pushFlag == False:
            pg.mixer.Sound("sounds/pi.wav").play()
            page = newpage
            pushFlag = True
    else:
        pushFlag = False

## ゲームステージ
def gamestage():
    global score
    global rightFlag
    global page
    global bullets
    
    screen.fill(pg.Color("DEEPSKYBLUE"))
    vx = 0
    vy = 0
    
    # 4.ユーザーからの入力を調べる
    key = pg.key.get_pressed()
    
    # 5.絵を描いたり、判定したりする
    if key[pg.K_RIGHT]:
        vx = 4
        rightFlag = True
    if key[pg.K_LEFT]:
        vx = -4
        rightFlag = False
    if key[pg.K_UP]:
        vy = -4
    if key[pg.K_DOWN]:
        vy = 4
    if key[pg.K_SPACE]:
        bullet_x = myrect.x + myrect.width // 2 - 8
        bullet_y = myrect.y + myrect.height // 2 - 8
        if rightFlag:
            bullet_vx = 10
        else:
            bullet_vx = -10
        bullets.append({"rect": pg.Rect(bullet_x, bullet_y, 16, 16), "vx": bullet_vx})
        pg.mixer.Sound("sounds/piko.wav").play()

    ## 星の処理
    for star in stars:
        star.y += star.w
        screen.blit(starimg, star)
        if star.y > 600:
            star.x = random.randint(0, 800)
            star.y = 0

    ## プレイヤーの処理
    myrect.x += vx
    myrect.y += vy
    
    if rightFlag:
        screen.blit(myimgR, myrect)
    else:
        screen.blit(myimgL, myrect)

    ## ゴールの処理
    pg.draw.rect(screen, pg.Color("GOLD"), goalrect)
    if myrect.colliderect(goalrect):
        pg.mixer.Sound("sounds/up.wav").play()
        page = 3

    ## オバケの処理
    ovx = 0
    ovy = 0
    if enemyrect.x < myrect.x:
        ovx = 1
    else:
        ovx = -1
    if enemyrect.y < myrect.y:
        ovy = 1
    else:
        ovy = -1
    enemyrect.x += ovx
    enemyrect.y += ovy
    if ovx > 0:
        screen.blit(enemyimgR, enemyrect)
    else:
        screen.blit(enemyimgL, enemyrect)
    if myrect.colliderect(enemyrect):
        pg.mixer.Sound("sounds/down.wav").play()
        page = 2

    ## UFOの処理
    for ufo in ufos:
        ufo.y += 10
        screen.blit(ufoimg, ufo)
        if ufo.y > 600:
            ufo.x = random.randint(0, 800)
            ufo.y = -100
        ## プレイヤーとUFOの衝突処理
        if ufo.colliderect(myrect):
            page = 2
            pg.mixer.Sound("sounds/down.wav").play()

    ## 弾の処理
    for bullet in bullets[:]:
        bullet["rect"].x += bullet["vx"]
        screen.blit(bulletimg, bullet["rect"])
        if bullet["rect"].x < 0 or bullet["rect"].x > 800:
            bullets.remove(bullet)
        ## 弾とUFOの衝突処理
        for ufo in ufos:
            if ufo.colliderect(bullet["rect"]):
                score += 1000
                ufo.y = -100
                ufo.x = random.randint(0, 800)
                if bullet in bullets:
                    bullets.remove(bullet)
                pg.mixer.Sound("sounds/piko.wav").play()

    ## スコアの処理
    font = pg.font.Font(None, 40)
    text = font.render("SCORE:" + str(score), True, pg.Color("WHITE"))
    screen.blit(text, (20, 20))

## データのリセット
def gamereset():
    global score
    score = 0
    myrect.x = 0
    myrect.y = 500
    enemyrect.x = 650
    enemyrect.y = 200
    for i in range(8):
        ufos[i] = pg.Rect(random.randint(0, 800), -100 * i, 50, 50)


## ゲームオーバー
def gameover():
    screen.fill(pg.Color("NAVY"))
    font = pg.font.Font(None, 150)
    text = font.render("GAMEOVER", True, pg.Color("RED"))
    screen.blit(text, (100, 200))
    btn1 = screen.blit(replay_img, (320, 480))
    font = pg.font.Font(None, 40)
    text = font.render("SCORE:" + str(score), True, pg.Color("WHITE"))
    screen.blit(text, (20, 20))
    button_to_jump(btn1, 1)
    if page==1:
        gamereset()

## ゲームクリア
def gameclear():
    if score==0:
        screen.blit(img4,(0,0))
        btn1 = screen.blit(replay_img, (320, 560))
        font = pg.font.Font(None, 40)
        text = font.render("SCORE:" + str(score), True, pg.Color("WHITE"))
        screen.blit(text, (20, 20))
        button_to_jump(btn1, 1)
        if page==1:
            gamereset()      
    else:     
        screen.blit(img5,(0,0))
        btn1 = screen.blit(replay_img, (320, 560))
        font = pg.font.Font(None, 40)
        text = font.render("SCORE:" + str(score), True, pg.Color("WHITE"))
        screen.blit(text, (20, 20))
        button_to_jump(btn1, 1)
        if page==1:
            gamereset()
        
## メインループ
while True:
    if page == 1:
        gamestage()
    elif page == 2:
        gameover()
    elif page == 3:
        gameclear()
    pg.display.update()
    pg.time.Clock().tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
