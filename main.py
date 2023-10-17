import pygame
from sys import exit
import math
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load("sprites/dinosaur/dino2.png").convert_alpha()
        player_walk2 = pygame.image.load("sprites/dinosaur/dino3.png").convert_alpha()
        self.player_jump = pygame.image.load("sprites/dinosaur/dino1.png").convert_alpha()
        player_duck1_surface = pygame.image.load("sprites/dinosaur/dinoduck1.png").convert_alpha()
        player_duck2_surface = pygame.image.load("sprites/dinosaur/dinoduck2.png").convert_alpha()

        self.player_duck_list = [player_duck1_surface, player_duck2_surface]
        self.player_duck_index = 0
        self.player_walk_list = [player_walk1, player_walk2]
        self.player_walk_index = 0
        self.image = self.player_walk_list[self.player_walk_index]
        self.rect = self.image.get_rect(midbottom = (200, 315))
        self.player_gravity = 0
        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
    
    def apply_gravity(self):
        self.player_gravity += 1
        self.rect.y += self.player_gravity
        if self.rect.bottom >= 315:
            self.rect.bottom = 315
    
    def jump(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 315:
            self.player_gravity = -18
            self.jump_sound.play()
    
    def animate(self):
        keys = pygame.key.get_pressed()
        if self.rect.bottom < 315:
            self.image = self.player_jump
        else:
            if keys[pygame.K_DOWN]:
                self.player_duck_index += 0.1
                if self.player_duck_index >= len(self.player_duck_list):
                    self.player_duck_index = 0
                self.image = self.player_duck_list[int(self.player_duck_index)]
                self.rect = self.image.get_rect(midbottom = (200, 315))
            else:
                self.player_walk_index += 0.1
                if self.player_walk_index >= len(self.player_walk_list):
                    self.player_walk_index = 0
                self.image = self.player_walk_list[int(self.player_walk_index)]
                self.rect = self.image.get_rect(midbottom = (200, 315))

    def down_button(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.player_gravity += 10

    def update(self):
        self.apply_gravity()
        self.jump()
        self.animate()
        self.down_button()

# obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type

        # selecting type of obstacle to spawn in based on the random number variable "type"
        if type < 4:
            self.image = pygame.image.load("sprites/cactus/bigcactus1.png")
            self.rect = self.image.get_rect(midbottom = (randint(800, 1000), 315 ))
        elif type < 7 and type > 3:
            self.image = pygame.image.load("sprites/cactus/bigcactus2.png")
            self.rect = self.image.get_rect(midbottom = (randint(800, 1000), 315))
        elif type < 10 and type > 6:
            self.image = pygame.image.load("sprites/cactus/bigcactus3.png")
            self.rect = self.image.get_rect(midbottom = (randint(800, 1000), 315))
        elif type == 10:
            self.image = pygame.image.load("sprites/cactus/cactusbunch.png")
            self.rect = self.image.get_rect(midbottom = (randint(800, 1000), 315))
        elif type > 10 and type < 14:
            pterosaur1_surface = pygame.image.load("sprites/pterosaur/pterosaur1.png").convert_alpha()
            pterosaur2_surface = pygame.image.load("sprites/pterosaur/pterosaur2.png").convert_alpha()
            self.pterosaur_list = [pterosaur1_surface, pterosaur2_surface]
            self.pterosaur_index = 0
            self.image = self.pterosaur_list[self.pterosaur_index]
            self.rect = self.image.get_rect(midbottom = (randint(800, 1000), 250)) # y= 280

    def animate_pterosaur(self):
        # increases the index by 0.1 every iteration, typecasts index to int and selects surface according to index
        # also sets index back to zero if it goes out of range
        if self.type > 10 and self.type < 14:
            self.pterosaur_index += 0.1
            if self.pterosaur_index >= len(self.pterosaur_list):
                self.pterosaur_index = 0
            self.image = self.pterosaur_list[int(self.pterosaur_index)]

    def remove_leftovers(self):
        # removes unwanted obstacle sprites to the left of the screen
        if self.rect.x < -100:
            self.kill()
    
    def update(self):
        # calls all member functions in one function for code consolidation
        self.animate_pterosaur()
        self.remove_leftovers()
        self.rect.x -= 7
# initialising pygame
pygame.init()

# score displayer
def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score = round(current_time/85)
    score_surface = score_font.render(f"Score: {score}", False, "Black")
    score_rect = score_surface.get_rect(midbottom = (300, 50))
    high_score_surface = score_font.render(f"High Score: {high_score}", False, "Black")
    high_score_rect = high_score_surface.get_rect(midbottom = (300, 70))
    screen.blit(score_surface, score_rect)
    screen.blit(high_score_surface, high_score_rect)
    return score
score = 0
start_time = 0

player_diesound = pygame.mixer.Sound("audio/die.mp3")
# detecting colissions between player and obstacle sprites
def detect_collission():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        player_diesound.play()
        obstacle_group.empty()
        return False
    else:
        return True
    
def cloud_movement():
    if cloud_list:
        for cloud in cloud_list:
            cloud.left -= randint(1, 3)
            screen.blit(cloud_surface, cloud)
            if cloud.left <= -100:
                cloud_list.remove(cloud)

        return cloud_list
    else:
        return []

score_list = []
high_score = 0
def highscore(score):
    score_list.append(score)
    high_score = max(score_list)
    return high_score

# making the screen
screen = pygame.display.set_mode((600, 400))

# window title
pygame.display.set_caption("Dinosaur Game")

# setting icon
icon = pygame.image.load("sprites/other/icon.png").convert_alpha()
pygame.display.set_icon(icon)

# game clock
clock = pygame.time.Clock()

# regular surfaces to put on display surface
bg_surface = pygame.Surface((600, 400))
bg_surface.fill("white")

# player group
player = pygame.sprite.GroupSingle()
player.add(Player())

# obstacle group
obstacle_group = pygame.sprite.Group()

# ground surface
ground_surface = pygame.image.load("sprites/other/ground1.png").convert()
ground_rect = ground_surface.get_rect(bottomleft = (0, 330))

# cloud surface
cloud_surface = pygame.image.load("sprites/other/cloud.png")
# cloud_rect = cloud_surface.get_rect(midbottom = (randint(800, 1000), 100))

# game title surface
title_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 20) # main font for the game
score_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 15)
title_surface = title_font.render("Dinosaur Game", False, "Black")
title_rect = title_surface.get_rect(midbottom = (300, 50))
title_rect_width = math.dist(title_rect.bottomright, title_rect.bottomleft)
title_outline_rect = pygame.Rect(title_rect.left-10, title_rect.top - 10, 278, 35)

