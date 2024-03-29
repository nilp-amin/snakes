#!/usr/bin/env python3
import pygame

from apple import Apple
from boundry import Boundry
from snake import Snake

from typing import Tuple

class World(object):
    ALLOWED_MOVES = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
    BACKGROUND_COLOUR = (175, 215, 70)
    GRASS_COLOUR = (167, 209, 61)
    def __init__(self, cell_number: int, cell_size: int):
        # the game screen
        self.world_surface = pygame.Surface((cell_number * cell_size, cell_number * cell_size), pygame.SCALED)
        self.cell_number = cell_number
        self.cell_size = cell_size
        
        # the apple object
        apple = Apple(cell_number, cell_size)

        # stores objects which cause collision
        self.collidable = pygame.sprite.Group(apple) 

        # stores the objects which can be eaten 
        self.edible = pygame.sprite.GroupSingle(apple)

        # the snake object
        self.snake = Snake(self.collidable, cell_number, cell_size)

        # the boundry object
        self.boundry = Boundry(self.collidable, cell_number, cell_size) 

        # current direction of the snake
        self.current_snake_direction = None

        # current score of the game
        self.score = 0
        # number of deaths
        self.deaths = 0

        # if the game is over
        self.game_over = False


    def set_direction(self, key: int) -> None:
        if key in World.ALLOWED_MOVES:
            self.current_snake_direction = key

    def get_edible_position(self) -> pygame.Vector2:
        return self.edible.sprite.get_grid_position()

    def get_snake_head_position(self) -> pygame.Vector2:
        return self.snake.get_head().get_grid_position()

    def check_for_collisions(self) -> bool:
        colliding_sprites = pygame.sprite.spritecollide(self.snake.get_head(), self.collidable, False)
        ate = False
        if colliding_sprites:
            for colliding_sprite in colliding_sprites:
                if isinstance(colliding_sprite, type(self.edible.sprite)):
                    # FIXME: add position of the score box
                    invalid_positions = set((chunk.get_grid_position().x, 
                                             chunk.get_grid_position().y) for chunk in self.snake.get_chunks())
                    colliding_sprite.set_random_position(invalid_positions)
                    ate = True
                else: # invalid collision detected
                    self.game_over = True
                    break

        return ate 

    def draw_background(self) -> None:
        # set background colour of world 
        self.world_surface.fill(World.BACKGROUND_COLOUR)

        # set alternating grass pattern
        for row in range(self.cell_number):
            for col in range(self.cell_number):
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(row * self.cell_size, col * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.world_surface, World.GRASS_COLOUR, grass_rect)

    def draw(self) -> pygame.Surface:
        self.draw_background()
        self.edible.draw(self.world_surface)
        self.snake.draw(self.world_surface)

        return self.world_surface

    def update(self) -> Tuple[int, int, bool]:
        # FIXME: this needs to be here so that when eating a food that causes
        # extension of snake to overlap itself it ends immediatly
        ate = self.check_for_collisions()

        if self.game_over:
            self.game_over = False
            self.current_snake_direction = None
            self.score = 0
            self.deaths += 1
            self.snake.reset()
            self.edible.sprite.reset()

            return self.score, self.deaths, True 

        self.snake.advance_snake(self.current_snake_direction, ate)

        self.score += int(ate)

        return self.score, self.deaths, False
