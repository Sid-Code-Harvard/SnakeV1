import random 

from config import (
    GRID_WIDTH,
    GRID_HEIGHT,
    INITIAL_SNAKE_LENGTH,
    INITIAL_SPEED,
    MAX_SPEED,
    POINTS_PER_FOOD,
    BONUS_FOOD_POINTS, 
)


class SnakeGame:

    def __init__(self, mode="classic"):

        self.mode = mode

        self.snake = [
            (GRID_WIDTH // 2, GRID_HEIGHT // 2)
            for i in range(INITIAL_SNAKE_LENGTH)
        ]

        self.direction = (1,0)
        self.next_direction = (1,0)


        self.score = 0
        self.level = 1
        self.speed = INITIAL_SPEED

        self.food = None
        self.bonus_food = None 

        self.obstacles = set()

        self.game_over = False
        self.paused = False 

        self.food_eaten = 0 
        self.spawn_food()

        if self.mode == "Obstacles":
            self.generate_obstacles()

    def spawn_food(self):
        empty_cells = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in self.snake
            and (x, y) not in self.obstacles
            and (x, y) != self.food
        ]

        if empty_cells:
            self.food = random.choice(empty_cells)

    def generate_obstacles(self):

        self.obstacles = set()

        center = (
            GRID_WIDTH // 2,
            GRID_HEIGHT // 2
        )

        while len(self.obstacles) < 15:

            position = (
                random.randint(2, GRID_WIDTH - 3),
                random.randint(2, GRID_HEIGHT - 3),
            )
            if (
                position not in self.snake 
                and position != center
            ):
                self.obstacles.add(position)

    def change_direction(self, direction):

        opposite = (
            -self.direction[0],
            -self.direction[1]
        )

        if direction != opposite:
            self.next_direction = direction 

    def move(self):

        if self.game_over or self.paused:
            return

        self.direction = self.next_direction 

        head_x, head_y = self.snake[0]

        dx, dy = self.direction

        new_head = (
            head_x + dx,
            head_y + dy
        )

        x, y = new_head



        if self.mode == "Zen":

            new_head = (
                x % GRID_WIDTH,
                y % GRID_HEIGHT
            )

        else:

            if (
                x < 0
                or x >= GRID_WIDTH
                or y < 0
                or y >= GRID_HEIGHT
            ):
                self.game_over = True 
                return 


            eating_food = new_head == self.food


            eating_bonus = new_head == self.bonus_food


            body = (
                self.snake
                if eating_food or eating_bonus
                else self.snake[:-1]
            )


            if new_head in body: 

                self.game_over = True 
                return 


            self.snake.insert(0, new_head)

            if eating_food:

                self.score += POINTS_PER_FOOD

                self.food_eaten += 1

                self.spawn_food()

                if self.food_eaten % 5 == 0:

                    self.level += 1 


                    self.speed = min(
                        INITIAL_SPEED + self.level,
                        MAX_SPEED
                    )

                if random.random() < 0.15:

                    self.spawn_bonus_food()

            elif eating_bonus:

                self.score += BONUS_FOOD_POINTS

                self.bonus_food = None

            else:

                self.snake.pop()

        def restart(self):

            self.__init__(self.mode)

        def toggle_pause(self):

            if not self.game_over:
                self.paused = not self.paused