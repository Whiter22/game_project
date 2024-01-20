import pygame as pg
import sys
import numpy as np
from button import Button
from asteroids import Asteroid
from bullet import Bullet
from player import Player

class Game:
    def __init__(self, midd, run):
        self.player = pg.sprite.GroupSingle(Player(midd))
        # self.bullets = pg.sprite.Group()
        self.asteroids = pg.sprite.Group()
        self.score = 0
        self.font = pg.font.Font('font/Pixeled.ttf', 25)
        self.is_running = run
        for _ in range(100):
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
            if pg.sprite.spritecollide(bullet, self.asteroids, True):
                self.score += 200
                bullet.kill()

        for asteroid in self.asteroids:
            if pg.sprite.spritecollide(asteroid, self.player, False):
                self.player.sprite.health -= 1
                self.score -= 300
                asteroid.kill()
                if(self.player.sprite.health == 0):
                    # print('GAME_OVER\n')
                    self.is_running = 3


    def end_point(self, midd, mouse_pos, radius):
        dist_x = mouse_pos[0] - midd[0]
        dist_y = mouse_pos[1] - midd[1]

        distance = np.sqrt(dist_x**2 + dist_y**2)

        scale = radius / distance
        return (midd[0] + dist_x * scale, midd[1] + dist_y * scale)
    

    def run(self, mouse_pos):
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


    def reset_game(self):
        self.player = pg.sprite.GroupSingle(Player(midd))
        self.asteroids = pg.sprite.Group()
        self.score = 0
        for _ in range(100):
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
                    
            if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                save_data_to_file()
                pg.quit()
                sys.exit()


def save_data_to_file() -> None:
    with open('game_info/g_info.txt', 'a+') as file:
        file.seek(0)
        lines = file.readlines()
        print(len(lines))
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
game = Game(midd, 0)
main_window = pg.display.set_mode(screen_size)

player = pg.sprite.GroupSingle(Player(midd))
bullets = pg.sprite.Group()
asteroids = pg.sprite.Group()

#MENU_SETTINGS#################################################################

BG = pg.image.load("menu_img/Background.png")
MENU_TEXT = get_font(100).render("MENU", True, "#b68f40")
MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

PLAY_BUTTON = Button(image=pg.image.load("menu_img/Play_Rect.png"), pos=(640, 250), 
                    text_input="PLAY", font=get_font(70), base_color="#d7fcd4", hovering_color="White")
OPTIONS_BUTTON = Button(image=pg.image.load("menu_img/Options_Rect.png"), pos=(640, 400), 
                    text_input="SCORE", font=get_font(70), base_color="#d7fcd4", hovering_color="White")
QUIT_BUTTON = Button(image=pg.image.load("menu_img/Quit_Rect.png"), pos=(640, 550), 
                    text_input="QUIT", font=get_font(70), base_color="#d7fcd4", hovering_color="White")

#GAME_OVER_SETTINGS##############################################################

GO_TEXT = get_font(100).render("GAME OVER", True, "#b68f40")
GO_SCORE_T = get_font(50).render(f"SCORE: {game.score}", True, "#b68f40")
GO_RECT = GO_TEXT.get_rect(center=(640, 100))
GO_SCORE_RECT = GO_SCORE_T.get_rect(center=(640, 400))

#################################################################################
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
                # with open('game_info/g_info.txt', 'a+') as file:
                #     file.seek(0)
                #     lines = file.readlines()
                #     print(len(lines))
                #     last_l = lines[-1].strip()
                #     game_number_start = last_l.find('Game_Number:') + len('Game_Number:')
                #     game_num_end = last_l.find('Points:')
                #     game_num_s = last_l[game_number_start:game_num_end].strip(' ')

                #     game_num = int(game_num_s)
                #     game_num += 1
                #     file.write(f'\nGame_Number: {game_num}\t\tPoints: {game.score}\t\tLeft_Alive: {len(game.asteroids)}\n')
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

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
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

    pg.display.update()
    clock.tick(60)  

'''
do dodania:
- zapisywanie stanu zdrowia do pliku
- QUIT pownien tez zapisywac do pliku dane //zrobione
- winning screen 
- funkcja do przycisku OPTIONS do odczytania danych z pliku ale to juz grubsza akcja bo game state bedzie kolejny do zrobienia Popoga
'''