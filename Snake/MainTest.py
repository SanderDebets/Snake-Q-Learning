import pygame
import random
import sys

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720

GRIDSIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE

UP = (0, -1)  # why is up -1 and down 1??
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class QlearningAgent:
    def __init__(self):
        self.stored_positions = []
        self.actions = ["up", "down", "left", "right"]

    def store_positions(self, food_position, snake_positions):
        combined = [food_position, snake_positions]
        # print(combined in self.stored_positions)
        print(combined)
        print(self.stored_positions)
        print("--------------")
        self.stored_positions.append(combined)

    def choose_action(self):
        return random.choice(self.actions)


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(int(GRID_WIDTH / 2), int(GRID_WIDTH / 2))]  # placing the snake in the middle of the screen
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])  # on initialization, a random direction is chosen
        self.color = (17, 24, 47)

    def get_head_position(self):
        return self.positions[0]

    def turn(self, direction):
        if self.length > 1 and (
                direction[0] * -1, direction[1] * -1) == self.direction:  # prevent the snake from going backwards
            return
        else:
            self.direction = direction

    def move(self, new_head_position):
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:  # is this if statement needed
            self.positions.pop()

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


class Food:
    def __init__(self):
        self.position = (random.randint(0, int(GRID_WIDTH) - 1), random.randint(0, int(GRID_HEIGHT) - 1))
        self.color = (223, 163, 49)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    snake = Snake()
    food = Food()
    agent = QlearningAgent()

    for i in range(1, 20):
        random_food_position = (random.randrange(1, 30), random.randrange(1, 30))
        random_snake_position = (random.randrange(1, 30), random.randrange(1, 30))
        agent.store_positions(random_food_position, random_snake_position)

    # while True:
    #     clock.tick(10)
    # #     next_action = random.choice(["up", "down", "left", "right"])
    # #     dir_x = 0
    # #     dir_y = 0
    # #     if next_action == "up":
    # #         dir_x = 0
    # #         dir_y = -1
    # #     elif next_action == "down":
    # #         dir_x = 0
    # #         dir_y = 1
    # #     elif next_action == "left":
    # #         dir_x = -1
    # #         dir_y = 0
    # #     elif next_action == "right":
    # #         dir_x = 1
    # #         dir_y = 0
    # #     head_position = snake.get_head_position()
    # #     new_head_position = (head_position[0] + dir_x, head_position[1] + dir_y)
    # #     snake.move(new_head_position)
    # #     agent.store_positions(food.position, snake.positions)
    #
    #     next_action = agent.choose_action()
    #     snake.handle_AI_action(next_action)
    #     head_position = snake.get_head_position()
    #     dir_x, dir_y = snake.direction
    #     new_head_position = (head_position[0] + dir_x, head_position[1] + dir_y)
    #     snake.move(new_head_position)
    #     agent.store_positions(food.position, snake.positions)


main()
