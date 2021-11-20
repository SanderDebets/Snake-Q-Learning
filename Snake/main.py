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
        # self.positions.insert(0, new_head_position)
        self.positions = [new_head_position] + self.positions

        if len(self.positions) > self.length:  # is this if statement needed
            self.positions.pop()


    def turn(self, direction):
        if self.length > 1 and (
        direction[0] * -1, direction[1] * -1) == self.direction:  # prevent the snake from going backwards
            return
        else:
            self.direction = direction

    def draw(self, surface):
        for part in self.positions:
            rect = pygame.Rect((part[0] * GRIDSIZE, part[1] * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, rect)  # drawing snake part
            # pygame.draw.rect(surface, (93, 216, 228), rect, 1)  # not sure what this line does

    def reset(self):
        self.length = 1
        self.positions = [(int(GRID_WIDTH / 2), int(GRID_WIDTH / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def handle_keys(self):
        for event in pygame.event.get():
            print("test")
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print("omhoog")
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    print("omlaag")
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    print("links")
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    print("rechts")
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
            self.turn(LEFT)
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



class QlearningAgent:
    def __init__(self):
        self.actions = ["up", "down", "left", "right"]
        self.currentAction = random.choice(self.actions)
        self.score = 0
        self.stored_positions = []
        self.left_rewards = []
        self.right_rewards = []
        self.up_rewards = []
        self.down_rewards = []
        self.rewards = [["left", 0, "right", 0, "down", 0, "up", 0]]
        self.current_state_index = 0
        self.append = True
        self.epsilon = 0.9

    def choose_action(self):
        if np.random.random() < self.epsilon:  # use the q learning algoritm
            options = [self.rewards[self.current_state_index][1], self.rewards[self.current_state_index][3],
                       self.rewards[self.current_state_index][5], self.rewards[self.current_state_index][7]]
            choice = np.argmax(options)
            self.currentAction = self.actions[choice]
        else:  # sometimes we choose randomly, this is to promote exploration
            self.currentAction = random.choice(self.actions)



    def store_positions(self, food_position, snake_positions):
        combined = [food_position, snake_positions]
        # print(combined in self.stored_positions)
        # print(combined)

        if combined in self.stored_positions:
            # this state has been seen before, find its index
            self.current_state_index = self.stored_positions.index(combined)
            self.append = False
        else:
            # this state hasn't been seen before, add it to the list
            self.current_state_index = len(self.stored_positions) # this line is probably not needed
            self.stored_positions.append([food_position, snake_positions])
            self.append = True

    def store_rewards(self, reward: int):
        if self.append:
            if self.currentAction == "left":
                self.rewards.append(["left", reward, "right", 0, "down", 0, "up", 0])
            elif self.currentAction == "right":
                self.rewards.append(["left", 0, "right", reward, "down", 0, "up", 0])
            elif self.currentAction == "down":
                self.rewards.append(["left", 0, "right", 0, "down", reward, "up", 0])
            elif self.currentAction == "up":
                self.rewards.append(["left", 0, "right", 0, "down", 0, "up", reward])
        elif not self.append:
            if self.currentAction == "left":
                self.rewards[self.current_state_index][1] += reward
            elif self.currentAction == "right":
                self.rewards[self.current_state_index][3] += reward
            elif self.currentAction == "down":
                self.rewards[self.current_state_index][5] += reward
            elif self.currentAction == "up":
                self.rewards[self.current_state_index][7] += reward






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
        clock.tick(14400)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        drawGrid(surface)
        if mode == "Human-Controlled":  # currently broken, pygame doesnt want to detect keys
            snake.handle_keys()
        elif mode == "Qlearning":
            # print(snake.positions)
            agent.store_positions(food.position, snake.positions)
            agent.choose_action()
            snake.handle_AI_action(agent.currentAction)
        head_position = snake.get_head_position()
        dir_x, dir_y = snake.direction
        new_head_position = (head_position[0] + dir_x, head_position[1] + dir_y)
        if new_head_position[0] >= GRID_WIDTH or new_head_position[0] < 0 or new_head_position[1] >= GRID_HEIGHT or \
                new_head_position[1] < 0:
            # snake goes outside border, the chosen action gets a -100 penalty
            snake.reset()
            agent.store_rewards(-100)
        elif snake.length > 2 and new_head_position in snake.positions[1:]:  # originally this was self.positions[2:]
            # snake crashes into itself, the chosen action gets a -100 penalty
            snake.reset()
            agent.store_rewards(-100)
        else:
            snake.move(new_head_position)
            if snake.get_head_position() == food.position:
                # the chosen action gets a +1 reward
                snake.length += 1
                agent.store_rewards(1)
                food.randomize_position(snake)
            else:
                # the snake survived, it gets a -1 penalty, this is to prevent it from just turning in circles
                agent.store_rewards(-1)

        snake.draw(surface)
        food.draw(surface)
        window.blit(surface, (0, 0))
        pygame.display.update()


if __name__ == "__main__":
    main()
