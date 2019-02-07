"""
This module contains the Stage, Viewport and Background classes.
Stage: The stage is the area of the game that is currently rendered, it contains the viewport.
Viewport: The viewport is the area of the stage visible on the display surface.
Background:
"""

import pygame

class PlayerGroup(pygame.sprite.Group):
    """pygame.sprite.Group.draw() function override.
    """

    def draw(self):
        for sprite in self:
            sprite.draw()


class Viewport:
    """The viewport is the area of the stage visible on the display surface.
    """

    def __init__(self, surface=None):
        """Initialization
        
        Keyword Arguments:
            surface {pygame.Surface} -- surface in which the viewport resides (default: {pygame.display.get_surface()})
        """

        if not surface:
            surface = pygame.display.get_surface()  # if surface is not supplied, it defaults to the currently set display surface

        rect = surface.get_rect()
        self.w, self.h = rect.size  # Set width and height of the viewport
        self.x, self.y = 0, 0  # Set position of the viewport

    def setLocation(self, x, y):
        """Sets the location of the viewport (specifically, the top left corner of the viewport).
        
        Arguments:
            x {float|int} -- x coordinate
            y {float|int} -- y coordinate
        """

        self.x, self.y = x, y

    def checkObjectVisible(self, sprite):
        """Checks if (part of) a sprite is within the viewport and thus, visible on the display surface.
        
        Arguments:
            sprite {Sprite} -- the sprite to check whether is visible
        
        Returns:
            bool -- True if the sprite is visible else False
        """

        rect = sprite.rect
        hw, hh = rect.size[0] / 2, rect.size[1] / 2  # Half width and half height of the sprite
        x, y = sprite.x, sprite.y  # Position of the sprite

        if x + hw < self.x or x - hw > self.x + self.w or y - hh > self.y + self.h or y < self.y - hh:
            return False
        return True

    def centerOnXY(self, x, y):
        """Move the viewport so that it is centered on (x,y).
        Arguments:
            x {float|int} -- x coordinate
            y {float|int} -- y coordinate
        """

        self.setLocation(x - (self.w / 2), y - (self.h / 2))


class Stage:
    """The stage is the area of the game that is currently rendered, it contains the viewport.
    """

    def __init__(self, num_layers):
        self.vp = Viewport()
        self.num_layers = num_layers
        self.layers = [PlayerGroup() for _ in range(num_layers)]
        self.focus = None
        self.x = 0
        self.y = 0

    def setFocus(self, sprite):
        """Configures the stage and viewport to follow a certain sprite.
        if the parameter sprite is set to None the stage and viewport will stay static.
        
        Arguments:
            sprite {Sprite} -- the sprite to be focused on
        """

        self.focus = sprite

    def addSprite(self, sprite, layer=-1):
        """Adds a sprite to the stage.
        
        Arguments:
            sprite {Sprite} -- sprite to be added to the stage
        
        Keyword Arguments:
            layer {int} -- layer to which the sprite will be added. defaults to the frontmost layer. (default: {-1})
        
        Returns:
            Sprite -- same Sprite object as supplied to the function via 'sprite'.
                      helpful when the 'sprite' parameter is supplied by declaration when calling to this function
                      and an instance of it is desireable.
        """

        self.layers[layer].add(sprite)
        return sprite

    def do(self):
        """Goes over all sprites in all layers and updates their x and y coordinates so they appear
           in a correct position on the screen relative to the viewport's position,
           then draws the sprites by the order of the layers.
        """

        for layer in self.layers:
            for sprite in layer:
                # if self.focus == sprite: continue
                x = sprite.x - self.vp.x
                y = sprite.y - self.vp.y
                # x = sprite.x
                # y = sprite.y
                sprite.update(x, y)
                if self.vp.checkObjectVisible(sprite):
                    sprite.draw()

        if self.focus:
            # x = self.vp.w // 2
            # y = self.vp.h // 2
            # self.focus.update(x, y)
            # self.focus.draw()
            self.vp.centerOnXY(self.focus.x, self.focus.y)
