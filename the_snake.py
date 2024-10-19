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
SPEED = 14

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс объекта игры"""

    def __init__(self, body_color=None):
        self.position = (SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2)
        self.body_color = body_color

    def draw(self):
        """Отрисовка"""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко"""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Выбор случайной позиции в пределах игрового поля"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовка"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку"""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self):
        """Отрисовка"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
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

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновление координат змейки"""
        new_position = None
        if self.direction == RIGHT:
            new_position = (self.get_head_position()[0] + GRID_SIZE,
                            self.get_head_position()[1])

            if new_position[0] > SCREEN_WIDTH - GRID_SIZE:
                new_position = (0, new_position[1])
        elif self.direction == LEFT:
            new_position = (self.get_head_position()[0] - GRID_SIZE,
                            self.get_head_position()[1])

            if new_position[0] < 0:
                new_position = (SCREEN_WIDTH - GRID_SIZE, new_position[1])
        elif self.direction == UP:
            new_position = (self.get_head_position()[0],
                            self.get_head_position()[1] - GRID_SIZE)

            if new_position[1] < 0:
                new_position = (new_position[0], SCREEN_HEIGHT - GRID_SIZE)
        elif self.direction == DOWN:
            new_position = (self.get_head_position()[0],
                            self.get_head_position()[1] + GRID_SIZE)

            if new_position[1] > SCREEN_HEIGHT - GRID_SIZE:
                new_position = (new_position[0], 0)
        else:
            return

        self.positions.insert(0, new_position)
        if self.length != len(self.positions):
            self.last = self.positions.pop()

    def get_head_position(self):
        """Получение координат головы змейки"""
        return self.positions[0]

    def reset(self):
        """сбрасывает змейку в начальное состояние после
        столкновения с собой.
        """
        self.length = 1
        self.positions = [(SCREEN_WIDTH / 2, SCREEN_WIDTH / 2)]


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
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
    """Основная функция игры"""
    # Инициализация PyGame:
    pygame.init()

    snake = Snake()
    apple = Apple()

    while apple.position in snake.positions:
        apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple = Apple()

            while apple.position in snake.positions:
                apple = Apple()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            rect = pygame.Rect((0, 0), (SCREEN_HEIGHT, SCREEN_WIDTH))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

        print(snake.positions)
        print(f'apple: {apple.position}')
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
