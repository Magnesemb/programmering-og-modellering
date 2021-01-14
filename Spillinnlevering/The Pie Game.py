import pygame
import time
import random

pygame.init() #starter pygame

crashed = False
helpscreen = False

#skjerm
width = 1050
height = 600
skjerm = pygame.display.set_mode((width,height)) #størrelse på skjerm
pygame.display.set_caption("The Pie Game")

#lyd
pygame.mixer.music.load("Itty-Bitty-8-Bit-Kevin-MacLeod.wav")
sound_splat = pygame.mixer.Sound("Stones-and-Water-On-Cement.wav")
sound_bonus = pygame.mixer.Sound("Wood-Plank-Flicks.wav")

#klokke
klokke = pygame.time.Clock()

#highscore (utenfor loop så den ikke resettes hver gang)
highscore = 0

#Farger (RGB)
BLUE = (0,0,255)
DARK_BLUE = (0,0,200)
SCREEN_BLUE = (67,165,211)
RED = (255,0,0)
DARK_RED = (200,0,0)
GREEN = (0,255,0)
BRIGHT_YELLOW = (255,255,0)
YELLOW = (200,200,0)
DARK_YELLOW = (150,150,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (150,150,150)

#legger inn "karakteren"
pieImg = pygame.image.load("pie_main.png")
pie_width = 140

#funksjoner

def info(info_name,info_count,info_y):   #viser hvor langt spilleren har kommet på skjermen
    font = pygame.font.Font("ScreamWhenYoureReadyToDieRegular-6AjD.ttf",20)
    text = font.render(info_name+str(info_count),True,WHITE)
    skjerm.blit(text,(width-340,info_y))

def pie(x,y):   #for å tegne paien
    skjerm.blit(pieImg,(x,y))

def linjer_vertikal(farge,linjex,linje_starty,linje_slutty,tykkelse):   #for å tegne rutenettet
    pygame.draw.line(skjerm,farge,(linjex,linje_starty),(linjex,linje_slutty),tykkelse)

def enemies(lane,enemy_starty,enemy_width,enemy_height,enemy_colour):   #lager klossene
    pygame.draw.rect(skjerm,enemy_colour,[lane,enemy_starty,enemy_width,enemy_height])

def powerup(p_up):  #for å bestemme om du får en knuse- eller bonusblokk
    p_colour = RED
    if p_up == 1:
        p_colour = BRIGHT_YELLOW

    return p_colour

def text_objects(text, font):   #
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def yellow_thing(): #hva som skjer når du treffer en gul blokk
    global enemies_passed
    global enemy_y
    global enemylane
    global p_up_value
    global enemyh
    pygame.mixer.Sound.play(sound_bonus)
    enemies_passed += random.randint(5,15)
    enemy_y = 0 - enemyh - 100
    enemylane = random.randint(1,7)
    p_up_value = random.randint(1,10)


def button(button_name,x,y,w,h,pc,c,action=None): #button name, x, y, width, height, pressed colour and unpressed colour
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(skjerm,pc,(x,y,w,h,))
            if click[0] == 1 and action != None:
                if action == "start":
                    main()
                elif action == "exit":
                    pygame.quit()
                    quit()
                elif action == "help":
                    help_screen()
                elif action == "title":
                    titlescreen()



        else:
            pygame.draw.rect(skjerm,c,(x,y,w,h))

        smalltext=pygame.font.Font("ScreamWhenYoureReadyToDieRegular-6AjD.ttf",20)
        textSurf, textRect = text_objects(button_name,smalltext)
        textRect.center = ((x+(w/2)),(y+h/2))
        skjerm.blit(textSurf,textRect)


def crash(): #hva som skjer når du treffer en rød blokk
    crashed = True
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(sound_splat)
    while crashed == True:
        largeText = pygame.font.Font("ScreamWhenYoureReadyToDieRegular-6AjD.ttf",60)
        TextSurf, TextRect = text_objects("SQUISHED!!", largeText)
        TextRect.center = ((width/2),(height/3))
        skjerm.blit(TextSurf, TextRect)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()

        button("RETRY",450,300,150,75,DARK_YELLOW,YELLOW,"start")
        button("LEAVE",450,400,150,75,DARK_RED,RED,"exit")

        pygame.display.update()
        klokke.tick(15)


def help_screen():
    helpscreen = True
    while helpscreen == True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
        bg = pygame.image.load("piegame_helpscreen.png") #laster opp bakgrunnsbilde
        skjerm.blit(bg,(0,0))
        button("BACK",450,459,150,75,DARK_RED,RED,"title")


        pygame.display.update()
        klokke.tick(15)



def titlescreen():
    titlescreen = True
    while titlescreen == True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
        bg = pygame.image.load("piegame_introscreen.png")   #laster opp bakgrunnsbilde
        skjerm.blit(bg,(0,0))
        button("START",450,200,150,75,DARK_YELLOW,YELLOW,"start")
        button("HELP",450,300,150,75,DARK_BLUE,BLUE,"help")
        button("LEAVE",450,400,150,75,DARK_RED,RED,"exit")

        pygame.display.update()
        klokke.tick(15)




#gameloop
def main():
    pygame.mixer.music.play(-1)

    #globale variabler
    global highscore
    global enemies_passed
    global enemy_y
    global enemylane
    global p_up_value
    global enemyh

    #for enemies
    lanex = 0
    lane1 = 110 #x-verdi for bane 1 osv
    lane2 = 310
    lane3 = 510
    enemy_y = -500 #hvor første fiende spawner
    enemyw = 180 #width
    enemyh = 150 #height
    enemylane = random.randint(1,7)
    enemyspeed = 5 #faten til fiende
    p_up_value = random.randint(1,15)

    lane1_check = False
    lane2_check = False
    lane3_check = False

    #for the Pie
    x = lane3 - pie_width - 32
    y = (height * 0.79)
    x_change = 0
    player_speed = 7
    d_down = False
    a_down = False


    #for vansklighetsgrad/informasjon
    enemies_passed = 0
    difficulty_change = 5
    level = 1



    pygame.display.update()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_a or e.key == pygame.K_LEFT:
                    x_change = -1*player_speed
                    a_down = True

                if e.key == pygame.K_d or e.key == pygame.K_RIGHT:
                    x_change = player_speed
                    d_down = True

            if e.type == pygame.KEYUP:

                if e.key == pygame.K_a or e.key == pygame.K_LEFT:
                    a_down = False
                    if d_down == True:  #gjør at du ikke "henger" når du skal bytte vei
                        x_change = player_speed
                    elif d_down == False:
                        x_change = 0

                if e.key == pygame.K_d or e.key == pygame.K_RIGHT:
                    d_down = False
                    if a_down == True:
                        x_change = -1*player_speed
                    elif a_down == False:
                        x_change = 0


        x += x_change

        skjerm.fill(SCREEN_BLUE)

        #def enemies(lane,enemy_starty,enemy_width,enemy_height,enemy_colour):
        if enemylane == 1:
            enemycolour = powerup(p_up_value)
            enemies(lane1,enemy_y,enemyw,enemyh,enemycolour)
            lane1_check = True
        elif enemylane == 2:
            enemycolour = powerup(p_up_value)
            enemies(lane2,enemy_y,enemyw,enemyh,enemycolour)
            lane2_check = True
        elif enemylane == 3:
            enemycolour = powerup(p_up_value)
            enemies(lane3,enemy_y,enemyw,enemyh,enemycolour)
            lane3_check = True
        elif enemylane == 4:
            enemycolour = RED
            enemies(lane1,enemy_y,enemyw,enemyh,enemycolour)
            enemies(lane2,enemy_y,enemyw,enemyh,enemycolour)
            lane1_check = True
            lane2_check = True
        elif enemylane == 5:
            enemycolour = RED
            enemies(lane1,enemy_y,enemyw,enemyh,enemycolour)
            enemies(lane3,enemy_y,enemyw,enemyh,enemycolour)
            lane1_check = True
            lane3_check = True
        else:
            enemycolour = RED
            enemies(lane2,enemy_y,enemyw,enemyh,enemycolour)
            enemies(lane3,enemy_y,enemyw,enemyh,enemycolour)
            lane2_check = True
            lane3_check = True

        #lager banene visuelt
        linje_x = 0
        linje_forste = 100
        linje_siste = 700
        linje_forste_lokke = int(linje_forste/100)
        linje_siste_lokke = int((linje_siste/100)+1)
        bunnlinje_y = height*0.95

        for i in range(linje_forste_lokke,linje_siste_lokke,2):
            linje_x = i*100
            linjer_vertikal(GRAY,linje_x,0,bunnlinje_y,5)
        pygame.draw.line(skjerm,GRAY,(linje_forste,bunnlinje_y),(linje_siste,bunnlinje_y),5)

        #tegner inn resten av det som skal på skjermen
        pie(x,y)
        pygame.draw.rect(skjerm,SCREEN_BLUE,(0,bunnlinje_y+2.5,width,height))
        enemy_y += enemyspeed
        info("Level: ",level,10)
        info("Points: ",enemies_passed,50)
        info("Highscore: ",highscore,90)

        pygame.display.update()
        klokke.tick(60)

        #logic_loop
        if x < linje_forste +5 or x > linje_siste - pie_width - 5:
            x_change = 0


        if enemy_y > height:
            enemy_y = 0 - enemyh - 100
            enemylane = random.randint(1,7)
            p_up_value = random.randint(1,10)
            enemies_passed += 1


        if enemies_passed > difficulty_change: #opp en level
                enemyspeed += 2
                player_speed += 2
                level += 1
                difficulty_change += 10


        if enemies_passed > highscore:
            highscore = enemies_passed


        if enemycolour == RED:
            if y < enemy_y + enemyh and y + 90 > enemy_y:
                if lane1_check == True:
                    if x > lane1 and x < lane1 + enemyw or x + pie_width > lane1 and x + pie_width < lane1 + enemyw:
                        crash()
                if lane2_check == True:
                    if x > lane2 and x < lane2 + enemyw or x + pie_width > lane2 and x + pie_width < lane2 + enemyw:
                        crash()
                if lane3_check == True:
                    if x > lane3 and x < lane3 + enemyw or x + pie_width > lane3 and x + pie_width < lane3 + enemyw:
                        crash()
            lane1_check = False
            lane2_check = False
            lane3_check = False

        elif enemycolour == BRIGHT_YELLOW:
            if y < enemy_y + enemyh and y + 90 > enemy_y:
                if lane1_check == True:
                    if x > lane1 and x < lane1 + enemyw or x + pie_width > lane1 and x + pie_width < lane1 + enemyw:
                        yellow_thing()
                if lane2_check == True:
                    if x > lane2 and x < lane2 + enemyw or x + pie_width > lane2 and x + pie_width < lane2 + enemyw:
                        yellow_thing()
                if lane3_check == True:
                    if x > lane3 and x < lane3 + enemyw or x + pie_width > lane3 and x + pie_width < lane3 + enemyw:
                        yellow_thing()
            lane1_check = False
            lane2_check = False
            lane3_check = False



titlescreen()
main()
pygame.quit()
quit()


