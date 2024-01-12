import pygame as pg
import sys
import numpy as np
from asteroids import Asteroid
from bullet import Bullet
from player import Player

class Game:
    def __init__(self, midd):
        self.player = pg.sprite.GroupSingle(Player(midd))
        # self.bullets = pg.sprite.Group()
        self.asteroids = pg.sprite.Group()
        self.score = 0
        self.font = pg.font.Font('font/Pixeled.ttf', 25)
        for _ in range(18):
            self.asteroids.add(Asteroid(midd, 60))


    def show_score(self):
        score_surf = self.font.render(f'SCORE: {self.score}', False, 'Red')
        score_rect = score_surf.get_rect(topleft = (midd[0] - (score_surf.get_width()/2), 0))
        main_window.blit(score_surf, score_rect)


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
                    print('GAME_OVER\n')


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
        self.player.draw(main_window)
        self.player.update(main_window)
        # bullets.draw(main_window)
        self.asteroids.draw(main_window)
        self.asteroids.update(STEP, midd)

        self.detect_collision()


# def end_point(midd, mouse_pos, radius):
#     dist_x = mouse_pos[0] - midd[0]
#     dist_y = mouse_pos[1] - midd[1]

#     distance = np.sqrt(dist_x**2 + dist_y**2)

#     scale = radius / distance
#     return (midd[0] + dist_x * scale, midd[1] + dist_y * scale)


STEP = 0.50
screen_size = (800, 640)
midd = (screen_size[0]/2, screen_size[1]/2)

#GAME__#########################################################################################################################################
pg.init()
main_window = pg.display.set_mode(screen_size)
# text_font = pg.font.Font()
# text_surf = text_font.render('GAME OVER', False, '')

player = pg.sprite.GroupSingle(Player(midd))
bullets = pg.sprite.Group()
asteroids = pg.sprite.Group()
for _ in range(18):
    asteroids.add(Asteroid(midd, 60))

# g_over = False
game = Game(midd)
clock = pg.time.Clock()
while(True):
    main_window.fill((0,0,0))

    mouse_pos = pg.mouse.get_pos()
    game.run(mouse_pos)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
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
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                game.player.sprite.bullets.add(Bullet(end, tuple(mouse_pos)))
    # mouse_pos = pg.mouse.get_pos()
    # game.run(mouse_pos)

    end = game.end_point(midd, mouse_pos, 45)
    pg.draw.line(main_window, (255, 255, 0), midd, end, 10)


    # player.draw(main_window)

    # mouse_pos = pg.mouse.get_pos()
    # end = end_point(midd, mouse_pos, 45)
    # pg.draw.line(main_window, (255, 255, 0), midd, end, 10)
    
    # for event in pg.event.get():
    #     if event.type == pg.QUIT:
    #         pg.quit()
    #         sys.exit()
    #     if event.type == pg.MOUSEBUTTONDOWN:
    #         if event.button == 1:
    #             bullets.add(Bullet(end, tuple(mouse_pos)))

    # bullets.draw(main_window)
    # bullets.update()

    # asteroids.draw(main_window)
    # asteroids.update(STEP, midd)

    # for bullet in bullets:
    #     if pg.sprite.spritecollide(bullet, asteroids, True):
    #         bullet.kill()

    # for asteroid in asteroids:
    #     if pg.sprite.spritecollide(asteroid, player, False):
    #         player.sprite.health -= 1
    #         asteroid.kill()
    #         if(player.sprite.health == 0):
    #             g_over = True
    #             break

    # if g_over:
    #     break

    pg.display.update()
    clock.tick(60)  


# print("GAME OVER")