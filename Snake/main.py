import pygame
import sys
import random
import numpy as np

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720

GRIDSIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE

UP = (0, -1)  # why is up -1 and down 1??
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def drawGrid(surface):
    for x in range(0, int(GRID_WIDTH)):
        for y in range(0, int(GRID_HEIGHT)):
            rect = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
            if (x + y) % 2 == 0:  # creating a checker board pattern
                pygame.draw.rect(surface, (93, 216, 228), rect)
            else:
                pygame.draw.rect(surface, (84, 194, 205), rect)


class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [(int(GRID_WIDTH / 2), int(GRID_WIDTH / 2))]  # placing the snake in the middle of the screen
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])  # on initialization, a random direction is chosen
        self.color = (17, 24, 47)

    def get_head_position(self):
        return self.positions[0]

    def move(self, new_head_position):

        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:  # is this if statement needed
            self.positions.pop()

    def turn(self, direction):
        if self.length > 1 and (direction[0] * -1, direction[1] * -1) == self.direction:  # prevent the snake from going backwards
            return
        else:
            self.direction = direction

    def draw(self, surface):
        for part in self.positions:
            rect = pygame.Rect((part[0] * GRIDSIZE, part[1] * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, rect)  # drawing snake part
            #pygame.draw.rect(surface, (93, 216, 228), rect, 1)  # not sure what this line does

    def reset(self):
        self.length = 1
        self.positions = [(int(GRID_WIDTH / 2), int(GRID_WIDTH / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

    def handle_AI_action(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if action == "up":
            self.turn(UP)
        elif action == "down":
            self.turn(DOWN)
        elif action == "left":
            self.turn(RIGHT)
        elif action == "right":
            self.turn(RIGHT)

class Food(object):
    def __init__(self):
        self.position = (random.randint(0, int(GRID_WIDTH) - 1), random.randint(0, int(GRID_HEIGHT) - 1))
        self.color = (223, 163, 49)

    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRIDSIZE, self.position[1] * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, rect)  # drawing food
        pygame.draw.rect(surface, (93, 216, 228), rect, 1)  # not sure what this line does

    def randomize_position(self, snake):  #
        new_position = (random.randint(0, int(GRID_WIDTH) - 1), random.randint(0, int(GRID_HEIGHT) - 1))
        while new_position in snake.positions:
            new_position = (random.randint(0, int(GRID_WIDTH) - 1), random.randint(0, int(GRID_HEIGHT) - 1))
        self.position = new_position

class QlearningAgent():
    def __init__(self):
        self.actions = ["up", "down", "left", "right", "nothing"]
        self.currentAction = random.choice(self.actions)
        self.score = 0

    def chooseAction(self):
        self.currentAction = random.choice(self.actions)  # right now we just choose a random action, here we should implement the q learning algorithm


def main():
    pygame.init()
    mode = "Qlearning"  # determines what mode the game is in. It can be either "Qlearning" or "Human-Controlled"
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(window.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food()
    agent = QlearningAgent()

    while True:
        clock.tick(10)
        drawGrid(surface)
        if mode == "Human-Controlled":
            snake.handle_keys()
        elif mode == "Qlearning":
            agent.chooseAction()
            snake.handle_AI_action(agent.currentAction)
        head_position = snake.get_head_position()
        dir_x, dir_y = snake.direction
        new_head_position = (head_position[0] + dir_x, head_position[1] + dir_y)
        if new_head_position[0] >= GRID_WIDTH or new_head_position[0] < 0 or new_head_position[1] >= GRID_HEIGHT or new_head_position[1] < 0:
            snake.reset()
            agent.score -= 50
        elif snake.length > 2 and new_head_position in snake.positions[1:]:  # originally this was self.positions[2:]
            snake.reset()
            agent.score -= 50
        else:
            snake.move(new_head_position)
        if snake.get_head_position() == food.position:
            snake.length += 1
            agent.score += 1
            food.randomize_position(snake)
        snake.draw(surface)
        food.draw(surface)
        window.blit(surface, (0, 0))
        pygame.display.update()


if __name__ == "__main__":
    main()
