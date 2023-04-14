import pygame
import os 
import sys
import random
import time
import math
#提供一開始的遊戲起始難度做選擇

# Initialize
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Create a window  
CLOCK = pygame.time.Clock()
WIN_RESOLUTIONS = pygame.display.Info()
pygame.display.set_caption("Dodge Game")
ICON = pygame.image.load(os.path.join("Assets" , "game_icon.png"))
pygame.display.set_icon(ICON)  # Set game's icon

# Set window
WIN_RESOLUTIONS = pygame.display.Info()
WIN_WIDTH , WIN_HEIGHT = WIN_RESOLUTIONS.current_w - 400 , WIN_RESOLUTIONS.current_h - 110  #1000 , 900
print(WIN_WIDTH , WIN_HEIGHT)
WIN = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT) , pygame.RESIZABLE)

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
Turquoise = (51,230,204)  # 綠松藍色
GOLD = (255,215,0)

# Load images
ORI_CHAR_IMG = pygame.image.load(os.path.join("Assets" , "char.png"))
ORI_BALL_IMG = pygame.image.load(os.path.join("Assets" , "ball.png"))
MUTE = pygame.transform.scale(pygame.image.load(os.path.join("Assets" , "mute.png")) , (50,50))
UNMUTE = pygame.transform.scale(pygame.image.load(os.path.join("Assets" , "unmute.png")) , (50,50))

