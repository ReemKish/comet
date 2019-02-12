"""
This module contains the Background, Stage and Viewport classes.
Viewport: The viewport is the area of the stage visible on the display surface.
Stage: The stage is the area of the game that is currently rendered, it contains the viewport.
Background:
"""

import pygame
from get_image import get_image


class Background:
    """Class to initiate the tile background of the game and set its tiles.
    """

    def __init__(self, color="black"):
        """Initialization.
        
        Keyword Arguments:
            color {str} -- color of the background behind the tiles (default: {"black"})
        """

        try:
            self.color = pygame.Color(color)
        except ValueError:
            self.color = pygame.Color("black")

    def setTiles(self, tiles):
        """Sets the background tiles.
        
        Arguments:
            tiles {str|list} -- either a string, a list of strings or a list of lists of strings.
                                    string - the file path to the background image
                                    list of strings - list of file paths to the background horizontal tiles
                                    list of lists - grid of the background tiles (each sublist represents a row of tiles)
        """

        if type(tiles) is str:
            self.tiles = [[get_image(tiles, False)]]
        elif type(tiles[0]) is str:
            self.tiles = [[get_image(tile, False) for tile in tiles]]
        else:
            self.tiles = [[get_image(tile, False) for tile in row] for row in tiles]
        self.tileWidth = self.tiles[0][0].get_width()
        self.tileHeight = self.tiles[0][0].get_height()


class Viewport:
    """The viewport is the area of the stage visible on the screen.
    """

    def __init__(self, surface=None):
        """Initialization.

        Keyword Arguments:
            surface {pygame.Surface} -- surface which determines the viewport's dimmentions (default: {pygame.display.get_surface()})
        """

        if not surface:
            # if surface is not supplied, it defaults to the currently set display surface
            surface = pygame.display.get_surface()

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
        # Half width and half height of the sprite
        hw, hh = rect.size[0] / 2, rect.size[1] / 2
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

    def __init__(self, num_layers, surface=None):
        """Initialization.
        
        Arguments:
            num_layers {int} -- number of layers of the stage
        
        Keyword Arguments:
            surface {pygame.Surface} -- surface in which the Stage resides (default: {pygame.display.get_surface()})
        """

        if surface:
            self.surface = surface
        else:  # if surface is not supplied, it defaults to the currently set display surface
            self.surface = pygame.display.get_surface()
        self.vp = Viewport()
        self.bg = Background()
        self.num_layers = num_layers
        self.layers = [pygame.sprite.Group() for _ in range(num_layers)]
        self.focus = None

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

    def setBackground(self, backgroundTiles):
        """Sets the background tiles. (See docstring of setTiles in the Background class).
        """

        self.bg.setTiles(backgroundTiles)

    def drawBackground(self, x, y):
        """Draws 4 background tiles around the tile vertex nearest to (x,y), ensuring that
           only tiles visible around (x,y) are drawn.
    
        Arguments:
            x {float} -- X coordinate
            y {float} -- Y coordinate
        """

        # World coordinates of the vertex closest to (x,y):
        vertex_x = round(x / self.bg.tileWidth) * self.bg.tileWidth
        vertex_y = round(y / self.bg.tileHeight) * self.bg.tileHeight

        # Index of bottom-right background tile:
        row = round(y / self.bg.tileHeight) % len(self.bg.tiles)
        col = round(x / self.bg.tileWidth) % len(self.bg.tiles[0])

        # Transform from world coordinates to screen coordinates:
        vertex_x -= self.vp.x
        vertex_y -= self.vp.y

        # Paint with background color and Blit 4 background tiles around the vertex:
        self.surface.fill(self.bg.color)
        self.surface.blit(self.bg.tiles[row][col], (vertex_x, vertex_y))
        self.surface.blit(self.bg.tiles[row-1][col], (vertex_x, vertex_y-self.bg.tileHeight))
        self.surface.blit(self.bg.tiles[row][col-1], (vertex_x-self.bg.tileWidth, vertex_y))
        self.surface.blit(self.bg.tiles[row-1][col-1], (vertex_x-self.bg.tileWidth, vertex_y-self.bg.tileHeight))

    def do(self):
        """Draws background around the focused sprite.
        Draws all visible sprites in their respective layers.
        Centralizes the viewport on the focused sprite.
        """

        if self.focus:
            self.drawBackground(self.focus.x, self.focus.y)
        else:
            self.drawBackground(self.vp.x, self.vp.y)

        for layer in self.layers:
            for sprite in layer:
                sprite.update(sprite.x, sprite.y)
                if self.vp.checkObjectVisible(sprite):
                    sprite.draw()

        if self.focus:
            self.vp.centerOnXY(self.focus.x, self.focus.y)
