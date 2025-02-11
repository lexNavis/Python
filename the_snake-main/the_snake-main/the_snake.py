from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Basic graphic object"""

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self):
        """Draws an object in the window. Must be redefined in child class"""
        pass


class Apple(GameObject):
    """Apple - food for snake"""

    def __init__(self):
        self.body_color = (255, 0, 0)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Returns a randomized pair of coordinates (x,y)"""
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    # Метод draw класса Apple
    def draw(self):
        """Draws an apple on the display"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Snake object"""

    def __init__(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None

    def update_direction(self):
        """Updates the direction of the snake if needed"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    # Метод draw класса Snake
    def draw(self):
        """Draws a snake on the display"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Returns the position of the head(first list element)"""
        return self.positions[0]

    def move(self):
        """Simulating movement by correcting the position list"""
        head_position = self.get_head_position()
        if self.direction == RIGHT:
            new_x = (head_position[0] + GRID_SIZE) % SCREEN_WIDTH
            head_position = (new_x, head_position[1])
        elif self.direction == LEFT:
            new_x = (head_position[0] - GRID_SIZE) % SCREEN_WIDTH
            head_position = (new_x, head_position[1])
        elif self.direction == DOWN:
            new_y = (head_position[1] + GRID_SIZE) % SCREEN_HEIGHT
            head_position = (head_position[0], new_y)
        elif self.direction == UP:
            new_y = (head_position[1] - GRID_SIZE) % SCREEN_HEIGHT
            head_position = (head_position[0], new_y)
        if self.length > 2 and head_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, head_position)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        """New game start"""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.__init__()
        self.direction = [UP, DOWN, LEFT, RIGHT][randint(0, 3)]


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Choose next snake direction based on pressed button"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Main part of the game"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        snake.draw()
        apple.draw()
        handle_keys(snake)
        snake.update_direction()
        pygame.display.update()
        snake.last = snake.positions[-1]
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple = Apple()


if __name__ == '__main__':
    main()