# Load musics
PAUSE_SOUND = pygame.mixer.Sound(os.path.join("Assets" , "don.mp3"))
PAUSE_SOUND.set_volume(0.4)
CRASH_SOUND = pygame.mixer.Sound(os.path.join("Assets" , "Meow.wav"))
CRASH_SOUND.set_volume(0.5)
pygame.mixer.music.load(os.path.join("Assets" , "BG_music.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# Some variables 
LINE_SPACE = 9
pause_state = False
F11_times = 0
on_or_off = [True , False]
VELOCITY = 4
pause_time = 0
fail_waiting = True
sound_check = 1
unmute_pos = pygame.Rect(WIN_WIDTH - UNMUTE.get_rect().width - 15 , 10 , UNMUTE.get_rect().width , UNMUTE.get_rect().height)  

# Load record 
try:
    with open(os.path.join("Assets" , "Record.txt") , 'r') as f:
        try:
            record = int(f.read())
        except:
            record = 0
except:
    record = 0 

class Char:
    def __init__(self , x , y , width , height , CHAR_IMG):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = CHAR_IMG
        self.rect = pygame.Rect(x , y , width , height)
    
    def update_rect(self):
        self.rect = pygame.Rect(self.x , self.y , self.width , self.height)

class Ball:
    def __init__(self , x , y , width , height , BALL_IMG):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = BALL_IMG
        self.rect = pygame.Rect(x , y , width , height)
        self.vel = 3.5
    
    def update_rect(self):
        self.rect = pygame.Rect(self.x , self.y , self.width , self.height)

    def move_right(self):
        self.x += self.vel
    def move_left(self):
        self.x -= self.vel
    def move_up(self):
        self.y -= self.vel
    def move_down(self):
        self.y += self.vel

    def change_vel(self):
        self.vel = VELOCITY

CHAR_ON_INIT = pygame.transform.scale(ORI_CHAR_IMG , (WIN_WIDTH/LINE_SPACE*1.3 , WIN_HEIGHT/LINE_SPACE*1.3))
class Char_screen(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = CHAR_ON_INIT
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0 , WIN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(0 , WIN_HEIGHT - self.rect.height)
        self.x_vel = random.randrange(-3,3)
        self.y_vel = random.randrange(-3,3)
        self.degree_list = [-3,-2,-1,1,2,3]
        self.rotate_degree = random.choice(self.degree_list)
        self.angle = 0

    def rotate(self):
        self.angle += self.rotate_degree
        self.angle %= 360
        self.image = pygame.transform.rotate(self.image_original , self.angle)
        self.image.set_colorkey(WHITE)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        if self.rect.right <= 0:
            self.rect.left = WIN_WIDTH
        elif self.rect.left >= WIN_WIDTH:
            self.rect.right = 0
        elif self.rect.top >= WIN_HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom <= 0:
            self.rect.top = WIN_HEIGHT

# Resize images
CHAR_IMG = pygame.transform.scale(ORI_CHAR_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
BALL_IMG = pygame.transform.scale(ORI_BALL_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))

# Class variables
char = Char(WIN_WIDTH/2 - WIN_WIDTH/LINE_SPACE/2 , WIN_HEIGHT/2 - WIN_HEIGHT/LINE_SPACE/2 , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , CHAR_IMG)
l_r_balls = [Ball(-150 , WIN_HEIGHT/LINE_SPACE*i , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG) for i in [random.randint(0 , 8) for _ in range(3)]] # 不重疊到的話:random.sample(range(9) , 3)
r_l_balls = [Ball(WIN_WIDTH + 150 , WIN_HEIGHT/LINE_SPACE*i , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG) for i in [random.randint(0 , 8) for _ in range(3)]] # 不重疊到的話:random.sample(range(9) , 3)
d_u_balls = [Ball(WIN_WIDTH/LINE_SPACE*i , WIN_HEIGHT + 200 , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG) for i in [random.randint(0 , 8) for _ in range(3)]] # 不重疊到的話:random.sample(range(9) , 3)
u_d_balls = [Ball(WIN_WIDTH/LINE_SPACE*i , -200 , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG) for i in [random.randint(0 , 8) for _ in range(3)]] # 不重疊到的話:random.sample(range(9) , 3)

def draw_text(text , font , font_size , x , y , color , bold = None):
    try:
        main_font = pygame.font.Font(font , font_size)
    except:
        main_font = pygame.font.SysFont(font , font_size , bold)
    render_text = main_font.render(text , True , color)
    text_rect = render_text.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    WIN.blit(render_text , text_rect)

def draw_failure(during_time):
    global WIN , WIN_WIDTH , WIN_HEIGHT , pause_state , char , CHAR_IMG , BALL_IMG , F11_times , on_or_off , l_r_balls , r_l_balls , d_u_balls , u_d_balls , fail_waiting , record
    # waiting = True
    if fail_waiting:
        CRASH_SOUND.play()
    """ 
    try:
        with open(os.path.join("Assets" , "Record.txt") , 'r') as f:
            try:
                record = int(f.read())
            except:
                record = 0
    except:
        record = 0 
    """
    NEWRECORD = False
    if record < during_time:
        NEWRECORD = True
        with open(os.path.join("Assets" , "Record.txt") , 'w') as f1:
            f1.write(str(during_time))
        record = during_time

    while fail_waiting:
        CLOCK.tick(60)
        redraw_window(during_time)
        if record:
            draw_text(f"Record : {(record//60)//60:0>2d}:{(record//60)%60:0>2d}:{record%60:0>2d}" , os.path.join("Assets" , "ComicSansMS3.ttf") , 20 , 100 , 45 , BLACK , False)
        draw_text(f"You crashed !" , os.path.join("Assets" , "Courier.ttf") , 50 , WIN_WIDTH/2 , WIN_HEIGHT/2 , BLUE , 1)
        draw_text("Press Enter to play again" , os.path.join("Assets" , "Courier.ttf") , 35 , WIN_WIDTH/2 , WIN_HEIGHT*3/4 , BLUE , 1)
        if NEWRECORD:
            draw_text("New Record !" , os.path.join("Assets" , "Courier.ttf") , 55 , WIN_WIDTH/2 , WIN_HEIGHT/4 , GOLD , 2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.VIDEORESIZE:
                ORI_WIN_WIDTH , ORI_WIN_HEIGHT = WIN_WIDTH , WIN_HEIGHT
                WIN_WIDTH , WIN_HEIGHT = event.w , event.h
                WIN = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT) , pygame.RESIZABLE)
                CHAR_IMG = pygame.transform.scale(ORI_CHAR_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                char = Char(char.x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , char.y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , CHAR_IMG)
                BALL_IMG = pygame.transform.scale(ORI_BALL_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                for i in range(len(l_r_balls)):
                    l_r_balls[i] = Ball(l_r_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , l_r_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                for i in range(len(r_l_balls)):
                    r_l_balls[i] = Ball(r_l_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , r_l_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                for i in range(len(d_u_balls)):
                    d_u_balls[i] = Ball(d_u_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , d_u_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                for i in range(len(u_d_balls)):
                    u_d_balls[i] = Ball(u_d_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , u_d_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                redraw_window(during_time)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True

                if event.key == pygame.K_F11:
                        if F11_times % 2:
                            ORI_WIN_WIDTH , ORI_WIN_HEIGHT = WIN_WIDTH , WIN_HEIGHT
                            WIN_WIDTH , WIN_HEIGHT = WIN_RESOLUTIONS.current_w - 400 , WIN_RESOLUTIONS.current_h - 110  #1000 , 900
                            WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT) , pygame.RESIZABLE)
                            CHAR_IMG = pygame.transform.scale(ORI_CHAR_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                            char = Char(char.x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , char.y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , CHAR_IMG)
                            BALL_IMG = pygame.transform.scale(ORI_BALL_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                            for i in range(len(l_r_balls)):
                                l_r_balls[i] = Ball(l_r_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , l_r_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(r_l_balls)):
                                r_l_balls[i] = Ball(r_l_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , r_l_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(d_u_balls)):
                                d_u_balls[i] = Ball(d_u_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , d_u_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(u_d_balls)):
                                u_d_balls[i] = Ball(u_d_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , u_d_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            pygame.mouse.set_visible(True)
                        else:
                            ORI_WIN_WIDTH , ORI_WIN_HEIGHT = WIN_WIDTH , WIN_HEIGHT
                            WIN_WIDTH , WIN_HEIGHT  = WIN_RESOLUTIONS.current_w , WIN_RESOLUTIONS.current_h
                            WIN = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT) , pygame.FULLSCREEN | pygame.NOFRAME)
                            CHAR_IMG = pygame.transform.scale(ORI_CHAR_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                            char = Char(char.x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , char.y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , CHAR_IMG)
                            BALL_IMG = pygame.transform.scale(ORI_BALL_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                            for i in range(len(l_r_balls)):
                                l_r_balls[i] = Ball(l_r_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , l_r_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(r_l_balls)):
                                r_l_balls[i] = Ball(r_l_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , r_l_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(d_u_balls)):
                                d_u_balls[i] = Ball(d_u_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , d_u_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(u_d_balls)):
                                u_d_balls[i] = Ball(u_d_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , u_d_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            pygame.mouse.set_visible(False)
                        F11_times += 1 
                        redraw_window(during_time)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    fail_waiting = False
                    return False
    return False

def draw_window(during_time):
    WIN.fill(WHITE) # Background
        
    # Draw background lines
    for i in range(1 , LINE_SPACE+1):
        pygame.draw.line(WIN , BLACK , (0 , WIN_HEIGHT/LINE_SPACE*i) , (WIN_WIDTH , WIN_HEIGHT/LINE_SPACE*i) , 2)
        pygame.draw.line(WIN , BLACK , (WIN_WIDTH/LINE_SPACE*i , 0) , (WIN_WIDTH/LINE_SPACE*i , WIN_HEIGHT) , 2)
    # Draw background lines

    WIN.blit(char.img , (char.x , char.y))
    char.update_rect()
    # pygame.draw.rect(BLUE , char.rect) 

    #左到右的球
    for l_r_ball in l_r_balls:
        WIN.blit(l_r_ball.img , (l_r_ball.x , l_r_ball.y))
        l_r_ball.move_right()
        l_r_ball.update_rect()
        l_r_ball.change_vel()
        # pygame.draw.rect(RED , l_r_ball.rect) 
    
    #右到左
    for r_l_ball in r_l_balls:
        WIN.blit(r_l_ball.img , (r_l_ball.x , r_l_ball.y))
        r_l_ball.move_left()
        r_l_ball.update_rect()
        r_l_ball.change_vel()

    
    #下到上
    for d_u_ball in d_u_balls:
        WIN.blit(d_u_ball.img , (d_u_ball.x , d_u_ball.y))
        d_u_ball.move_up()
        d_u_ball.update_rect()
        d_u_ball.change_vel()

    #上到下
    for u_d_ball in u_d_balls:
        WIN.blit(u_d_ball.img , (u_d_ball.x , u_d_ball.y))
        u_d_ball.move_down()
        u_d_ball.update_rect()
        u_d_ball.change_vel()

    draw_text(f"Time : {(during_time//60)//60:0>2d}:{(during_time//60)%60:0>2d}:{during_time%60:0>2d}" , os.path.join("Assets" , "ComicSansMS3.ttf") , 20 , 90 , 20 , BLACK)
    if record:
        draw_text(f"Record : {(record//60)//60:0>2d}:{(record//60)%60:0>2d}:{record%60:0>2d}" , os.path.join("Assets" , "ComicSansMS3.ttf") , 20 , 100 , 45 , BLACK , False)

    pygame.display.update()

def redraw_window(during_time):
    WIN.fill(WHITE) # Background

    # Draw background lines
    for i in range(1 , LINE_SPACE+1):
        pygame.draw.line(WIN , BLACK , (0 , WIN_HEIGHT/LINE_SPACE*i) , (WIN_WIDTH , WIN_HEIGHT/LINE_SPACE*i) , 2)
        pygame.draw.line(WIN , BLACK , (WIN_WIDTH/LINE_SPACE*i , 0) , (WIN_WIDTH/LINE_SPACE*i , WIN_HEIGHT) , 2)
    # Draw background lines

    WIN.blit(char.img , (char.x , char.y))
    char.update_rect()

    for l_r_ball in l_r_balls:
        WIN.blit(l_r_ball.img , (l_r_ball.x , l_r_ball.y))
        l_r_ball.update_rect()

    for r_l_ball in r_l_balls:
        WIN.blit(r_l_ball.img , (r_l_ball.x , r_l_ball.y))
        r_l_ball.update_rect()

    for d_u_ball in d_u_balls:
        WIN.blit(d_u_ball.img , (d_u_ball.x , d_u_ball.y))
        d_u_ball.update_rect()

    for u_d_ball in u_d_balls:
        WIN.blit(u_d_ball.img , (u_d_ball.x , u_d_ball.y))
        u_d_ball.update_rect()

    draw_text(f"Time : {(during_time//60)//60:0>2d}:{(during_time//60)%60:0>2d}:{during_time%60:0>2d}" , os.path.join("Assets" , "ComicSansMS3.ttf") , 20 , 90 , 20 , BLACK)
    if record:
        draw_text(f"Record : {(record//60)//60:0>2d}:{(record//60)%60:0>2d}:{record%60:0>2d}" , os.path.join("Assets" , "ComicSansMS3.ttf") , 20 , 100 , 45 , BLACK , False)

    # pygame.display.update()

def pause(during_time):
    global WIN , WIN_WIDTH , WIN_HEIGHT , pause_state , char , CHAR_IMG , BALL_IMG , F11_times , on_or_off , l_r_balls , r_l_balls , d_u_balls , u_d_balls , pause_time , sound_check , unmute_pos
    pause_start = time.time()  #暫停開始的時間
    waiting = True
    while waiting:
        CLOCK.tick(60)
        if sound_check % 2:
            # pygame.draw.rect(WIN , WHITE , (WIN_WIDTH - UNMUTE.get_rect().width - 15 , 10 , WIN_WIDTH - 15 , 10 + UNMUTE.get_rect().height))  # Redraw right corner to update mute or unmute
            redraw_window(during_time)    
            WIN.blit(UNMUTE , (WIN_WIDTH - UNMUTE.get_rect().width - 15 , 10))
        else:
            # pygame.draw.rect(WIN , WHITE , (WIN_WIDTH - UNMUTE.get_rect().width - 15 , 10 , WIN_WIDTH - 15 , 10 + UNMUTE.get_rect().height))  # Redraw right corner to update mute or unmute
            redraw_window(during_time)    
            WIN.blit(MUTE , (WIN_WIDTH - MUTE.get_rect().width - 15 , 10))

        draw_text("Pause" , os.path.join("Assets" , "Courier.ttf") , 100 , WIN_WIDTH/2 , WIN_HEIGHT/2 , BLUE , 3)
        draw_text("F11 : Full Screen" , os.path.join("Assets" , "ComicSansMS3.ttf") , 20 , WIN_WIDTH - 100 , 90 , BLACK)
        draw_text("Esc : End the game" , os.path.join("Assets" , "ComicSansMS3.ttf") , 20 , WIN_WIDTH - 100 , 120 , BLACK)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.VIDEORESIZE:
                ORI_WIN_WIDTH , ORI_WIN_HEIGHT = WIN_WIDTH , WIN_HEIGHT
                WIN_WIDTH , WIN_HEIGHT = event.w , event.h
                WIN = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT) , pygame.RESIZABLE)
                unmute_pos = pygame.Rect(WIN_WIDTH - UNMUTE.get_rect().width - 15 , 10 , UNMUTE.get_rect().width , UNMUTE.get_rect().height)  
                CHAR_IMG = pygame.transform.scale(ORI_CHAR_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                char = Char(char.x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , char.y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , CHAR_IMG)
                BALL_IMG = pygame.transform.scale(ORI_BALL_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                for i in range(len(l_r_balls)):
                    l_r_balls[i] = Ball(l_r_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , l_r_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                for i in range(len(r_l_balls)):
                    r_l_balls[i] = Ball(r_l_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , r_l_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                for i in range(len(d_u_balls)):
                    d_u_balls[i] = Ball(d_u_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , d_u_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                for i in range(len(u_d_balls)):
                    u_d_balls[i] = Ball(u_d_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , u_d_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                redraw_window(during_time)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True

                if event.key == pygame.K_F11:
                        if F11_times % 2:
                            ORI_WIN_WIDTH , ORI_WIN_HEIGHT = WIN_WIDTH , WIN_HEIGHT
                            WIN_WIDTH , WIN_HEIGHT = WIN_RESOLUTIONS.current_w - 400 , WIN_RESOLUTIONS.current_h - 110  #1000 , 900
                            WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT) , pygame.RESIZABLE)
                            CHAR_IMG = pygame.transform.scale(ORI_CHAR_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                            char = Char(char.x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , char.y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , CHAR_IMG)
                            BALL_IMG = pygame.transform.scale(ORI_BALL_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                            for i in range(len(l_r_balls)):
                                l_r_balls[i] = Ball(l_r_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , l_r_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(r_l_balls)):
                                r_l_balls[i] = Ball(r_l_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , r_l_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(d_u_balls)):
                                d_u_balls[i] = Ball(d_u_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , d_u_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(u_d_balls)):
                                u_d_balls[i] = Ball(u_d_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , u_d_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            pygame.mouse.set_visible(True)
                        else:
                            ORI_WIN_WIDTH , ORI_WIN_HEIGHT = WIN_WIDTH , WIN_HEIGHT
                            WIN_WIDTH , WIN_HEIGHT  = WIN_RESOLUTIONS.current_w , WIN_RESOLUTIONS.current_h
                            WIN = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT) , pygame.FULLSCREEN | pygame.NOFRAME)
                            CHAR_IMG = pygame.transform.scale(ORI_CHAR_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                            char = Char(char.x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , char.y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , CHAR_IMG)
                            BALL_IMG = pygame.transform.scale(ORI_BALL_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                            for i in range(len(l_r_balls)):
                                l_r_balls[i] = Ball(l_r_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , l_r_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(r_l_balls)):
                                r_l_balls[i] = Ball(r_l_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , r_l_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(d_u_balls)):
                                d_u_balls[i] = Ball(d_u_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , d_u_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(u_d_balls)):
                                u_d_balls[i] = Ball(u_d_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , u_d_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            pygame.mouse.set_visible(False)
                        F11_times += 1 
                        redraw_window(during_time)
                
                if event.key == pygame.K_SPACE:
                    pause_state = on_or_off[0]
                    on_or_off.reverse()
                    pause_time += time.time() - pause_start  #計算暫停的時間
                    return False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x , mouse_y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0] and unmute_pos.left < mouse_x < unmute_pos.right and unmute_pos.top < mouse_y < unmute_pos.bottom:
                    sound_check += 1
                    if sound_check % 2:
                        PAUSE_SOUND.set_volume(0.4)
                        CRASH_SOUND.set_volume(0.5)
                        pygame.mixer.music.unpause()
                        # pygame.mixer.music.set_volume(0.2)
                    else:
                        PAUSE_SOUND.set_volume(0)
                        CRASH_SOUND.set_volume(0)
                        pygame.mixer.music.pause()
                        # pygame.mixer.music.set_volume(0)
                
def change_velocity(during_time):
    global VELOCITY
    if 0 <= during_time < 10:
        VELOCITY = 4
    elif 10 <= during_time < 25:
        VELOCITY = 4.5
    elif 25 <= during_time < 40:
        VELOCITY = 5.5
    elif 40 <= during_time < 60:
        VELOCITY = 6.5
    elif 60 <= during_time < 90:
        VELOCITY = 7.5
    elif 90 <= during_time < 120:
        VELOCITY = 9
    elif 120 <= during_time < 150:
        VELOCITY = 10
    elif 150 <= during_time < 180:
        VELOCITY = 11
    elif 180 <= during_time < 210:
        VELOCITY = 12
    elif 210 <= during_time < 240:
        VELOCITY = 13
    elif 240 <= during_time < 270:
        VELOCITY = 14
    elif 270 <= during_time < 300:
        VELOCITY = 15
    elif 300 <= during_time:
        VELOCITY = 16
    else:
        VELOCITY = 4

def draw_init_screen():
    global WIN , WIN_WIDTH , WIN_HEIGHT , pause_state , char , CHAR_IMG , BALL_IMG , F11_times , on_or_off , l_r_balls , r_l_balls , d_u_balls , u_d_balls , pause_time
    char_sprites = pygame.sprite.Group()
    for _ in range(10):
        chars = Char_screen()
        char_sprites.add(chars)
    waiting = True
    while waiting:
        CLOCK.tick(60)
        WIN.fill(WHITE)
        char_sprites.draw(WIN)
        char_sprites.update()
        draw_text("Welcome to Dodge Game!" , os.path.join("Assets" , "Courier.ttf") , 40 , WIN_WIDTH/2 , WIN_HEIGHT/3 , BLACK)
        draw_text("Use arrow key to move the character" , os.path.join("Assets" , "Courier.ttf") , 35 , WIN_WIDTH/2 , WIN_HEIGHT/2 , BLUE)
        draw_text("Press Enter to start" , os.path.join("Assets" , "Courier.ttf") , 30 , WIN_WIDTH/2 , WIN_HEIGHT*2/3 , BLACK)
        draw_text("(Press Space to pause)" , os.path.join("Assets" , "Courier.ttf") , 25 , WIN_WIDTH/2 , WIN_HEIGHT*7/9 , BLACK)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.quit()
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                if event.key == pygame.K_F11:
                    if F11_times % 2:
                        ORI_WIN_WIDTH , ORI_WIN_HEIGHT = WIN_WIDTH , WIN_HEIGHT
                        WIN_WIDTH , WIN_HEIGHT = WIN_RESOLUTIONS.current_w - 400 , WIN_RESOLUTIONS.current_h - 110  #1000 , 900
                        WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT) , pygame.RESIZABLE)
                        CHAR_IMG = pygame.transform.scale(ORI_CHAR_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                        char = Char(char.x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , char.y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , CHAR_IMG)
                        BALL_IMG = pygame.transform.scale(ORI_BALL_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                        for i in range(len(l_r_balls)):
                            l_r_balls[i] = Ball(l_r_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , l_r_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                        for i in range(len(r_l_balls)):
                            r_l_balls[i] = Ball(r_l_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , r_l_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                        for i in range(len(d_u_balls)):
                            d_u_balls[i] = Ball(d_u_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , d_u_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                        for i in range(len(u_d_balls)):
                            u_d_balls[i] = Ball(u_d_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , u_d_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                        pygame.mouse.set_visible(True)
                    else:
                        ORI_WIN_WIDTH , ORI_WIN_HEIGHT = WIN_WIDTH , WIN_HEIGHT
                        WIN_WIDTH , WIN_HEIGHT  = WIN_RESOLUTIONS.current_w , WIN_RESOLUTIONS.current_h
                        WIN = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT) , pygame.FULLSCREEN | pygame.NOFRAME)
                        CHAR_IMG = pygame.transform.scale(ORI_CHAR_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                        char = Char(char.x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , char.y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , CHAR_IMG)
                        BALL_IMG = pygame.transform.scale(ORI_BALL_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                        for i in range(len(l_r_balls)):
                            l_r_balls[i] = Ball(l_r_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , l_r_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                        for i in range(len(r_l_balls)):
                            r_l_balls[i] = Ball(r_l_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , r_l_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                        for i in range(len(d_u_balls)):
                            d_u_balls[i] = Ball(d_u_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , d_u_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                        for i in range(len(u_d_balls)):
                            u_d_balls[i] = Ball(u_d_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , u_d_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                        pygame.mouse.set_visible(False)
                    F11_times += 1 
                    
            if event.type == pygame.VIDEORESIZE:
                ORI_WIN_WIDTH , ORI_WIN_HEIGHT = WIN_WIDTH , WIN_HEIGHT
                WIN_WIDTH , WIN_HEIGHT = event.w , event.h
                WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT) , pygame.RESIZABLE)
                CHAR_IMG = pygame.transform.scale(ORI_CHAR_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                char = Char(char.x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , char.y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , CHAR_IMG)
                BALL_IMG = pygame.transform.scale(ORI_BALL_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                for i in range(len(l_r_balls)):
                    l_r_balls[i] = Ball(l_r_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , l_r_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                for i in range(len(r_l_balls)):
                    r_l_balls[i] = Ball(r_l_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , r_l_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                for i in range(len(d_u_balls)):
                    d_u_balls[i] = Ball(d_u_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , d_u_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                for i in range(len(u_d_balls)):
                    u_d_balls[i] = Ball(u_d_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , u_d_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    # waiting = False
                    return False


def main(show):
    global WIN , WIN_WIDTH , WIN_HEIGHT , pause_state , char , CHAR_IMG , BALL_IMG , F11_times , on_or_off , l_r_balls , r_l_balls , d_u_balls , u_d_balls , pause_time , fail_waiting , ori_char_pos

    # Class variables (When restart the game , we need to initialize these variables)
    char = Char(WIN_WIDTH/2 - WIN_WIDTH/LINE_SPACE/2 , WIN_HEIGHT/2 - WIN_HEIGHT/LINE_SPACE/2 , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , CHAR_IMG)
    l_r_balls = [Ball(-150 , WIN_HEIGHT/LINE_SPACE*i , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG) for i in [random.randint(0 , 8) for _ in range(3)]] # 不重疊到的話:random.sample(range(9) , 3)
    r_l_balls = [Ball(WIN_WIDTH + 150 , WIN_HEIGHT/LINE_SPACE*i , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG) for i in [random.randint(0 , 8) for _ in range(3)]] # 不重疊到的話:random.sample(range(9) , 3)
    d_u_balls = [Ball(WIN_WIDTH/LINE_SPACE*i , WIN_HEIGHT + 200 , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG) for i in [random.randint(0 , 8) for _ in range(3)]] # 不重疊到的話:random.sample(range(9) , 3)
    u_d_balls = [Ball(WIN_WIDTH/LINE_SPACE*i , -200 , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG) for i in [random.randint(0 , 8) for _ in range(3)]] # 不重疊到的話:random.sample(range(9) , 3)

    #start time
    START_TIME = time.time()  #重置遊戲時間
    pause_time = 0

    fail_waiting = True  #重置跳出失敗畫面
     
    init_show = show  #起始畫面
    run = True
    while run:
        if init_show:
            close = draw_init_screen()
            if close:
                return True
            init_show = False
            START_TIME = time.time()  #遊戲正式開始的時間

        CLOCK.tick(60) # FPS
        during_time = math.floor(time.time() - START_TIME - pause_time)  #扣除遊戲開始時間跟暫停的時間
        change_velocity(during_time)

        if pause_state:
            pause_game = pause(during_time)
            if pause_game:
                return True
        else:
            for l_r_ball in l_r_balls:
                if l_r_ball.rect.right - WIN_WIDTH/LINE_SPACE/2 >= char.rect.left and l_r_ball.rect.left <= char.rect.right - WIN_WIDTH/LINE_SPACE/2 and l_r_ball.rect.bottom >= char.rect.top + WIN_HEIGHT/LINE_SPACE/3.5 and l_r_ball.rect.top <= char.rect.bottom - WIN_HEIGHT/LINE_SPACE/3.5:
                    # CRASH_SOUND.play()
                    fail = draw_failure(during_time)
                    if fail:
                        return True
                    else:
                        run = False
                        break
                if l_r_ball.rect.left > WIN_WIDTH:
                    l_r_ball.x = -150
                    l_r_ball.y = WIN_HEIGHT/LINE_SPACE*random.randint(0,8)
            
            for r_l_ball in r_l_balls:
                if r_l_ball.rect.left + WIN_WIDTH/LINE_SPACE/2 <= char.rect.right and r_l_ball.rect.right >= char.rect.left + WIN_WIDTH/LINE_SPACE/2 and r_l_ball.rect.bottom >= char.rect.top + WIN_HEIGHT/LINE_SPACE/3.5 and r_l_ball.rect.top <= char.rect.bottom - WIN_HEIGHT/LINE_SPACE/3.5:
                    # CRASH_SOUND.play()
                    fail_1 = draw_failure(during_time)
                    if fail_1:
                        return True
                    else:
                        run = False
                        break
                if r_l_ball.rect.right < 0:
                    r_l_ball.x = WIN_WIDTH + 150   # - WIN_WIDTH/LINE_SPACE(讓左右兩邊同頻率，但剛好可以讓左右錯開，所以不同步)
                    r_l_ball.y = WIN_HEIGHT/LINE_SPACE*random.randint(0,8)

            for d_u_ball in d_u_balls:
                if d_u_ball.rect.top + WIN_HEIGHT/LINE_SPACE/3.5 <= char.rect.bottom and d_u_ball.rect.bottom >= char.rect.top + WIN_HEIGHT/LINE_SPACE/3.5 and d_u_ball.rect.left <= char.rect.right - WIN_WIDTH/LINE_SPACE/2 and d_u_ball.rect.right >= char.rect.left + WIN_WIDTH/LINE_SPACE/2:
                    # CRASH_SOUND.play()
                    fail_2 = draw_failure(during_time)
                    if fail_2:
                        return True
                    else:
                        run = False
                        break
                if d_u_ball.rect.bottom < 0:
                    d_u_ball.y = WIN_HEIGHT + 200 
                    d_u_ball.x = WIN_WIDTH/LINE_SPACE*random.randint(0,8)

            for u_d_ball in u_d_balls:
                if u_d_ball.rect.bottom - WIN_HEIGHT/LINE_SPACE/3.5 >= char.rect.top and u_d_ball.rect.top <= char.rect.bottom - WIN_HEIGHT/LINE_SPACE/3.5 and u_d_ball.rect.left <= char.rect.right - WIN_WIDTH/LINE_SPACE/2 and u_d_ball.rect.right >= char.rect.left + WIN_WIDTH/LINE_SPACE/2:
                    # CRASH_SOUND.play()
                    fail_3 = draw_failure(during_time)
                    if fail_3:
                        return True
                    else:
                        run = False
                        break
                if u_d_ball.rect.top > WIN_HEIGHT:
                    u_d_ball.y = -200
                    u_d_ball.x = WIN_WIDTH/LINE_SPACE*random.randint(0,8)

            draw_window(during_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
                
            if event.type == pygame.VIDEORESIZE:
                ORI_WIN_WIDTH , ORI_WIN_HEIGHT = WIN_WIDTH , WIN_HEIGHT
                WIN_WIDTH , WIN_HEIGHT = event.w , event.h
                WIN = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT) , pygame.RESIZABLE)
                CHAR_IMG = pygame.transform.scale(ORI_CHAR_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                char = Char(char.x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , char.y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , CHAR_IMG)
                BALL_IMG = pygame.transform.scale(ORI_BALL_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                for i in range(len(l_r_balls)):
                    l_r_balls[i] = Ball(l_r_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , l_r_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                for i in range(len(r_l_balls)):
                    r_l_balls[i] = Ball(r_l_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , r_l_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                for i in range(len(d_u_balls)):
                    d_u_balls[i] = Ball(d_u_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , d_u_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                for i in range(len(u_d_balls)):
                    u_d_balls[i] = Ball(u_d_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , u_d_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True

                if event.key == pygame.K_F11:
                        if F11_times % 2:
                            ORI_WIN_WIDTH , ORI_WIN_HEIGHT = WIN_WIDTH , WIN_HEIGHT
                            WIN_WIDTH , WIN_HEIGHT = WIN_RESOLUTIONS.current_w - 400 , WIN_RESOLUTIONS.current_h - 110  #1000 , 900
                            WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT) , pygame.RESIZABLE)
                            CHAR_IMG = pygame.transform.scale(ORI_CHAR_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                            char = Char(char.x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , char.y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , CHAR_IMG)
                            BALL_IMG = pygame.transform.scale(ORI_BALL_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                            for i in range(len(l_r_balls)):
                                l_r_balls[i] = Ball(l_r_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , l_r_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(r_l_balls)):
                                r_l_balls[i] = Ball(r_l_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , r_l_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(d_u_balls)):
                                d_u_balls[i] = Ball(d_u_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , d_u_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(u_d_balls)):
                                u_d_balls[i] = Ball(u_d_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , u_d_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            pygame.mouse.set_visible(True)
                        else:
                            ORI_WIN_WIDTH , ORI_WIN_HEIGHT = WIN_WIDTH , WIN_HEIGHT
                            WIN_WIDTH , WIN_HEIGHT  = WIN_RESOLUTIONS.current_w , WIN_RESOLUTIONS.current_h
                            WIN = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT) , pygame.FULLSCREEN | pygame.NOFRAME)
                            CHAR_IMG = pygame.transform.scale(ORI_CHAR_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                            char = Char(char.x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , char.y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , CHAR_IMG)
                            BALL_IMG = pygame.transform.scale(ORI_BALL_IMG , (WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE))
                            for i in range(len(l_r_balls)):
                                l_r_balls[i] = Ball(l_r_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , l_r_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(r_l_balls)):
                                r_l_balls[i] = Ball(r_l_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , r_l_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(d_u_balls)):
                                d_u_balls[i] = Ball(d_u_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , d_u_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            for i in range(len(u_d_balls)):
                                u_d_balls[i] = Ball(u_d_balls[i].x / (ORI_WIN_WIDTH/LINE_SPACE) * (WIN_WIDTH/LINE_SPACE) , u_d_balls[i].y / (ORI_WIN_HEIGHT/LINE_SPACE) * (WIN_HEIGHT/LINE_SPACE) , WIN_WIDTH/LINE_SPACE , WIN_HEIGHT/LINE_SPACE , BALL_IMG)
                            pygame.mouse.set_visible(False)
                        F11_times += 1 

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    char.y -= WIN_HEIGHT/LINE_SPACE
                    char.update_rect()
                    if char.y + 10 < 0 :
                        char.y = WIN_HEIGHT - WIN_HEIGHT/LINE_SPACE
                        char.update_rect()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    char.x += WIN_WIDTH/LINE_SPACE
                    char.update_rect()
                    if char.x + 10 >= WIN_WIDTH :
                        char.x = 0
                        char.update_rect()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    char.y += WIN_HEIGHT/LINE_SPACE
                    char.update_rect()
                    if char.y + 10 >= WIN_HEIGHT :
                        char.y = 0
                        char.update_rect()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    char.x -= WIN_WIDTH/LINE_SPACE
                    char.update_rect()
                    if char.x + 10 < 0 :
                        char.x = WIN_WIDTH - WIN_WIDTH/LINE_SPACE
                        char.update_rect()
                
                if event.key == pygame.K_SPACE:
                    PAUSE_SOUND.play()
                    pause_state = on_or_off[0]
                    on_or_off.reverse()

    main(False)

if __name__ == "__main__":
    quit = main(True)
    if quit:
        pygame.quit()
        sys.exit()

