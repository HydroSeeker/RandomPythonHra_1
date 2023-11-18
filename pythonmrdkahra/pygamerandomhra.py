import pygame
from sys import exit
from random import randint

def dislpay_score():
    current_time = int(pygame.time.get_ticks() /1000) - start_time
    sf_score = font1.render('Skero: '+str (current_time), False, ('Black'))
    sf_score_rect = sf_score.get_rect(center = (400,25))
    screen.blit(sf_score, sf_score_rect)
    return current_time

def obs_movement(obs_list):
    if obs_list:
        for obs_rect in obs_list:
            obs_rect.x -= 10

            if obs_rect.bottom == 300:
                screen.blit(sf_enemy, obs_rect)
            else:
                screen.blit(sf_enemy2, obs_rect)

        obs_list = [obstacle for obstacle in obs_list if obstacle.x > -100]
        return obs_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obs_rect in obstacles:
            if player.colliderect(obs_rect): return False
    return True

def player_animation():
    global sf_player, player_index

    if sf_player_rect.bottom < 300:
        sf_player = sf_player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        sf_player = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800,400))
screen.fill('darkgray')
pygame.display.set_caption('Curun')
clock = pygame.time.Clock()
font1 = pygame.font.Font('D:\pythonmrdky\pythonmrdkahra\8bitOperatorPlus-Bold.ttf', 30)

game_active = False
start_time = 0
score = 0

bg_music = pygame.mixer.Sound('D:/pythonmrdky/pythonmrdkahra/audio/bgmusic.ogg')
bg_music.play(loops = -1)

#objects
sf_bg = pygame.image.load('D:\pythonmrdky\pythonmrdkahra\graphics\sky.png').convert()
sf_ground = pygame.image.load('D:\pythonmrdky\pythonmrdkahra\graphics\ground.png').convert()
sf_ground_rect = sf_ground.get_rect(midbottom = (400, 400))
intro = pygame.image.load('D:\pythonmrdky\pythonmrdkahra\graphics\intro.png').convert()

#obstacles
sf_enemy11 = pygame.image.load('D:\pythonmrdky\pythonmrdkahra\graphics\enemy\enemy0.png').convert_alpha()
sf_enemy12 = pygame.image.load('D:\pythonmrdky\pythonmrdkahra\graphics\enemy\enemy1.png').convert_alpha()
sf_enemy_frame = [sf_enemy11, sf_enemy12]
sf_enemy_index = 0
sf_enemy = sf_enemy_frame[sf_enemy_index]

sf_enemy21 = pygame.image.load('D:\pythonmrdky\pythonmrdkahra\graphics\enemy2\hak0.png').convert_alpha()
sf_enemy22 = pygame.image.load('D:\pythonmrdky\pythonmrdkahra\graphics\enemy2\hak1.png').convert_alpha()
sf_enemy2_frame = [sf_enemy21, sf_enemy22]
sf_enemy2_index = 0
sf_enemy2 = sf_enemy2_frame[sf_enemy2_index]

obs_rect_list = []

#player
sf_player1 = pygame.image.load('D:\pythonmrdky\pythonmrdkahra\graphics\player\player0.png').convert_alpha()
sf_player2 = pygame.image.load('D:\pythonmrdky\pythonmrdkahra\graphics\player\player1.png').convert_alpha()
player_walk = [sf_player1,sf_player2]
player_index = 0
sf_player_jump = pygame.image.load('D:\pythonmrdky\pythonmrdkahra\graphics\player\playerjump.png').convert_alpha()

sf_player = player_walk[player_index]
sf_player_rect = sf_player.get_rect(midbottom = (100,300))
gravity = 0

#skore
current_time = int(pygame.time.get_ticks() /1000) - start_time
game_message = font1.render('Zmackni uz ten mezernik more', False, ('Black'))
game_message_rect = game_message.get_rect(center = (500,375))

#timer
obs_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obs_timer,750)

enemy_ani_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_ani_timer, 500)

enemy2_ani_timer = pygame.USEREVENT + 3
pygame.time.set_timer(enemy2_ani_timer, 400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sf_player_rect.collidepoint(mouse_pos) and sf_player_rect.bottom >= 300:
                    gravity = -20   

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and sf_player_rect.bottom >= 300:
                    gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    #sf_ground_rect.left = 0
                    start_time = int(pygame.time.get_ticks() /1000)
        if game_active:
            #if sf_ground_rect.left <= -400: sf_ground_rect.left = 0
            if event.type == obs_timer and game_active:
                if randint(0,2):
                    obs_rect_list.append(sf_enemy.get_rect(midbottom = (randint(900,1200), 300)))
                else:
                    obs_rect_list.append(sf_enemy2.get_rect(midbottom = (randint(900,1050), 195)))

            if event.type == enemy_ani_timer:
                if sf_enemy_index == 0: sf_enemy_index = 1
                else: sf_enemy_index = 0
                sf_enemy = sf_enemy_frame[sf_enemy_index]

            if event.type == enemy2_ani_timer:
                if sf_enemy2_index == 0: sf_enemy2_index = 1
                else: sf_enemy2_index = 0
                sf_enemy2 = sf_enemy2_frame[sf_enemy2_index]



    if game_active:
        screen.blit(sf_bg,(0,0))
        screen.blit(sf_ground,(0,300))
        #pygame.draw.rect(screen,'White', sf_text_rect,40)
        #screen.blit(sf_text,sf_text_rect)
        score = dislpay_score()

        sf_ground_rect.x -= 5
        if sf_ground_rect.left <= -800: sf_ground_rect.left = 0
        screen.blit(sf_ground,sf_ground_rect)

        #player
        gravity += 1
        sf_player_rect.y += gravity
        if sf_player_rect.bottom >= 300: sf_player_rect.bottom = 300
        player_animation()
        screen.blit(sf_player,sf_player_rect)

        #obstacles movement
        obs_rect_list = obs_movement(obs_rect_list)

        #enemy collision
        #if sf_enemy_rect.colliderect(sf_player_rect):
        # game_active = False
        game_active = collisions(sf_player_rect, obs_rect_list)

    else:
        obs_rect_list.clear()
        sf_player_rect.midbottom = (100,300)
        gravity = 0

        #intro screen
        screen.blit(intro,(0,0))
        score_message = font1.render('Posledni skero: ' + str(score), False, ('Black'))
        score_message_rect = score_message.get_rect(center = (500,375))
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message,score_message_rect)

    pygame.display.update() #update screen
    clock.tick(60)