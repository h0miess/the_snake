from random import randint, choice
import os.path

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

CENTER_X, CENTER_Y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2

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

# Цвет банана
BANANA_COLOR = (255, 255, 0)

# Цвет персика
GRAPE_COLOR = (252, 15, 192)

# Цвет голубики
BLUEBERRY_COLOR = (0, 0, 255)

# Скорость движения змейки:
SPEED = 14

# Названия файла с сохраненным рекордом
RECORD_FILE_NAME = "record.txt"

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

record = ""
if os.path.exists(RECORD_FILE_NAME):
    with open(RECORD_FILE_NAME, 'r') as file:
        try:
            record = str(int(file.readline()))
        except ValueError:
            pass

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка" + record)

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс объекта игры"""

    def __init__(self, body_color=None):
        self.position = (CENTER_X, CENTER_Y)
        self.body_color = body_color

    def draw(self):
        """Отрисовка"""
        pass


class Eat(GameObject):
    """Абстрактный класс, описывающий объект еды"""

    def __init__(self, body_color):
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self):
        """Выбор случайной позиции в пределах игрового поля"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовка"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def clear(self):
        """Очистка объекта с игрового поля"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)


class Apple(Eat):
    """Класс, описывающий яблоко"""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)


class Banana(Eat):
    """Класс, описывающий банан (неправильная еда)"""

    def __init__(self):
        super().__init__(BANANA_COLOR)


class Grape(Eat):
    """Класс, описывающий виноград (неправильная еда)"""

    def __init__(self):
        super().__init__(GRAPE_COLOR)


class Blueberry(Eat):
    """Класс, описывающий голубику (неправильная еда)"""

    def __init__(self):
        super().__init__(BLUEBERRY_COLOR)


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
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.get_head_position(),
                                (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def decrease(self):
        """Уменьшить длину змейки на 1 квадратик"""
        if self.length == 1:
            return

        self.length -= 1
        tail = pygame.Rect(self.positions.pop(), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, tail)

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновление координат змейки"""
        new_position = None
        if self.direction == RIGHT:
            new_position = (
                self.get_head_position()[0] + GRID_SIZE,
                self.get_head_position()[1],
            )

            if new_position[0] > SCREEN_WIDTH - GRID_SIZE:
                new_position = (0, new_position[1])
        elif self.direction == LEFT:
            new_position = (
                self.get_head_position()[0] - GRID_SIZE,
                self.get_head_position()[1],
            )

            if new_position[0] < 0:
                new_position = (SCREEN_WIDTH - GRID_SIZE, new_position[1])
        elif self.direction == UP:
            new_position = (
                self.get_head_position()[0],
                self.get_head_position()[1] - GRID_SIZE,
            )

            if new_position[1] < 0:
                new_position = (new_position[0], SCREEN_HEIGHT - GRID_SIZE)
        elif self.direction == DOWN:
            new_position = (
                self.get_head_position()[0],
                self.get_head_position()[1] + GRID_SIZE,
            )

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
        self.positions = [(CENTER_X, CENTER_Y)]


def save_record(length):
    """Функция для записи рекорда"""
    with open(RECORD_FILE_NAME, "w+") as file:
        prev_record = None
        try:
            prev_record = int(file.readline())
        except ValueError:
            pass
        if prev_record is None or length > prev_record:
            file.write(str(length))


def quit_game(game_object, record):
    """Функция выхода из игры"""
    pygame.quit()
    save_record(record)
    raise SystemExit


def handle_keys(game_object, record):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game(game_object, record)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:
                quit_game(game_object, record)
                raise SystemExit


def main() -> None:
    """Основная функция игры"""
    # Инициализация PyGame:
    pygame.init()

    snake = Snake()
    apple = Apple()

    bad_eat_list = [Banana(), Grape(), Blueberry()]
    bad_eat: Eat = choice(bad_eat_list)

    session_record = int(record) if record != '' else 1

    while apple.position in snake.positions:
        apple = apple.randomize_position()

    while True:
        clock.tick(SPEED)
        handle_keys(snake, session_record)
        snake.update_direction()
        snake.move()
        snake_head = snake.get_head_position()
        if apple.position == snake_head or bad_eat.position == snake_head:

            if apple.position == snake_head:
                snake.length += 1

                if snake.length > session_record:
                    session_record = snake.length

            elif bad_eat.position == snake_head:
                snake.decrease()

            apple.clear()
            apple.randomize_position()

            bad_eat.clear()
            bad_eat: Eat = choice(bad_eat_list)
            bad_eat.randomize_position()

            while apple.position in snake.positions:
                apple.randomize_position()

            while bad_eat.position in snake.positions:
                bad_eat.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

            # Очистка всего поля
            rect = pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

        snake.draw()
        apple.draw()
        bad_eat.draw()
        pygame.display.set_caption(f"Змейка. Рекорд: {session_record}!")
        pygame.display.update()


if __name__ == "__main__":
    main()
