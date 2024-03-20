import pygame
from sys import exit
from random import randint, choice

width = 800
height = 400


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

        self.player_gravity = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(100, 300))

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def player_animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= 2:
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "snail":
            self.frames = [pygame.image.load("graphics/snail/snail1.png").convert_alpha(),
                           pygame.image.load("graphics/snail/snail2.png").convert_alpha()]
            y_pos = 300
        else:
            self.frames = [pygame.image.load("graphics/Fly/Fly1.png").convert_alpha(),
                           pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()]
            y_pos = 200
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.frame_index += 0.1
        if self.frame_index >= 2:
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()


def display_score():
    time = pygame.time.get_ticks() - start_time
    score_surface = test_font.render("Score: " + str(time // 1000), False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(width // 2, 50))
    screen.blit(score_surface, score_rect)
    return time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstactle_group, False):
        obstactle_group.empty()
        return True
    return False


blue = (94, 128, 163)
pygame.init()
start_time = 0
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False

sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

player = pygame.sprite.GroupSingle()
player.add(Player())
obstactle_group = pygame.sprite.Group()
score = 0
bg_Music = pygame.mixer.Sound("audio/music.wav")
bg_Music.set_volume(0.1)
bg_Music.play(loops=-1)

# Intro Screen
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# Timer
obstactle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstactle_timer, 1400)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

k = -2
while True:
    for event in pygame.event.get():
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstactle_timer:
                obstactle_group.add(Obstacle(choice(["snail", "fly"])))
        if not game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = pygame.time.get_ticks()

    if game_active:
        screen.fill((0, 0, 0))
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, sky_surface.get_height()))
        score = display_score()

        player.draw(screen)
        player.update()
        obstactle_group.draw(screen)
        obstactle_group.update()

        game_active = not collision_sprite()
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        x, y = player_stand_rect.midbottom
        y += 20
        if score == 0:
            instruction_surface = test_font.render("Press [Space] to Start", False, (255, 255, 255))
            instruction_rect = instruction_surface.get_rect(midtop=(x, y))
            screen.blit(instruction_surface, instruction_rect)
        else:
            score_surface = test_font.render("Score: " + str(score // 1000), False, (255, 255, 255))
            score_rect = score_surface.get_rect(midtop=(x, y))
            screen.blit(score_surface, score_rect)

        title_surface = pygame.transform.scale2x(test_font.render("The Runner", False, (255, 255, 255)))
        title_rect = title_surface.get_rect(center=(400, 80))
        screen.blit(title_surface, title_rect)

    pygame.display.update()
    clock.tick(60)
