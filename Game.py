#!py -3

# ----------------------------------------------------- Imports ------------------------------------------------------ #
import pygame
import math
import sys
import os
import random

import sprites
from stage import Viewport, Stage, Background
from get_image import get_image


# ----------------------------------------------------- Classes ------------------------------------------------------ #
class Sprite(pygame.sprite.Sprite):
    """Base class for all sprites in the game.
    """

    def __init__(self, skins, animation_fps, x, y):
        """Initialization.
        
        Arguments:
            skins {list} -- the list of the sprite's skins - taken from 'sprites.py' module
            animation_fps {int} -- pace (in frames per second) of the  player's skin animation
            x {float|int} -- sprites's X-coordinate position
            y {float|int} -- sprite's Y-coordinate position
        """

        pygame.sprite.Sprite.__init__(self)

        self.skins = skins
        self.skin = get_image(skins[0])  # Current sprite's skin
        self.skin_i = 0  # Index of the current sprite's skin in self.skins
        self.animation_fps = animation_fps
        self.rect = self.skin.get_rect()  # Used in pygame.sprite class to detect collision
        self.x = x  # Sprite's X-coordinate position
        self.y = y  # Sprite's Y-coordinate position
        self.direction = 0  # Sprite's facing direction in degrees

    def draw(self):
        """Draws the sprite on the display according to its position and direction.
        """
        self.skin = get_image(self.skins[self.skin_i])
        rotated = pygame.transform.rotate(self.skin, self.direction)
        rect = rotated.get_rect()
        gameDisplay.blit(rotated, (self.x - stage.vp.x -
                                   rect.center[0], self.y - stage.vp.y - rect.center[1]))


class Player(Sprite):
    """A player object is a player shown on screen and is controlled by the user.
    """

    def __init__(self, skins, animation_fps=8, x=0, y=0,
                 speed_factor=1.2, keys=(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE)):
        """Initialization.
        
        Arguments:
            skins {list} -- The list of the sprite's skins - taken from 'sprites.py' module
        
        Keyword Arguments:
            animation_fps {int} -- Pace (in frames per second) of the  player's skin animation (default: {8})
            x {int|float} -- sprites's x-coordinate (default: {0})
            y {int|float} -- sprite's y-coordinate (default: {0})
            speed_factor {int|float} -- the higher the speed factor, the faster the player moves (default: {1.2})
            keys {tuple} -- A tuple that contains the keys that update the player's actions in the following order:
                     ([Thrust], [TurnLeft], [TurnRight], [Shoot]) 
                     (default: {(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE)})
        """

        Sprite.__init__(self, skins, animation_fps, x, y)
        self.speed = 0
        self.speed_factor = speed_factor
        self.keys = keys
        self.velocity = 0  # Main factor in the calculation of player's speed

        # controls: A dictionary that maps each key to the player's actions associated with it
        self.controls = {keys[0]: self.Thrust,
                         keys[1]: self.TurnLeft,
                         keys[2]: self.Reverse,
                         keys[3]: self.TurnRight,
                         keys[4]: self.Shoot}

    def update(self, x, y):
        self.iter_image()
        keys_states = pygame.key.get_pressed()
        for key, state in enumerate(keys_states):
            if state and (key in self.keys):
                self.controls[key]()
        if not keys_states[self.keys[0]] and not keys_states[self.keys[2]] and self.speed != 0:
            self.Pull()
        self.Move(x, y)

    def iter_image(self):
        if current_frame % (FPS // self.animation_fps) == 0:
            if 1 <= self.skin_i <= 5:
                self.skin_i = self.skin_i % 5 + 1
            elif 6 <= self.skin_i <= 9:
                self.skin_i = (self.skin_i + 1) % 9

    def handle_key_event(self, event, key):
        action = self.controls[key]
        if event == pygame.KEYDOWN:
            action()
        elif event == pygame.KEYUP:
            action()

    def Move(self, x, y):
        self.speed = 2 ** ((self.velocity+20)/10-1) - 2
        direction_radians = math.pi * self.direction / 180
        dx = math.cos(direction_radians) * self.speed * self.speed_factor
        dy = math.sin(direction_radians) * self.speed * self.speed_factor
        self.x = x + dx
        self.y = y - dy
        self.rect.x = self.x - self.rect.size[0] / 2
        self.rect.y = self.y - self.rect.size[1] / 2

    def Pull(self):
        if self.velocity > 0:
            self.velocity -= min(0.325, self.velocity)
        elif self.velocity < 0:
            self.velocity += min(1, abs(self.velocity))

    def Ignite(self):
        self.skin_i = 1

    def Extinguish(self):
        self.skin_i = 6

    def Thrust(self):
        if self.velocity < 17:
            self.velocity += 0.5

    def TurnLeft(self):
        self.direction += 3 + self.speed / 14.0
        self.direction %= 360

    def Reverse(self):
        if self.velocity > -30:
            self.velocity -= 0.5

    def TurnRight(self):
        self.direction -= 3 + self.speed / 14.0
        self.direction %= 360

    def Shoot(self):
        pass


# ---------------------------------------------------- Functions ----------------------------------------------------- #
def HandleEvents():
    """Handle program events (e.g. keypresses, closing of the window)
    """

    global player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            elif event.key == player.keys[0]:
                player.Ignite()
            elif event.key == pygame.K_SPACE:
                stage.setFocus(player2 if stage.focus == player else player)
        elif event.type == pygame.KEYUP:
            if event.key == player.keys[0]:
                player.Extinguish()


# ---------------------------------------------------- Game Loop ----------------------------------------------------- #
def gameLoop():
    global player
    global current_frame
    while True:
        HandleEvents()
        stage.do()
        # Display FPS and the focused sprite's coordinates
        fps = clock.get_fps()
        gameDisplay.blit(font.render("%.1f" % fps, True,
                                     pygame.Color('orange')), (0, 0))
        gameDisplay.blit(font.render("%.2f, %.2f" % (
            stage.focus.x, stage.focus.y), True, pygame.Color('white')), (0, 30))
        # Cap FPS
        clock.tick(FPS)
        current_frame = (current_frame + 1) % 30
        pygame.display.update()


# ------------------------------------------------------- Main ------------------------------------------------------- #
def main():
    global FPS
    global white, black, red, green, blue, space  # Colors
    global gameDisplay
    global clock
    global stage
    global player, player2
    global current_frame
    global font

    # Framerate variables:
    FPS = 60
    clock = pygame.time.Clock()
    current_frame = 0

    # Initialize display:
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    # gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)  # Run fullscreen
    gameDisplay = pygame.display.set_mode((0, 0), pygame.NOFRAME)  # Run borderless windowed
    pygame.mouse.set_visible(False)
    pygame.display.set_caption('GunGame')
    font = pygame.font.Font(None, 30)

    # Initialize the stage and add sprites:
    stage = Stage(2)  # 2 layers
    player = stage.addSprite(Player(sprites.spaceship1, x=500, y=500))
    player2 = stage.addSprite(Player(sprites.spaceship2, 8, y=64, keys=(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_SPACE)))
    stage.setFocus(player)
    stage.setBackground([["textures\\background\\debug00.png","textures\\background\\debug10.png","textures\\background\\debug20.png"],
                         ["textures\\background\\debug01.png","textures\\background\\debug11.png","textures\\background\\debug21.png"],
                         ["textures\\background\\debug02.png","textures\\background\\debug12.png","textures\\background\\debug22.png"]])

    # End of initialization
    gameLoop()


if __name__ == "__main__":
    main()