# scaled player surface for game over screen
player_gameover = pygame.image.load("sprites/dinosaur/dino4.png").convert_alpha()
player_gameover_scaled = pygame.transform.rotozoom(player_gameover, 0, 2.5)
player_gameover_rect = player_gameover_scaled.get_rect(center = (300, 200))

# game over
game_running = False

# cactus timer
obsctale_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obsctale_timer, 1000)
cactus_list = []

# cloud timer
cloud_timer = pygame.USEREVENT + 2
pygame.time.set_timer(cloud_timer, randint(6000, 8000))
cloud_list = []

while True:
    # event loop
    for event in pygame.event.get():
        # checking for player clicking on x button
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # spawning obstacle only when game is running
        if game_running:
            # spawning an obstacle every 1000 miliseconds / 1 second
            if event.type == obsctale_timer:
                type = randint(1, 13)
                obstacle_group.add(Obstacle(type))
            
            if event.type == cloud_timer:
                cloud_list.append(cloud_surface.get_rect(midbottom = (randint(800, 1000), randint(100, 200))))
            
        # starting game again when game is over, displaying score
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_running = True
                    start_time = pygame.time.get_ticks()
                    high_score = highscore(score)

    if game_running:
        # placing main surfaces
        screen.blit(bg_surface, (0,0))

        # ground blitting and moving
        ground_rect.left -= 7
        screen.blit(ground_surface, ground_rect)
        if ground_rect.right < 600:
            ground_rect.left = 0

        score = display_score()
        cloud_movement()

        # drawing player and obstacles and calling respective functions
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        # collision detection with cactus
        game_running = detect_collission()

    else:
        screen.fill("white")    # clearing full bg in game_running state
        screen.blit(title_surface, title_rect)    # adding game name
        cloud_list.clear() 
        if score > 0:
            score_surface = title_font.render(f"Your Score: {score}", False, "black")    # making and adding final score
            score_rect = score_surface.get_rect(midbottom = (300, 350))
            screen.blit(score_surface, score_rect)
        if score == 0:
            score_surface = title_font.render(f"Press SPACE or", False, "black")    # making and adding final score
            score_rect = score_surface.get_rect(midbottom = (300, 350))
            screen.blit(score_surface, score_rect)
            score_surface1 = title_font.render(f"Left-Click to start", False, "black")    # making and adding final score
            score1_rect = score_surface1.get_rect(midbottom = (300, 380))
            screen.blit(score_surface1, score1_rect)
        pygame.draw.rect(screen, "#525252", title_outline_rect, width = 4)
        screen.blit(player_gameover_scaled, player_gameover_rect)    # adding dead player surface
    
    pygame.display.update()
    clock.tick(60)    # setting max framerate for the game