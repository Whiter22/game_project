import pygame as pg
import sys
import numpy as np
from button import Button
from asteroids import Asteroid
from bullet import Bullet
from player import Player

class Game:
    def __init__(self, run):
        self.player = None
        self.bullets = None
        self.asteroids = pg.sprite.Group()
        self.score = 0
        self.font = pg.font.Font('font/Pixeled.ttf', 25)
        self.mode = False
        self.endless_count = 0
        self.is_running = run
        self.asteroids.add(Asteroid(midd, 60))


    def show_score(self):
        score_surf = self.font.render(f'SCORE: {self.score}', False, 'Red')
        score_rect = score_surf.get_rect(topleft = (midd[0] - (score_surf.get_width()/2), 0))
        main_window.blit(score_surf, score_rect)


    def show_health(self):
        health_surf = self.font.render(f'Health: {self.player.sprite.health}', False, 'Green')
        score_rect = health_surf.get_rect(topleft = (50, 0))
        main_window.blit(health_surf, score_rect)


    def detect_collision(self):
        for bullet in self.player.sprite.bullets:
            collided = pg.sprite.spritecollide(bullet, self.asteroids, True)
            if collided:
                # if self.mode == True and collided[-1].color == (0, 255, 0):
                #     self.player.sprite.health += 1
                if collided[-1].color == (255, 0, 0):
                    self.score += 400
                    self.player.sprite.health += 1
                else:
                    self.score += 200
                bullet.kill()

        for asteroid in self.asteroids:
            if pg.sprite.spritecollide(asteroid, self.player, False):
                if asteroid.color == (255, 0, 0):
                    self.player.sprite.health -= 2
                else:
                    self.player.sprite.health -= 1
                
                self.score -= 500
                asteroid.kill()
                if(self.player.sprite.health <= 0 ):
                    # print('GAME_OVER\n')
                    self.is_running = 3


    def end_point(self, midd, mouse_pos, radius):
        dist_x = mouse_pos[0] - midd[0]
        dist_y = mouse_pos[1] - midd[1]

        distance = np.sqrt(dist_x**2 + dist_y**2)

        scale = radius / distance
        return (midd[0] + dist_x * scale, midd[1] + dist_y * scale)
    

    def run(self, mouse_pos):
        global time_spawn
        end = self.end_point(midd, mouse_pos, 45)
        pg.draw.line(main_window, (255, 255, 0), midd, end, 10)

        self.show_score()
        self.show_health()
        self.player.draw(main_window)
        self.player.update(main_window)
        # bullets.draw(main_window)
        self.asteroids.draw(main_window)
        self.asteroids.update(STEP, midd)

        self.detect_collision()

        if self.mode == True:
            curr_time = pg.time.get_ticks()
            if curr_time - time_spawn >= TIME_INTERVAL:
                self.endless_count += 4
                for _ in range(self.endless_count):
                    self.asteroids.add(Asteroid(midd, 60))
                time_spawn = curr_time


    def reset_game(self):
        self.player = pg.sprite.GroupSingle(Player(midd))
        self.asteroids = pg.sprite.Group()
        self.score = 0
        if self.mode == False:
            for _ in range(100):
                self.asteroids.add(Asteroid(midd, 60))
            self.is_running = 1
        else:
            for _ in range(10):
                self.asteroids.add(Asteroid(midd, 60))
            self.is_running = 1



def get_font(size):
    return pg.font.Font("font/Pixeled.ttf", size)


def menu_wait_for_event() -> None:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                game.reset_game()
                game.is_running = 1
                    
            if SEC_MODE_BUTTON.checkForInput(MENU_MOUSE_POS):
                game.mode = True
                game.reset_game()
                game.is_running = 1

            if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                save_data_to_file()
                pg.quit()
                sys.exit()


def save_data_to_file() -> None:
    with open('game_info/g_info.txt', 'a+') as file:
        file.seek(0)
        lines = file.readlines()
        # print(len(lines))
        last_l = lines[-1].strip()
        game_number_start = last_l.find('Game_Number:') + len('Game_Number:')
        game_num_end = last_l.find('Points:')
        game_num_s = last_l[game_number_start:game_num_end].strip(' ')

        game_num = int(game_num_s)
        game_num += 1
        file.write(f'\nGame_Number: {game_num}\t\tPoints: {game.score}\t\tLeft_Alive: {len(game.asteroids)}\n')

#game_window_settings
STEP = 0.40
screen_size = (1280, 720)
midd = (screen_size[0]/2, screen_size[1]/2)

