import pygame
import sys
import os

pygame.init()

# set window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 6 / 8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# set caption
pygame.display.set_caption('Maligone: Origin')

# define colours
GREEN = (100, 150, 100)
BLACK = (0, 0, 0)
WHITE = (225, 225, 225)
#set frame rate
clock = pygame.time.Clock()
FPS = 60

#game action vaiables
moving_left = False
moving_right = False
jump = False

#human class'
class human(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.scale = scale
        self.speed = speed
        self.animation_list = []
        self.action = 0
        self.frame_index = 0
        self.direction = 1
        self.flip = False
        self.update_time = pygame.time.get_ticks()
        self.in_air = False

        #importing frames
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            #list for frames in animation
            temp_list = []
            #get number of frames in animation
            num_of_frames = len(os.listdir(f'data/img/{self.char_type}/{animation}'))
            for frame in range(num_of_frames):
                img = pygame.image.load(f'data/img/{self.char_type}/{animation}/{frame}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(screen.get_height()*scale), int(screen.get_height()*scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        #initializing
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # update_animation
        ANIMATION_COOLDOWN = 100
        #pdate image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check time for next frame
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #reset
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def move(self, moving_left, moving_right):
        #moving variables
        dx = 0
        dy = 0

        # check if moving 
        if moving_right:
            dx = self.speed
            self.direction = 1
            self.flip = False
        if moving_left:
            dx = -self.speed
            self.direction = -1
            self.flip = True


        #update pos
        self.rect.x += dx
        self.rect.y += dy





    def update_action(self, action):
        if self.action != action:
            self.action = action
            #reset animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)



#create player instance
player = human("player", 300, 300, 0.1, 5)

run = True

while run:
    screen.fill(GREEN)

    #draw characters
    player.draw()
    player.update()

    if player.in_air:
        player.update_action(2)#2 = jump
    elif moving_left or moving_right:
        player.update_action(1)#1 = run
    else:
        player.update_action(0)#0 = idle
    player.move(moving_left, moving_right)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # run = False
            pygame.quit()
            sys.exit()
        #keybord press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_r:
                granade = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
   
        
        #keyboard relese
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_r:
                granade = False
                granade_thrown = False

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