#GAME__#########################################################################################################################################
pg.init()
game = Game(0)
main_window = pg.display.set_mode(screen_size)

player = pg.sprite.GroupSingle(Player(midd))
bullets = pg.sprite.Group()
asteroids = pg.sprite.Group()

#MENU_SETTINGS#################################################################

BG = pg.image.load("menu_img/Background.png")
MENU_TEXT = get_font(100).render("MENU", True, "#b68f40")
MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
CREATORS_TEXT = get_font(10).render("Created by: Daniel Bolechowicz, Mikolaj Falkowski", True, "#b68f40")
CREATORS_RECT = CREATORS_TEXT.get_rect(center=(640, 700))

PLAY_BUTTON = Button(image=pg.image.load("menu_img/Play_Rect.png"), pos=(640, 250), 
                    text_input="PLAY", font=get_font(70), base_color="#d7fcd4", hovering_color="White")
SEC_MODE_BUTTON = Button(image=pg.image.load("menu_img/Options_Rect.png"), pos=(640, 400), 
                    text_input="ENDLESS", font=get_font(70), base_color="#d7fcd4", hovering_color="White")
QUIT_BUTTON = Button(image=pg.image.load("menu_img/Quit_Rect.png"), pos=(640, 550), 
                    text_input="QUIT", font=get_font(70), base_color="#d7fcd4", hovering_color="White")

#GAME_OVER_SETTINGS##############################################################

GO_TEXT = get_font(100).render("GAME OVER", True, "#b68f40")
GO_SCORE_T = get_font(50).render(f"SCORE: {game.score}", True, "#b68f40")
GO_RECT = GO_TEXT.get_rect(center=(640, 100))
GO_SCORE_RECT = GO_SCORE_T.get_rect(center=(640, 400))

#WINNING_SCREEN_SETTINGS##################################################################

GO_TEXT_WIN = get_font(100).render("YOU WON!", True, "#b68f40")
GO_SCORE_WIN = get_font(50).render(f"SCORE: {game.score}", True, "#b68f40")
GO_RECT_WIN = GO_TEXT_WIN.get_rect(center=(640, 100))
GO_SCORE_RECT_WIN= GO_SCORE_WIN.get_rect(center=(590, 600))

#################################################################################
# pg.mixer.music.load('music/stolen_ambient.mp3')
# pg.mixer.music.set_volume(0.5)
# pg.mixer.music.play(-1)
TIME_INTERVAL = 5000
time_spawn = 0
clock = pg.time.Clock()
while(True):
    # main_window.fill((0,0,0))

    # mouse_pos = pg.mouse.get_pos()

    if game.is_running == 1:
        main_window.fill((0,0,0))
        mouse_pos = pg.mouse.get_pos()
        game.run(mouse_pos)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                save_data_to_file()
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.player.sprite.bullets.add(Bullet(end, tuple(mouse_pos)))

        end = game.end_point(midd, mouse_pos, 45)
        pg.draw.line(main_window, (255, 255, 0), midd, end, 10)

    elif game.is_running == 0:
        main_window.blit(BG, (0,0))
        # pg.display.set_caption("menu")
        MENU_MOUSE_POS = pg.mouse.get_pos()

        main_window.blit(MENU_TEXT, MENU_RECT)
        main_window.blit(CREATORS_TEXT, CREATORS_RECT)

        for button in [PLAY_BUTTON, SEC_MODE_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(main_window)

        menu_wait_for_event()        

    else:
        main_window.blit(BG, (0,0))
        MENU_MOUSE_POS = pg.mouse.get_pos()
        GO_SCORE_T = get_font(50).render(f"SCORE: {game.score}", True, "#b68f40")
        main_window.blit(GO_TEXT, GO_RECT)
        main_window.blit(GO_SCORE_T, GO_SCORE_RECT)
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(main_window)

        menu_wait_for_event()

    if len(game.asteroids) == 0:
        main_window.blit(BG, (0,0))
        MENU_MOUSE_POS = pg.mouse.get_pos()
        GO_SCORE_WIN = get_font(50).render(f"SCORE: {game.score}", True, "#b68f40")
        main_window.blit(GO_TEXT_WIN, GO_RECT_WIN)
        main_window.blit(GO_SCORE_WIN, GO_SCORE_RECT_WIN)
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(main_window)
        
        menu_wait_for_event()

    pg.display.update()
    clock.tick(60)  

'''
do dodania:
- QUIT pownien tez zapisywac do pliku dane //zrobione
- winning screen //zrobione
'''