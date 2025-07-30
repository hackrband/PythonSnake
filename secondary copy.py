import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 350, 530
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 225)
BLACK = (0, 0, 0)
# User Colors & Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)


# Font
FONT = pygame.font.Font(None, 36)


# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2), (GRID_WIDTH // 2, GRID_HEIGHT // 2 + 1),
                     (GRID_WIDTH // 2, GRID_HEIGHT // 2 + 2)]
        self.direction = (0, 0)  # Start with no movement
        self.started_moving = False  # Indicates if snake has started moving
        self.frozen = True  # Start frozen

    def move(self):
        if not self.frozen:
            new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
            self.body = [new_head] + self.body[:-1]

    def grow(self):
        self.body.append(self.body[-1])

    def draw(self, surface):
        for i, segment in enumerate(self.body):
            color = blend_color(i / len(self.body))
            pygame.draw.rect(surface, color, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def blend_color(ratio):
    # Define colors for the head, tail, and blend between them
    head_color = GREEN  # Lightest
    tail_color = (0, 50, 0)  # Darkest
    blend_color = [int(head_color[i] * ratio + tail_color[i] * (1 - ratio)) for i in range(3)]
    return tuple(blend_color)


# Food class
def randomize_position():
    return random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)


class Food:
    def __init__(self):
        self.position = randomize_position()

    def draw(self, surface):
        # Calculate the center of the circle
        center = ((self.position[0] * GRID_SIZE) + (GRID_SIZE // 2), (self.position[1] * GRID_SIZE) + (GRID_SIZE // 2))
        # Calculate the radius of the circle
        radius = GRID_SIZE // 2
        pygame.draw.circle(surface, RED, center, radius)

# Function to display text
def display_text(text, position):
    text_surface = FONT.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=position)
    WIN.blit(text_surface, text_rect)


def game_over(score):
    best_score = 0

    try:
        with open("data.txt", "r") as file:
            best_score = int(file.read())
    except FileNotFoundError:
        print('Unable to saves score')
        pass

    if score > best_score:
        best_score = score
        with open("data.txt", "w") as file:
            file.write(str(best_score))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    pygame.quit()
                    quit()

        WIN.fill(WHITE)
        display_text("GAME OVER!", (WIDTH // 2, HEIGHT // 2))
        display_text(f"Score: {score}", (WIDTH // 2, HEIGHT // 2 - 50))
        display_text("Play again? (Y/N)", (WIDTH // 2, HEIGHT // 2 + 50))
        display_text(f"Best Score: {best_score}", (WIDTH // 2, HEIGHT - 20))  # Remove 'size' parameter
        pygame.display.update()


# Main function
def main():
    clock = pygame.time.Clock()

    while True:
        snake = Snake()
        food = Food()
        score = 0
        popup_shown = True  # Set to True initially

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                        if not snake.started_moving and popup_shown:
                            snake.started_moving = True
                            snake.frozen = False
                            popup_shown = False
                        if event.key == pygame.K_UP and snake.direction != (0, 1):
                            snake.direction = (0, -1)
                        elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                            snake.direction = (0, 1)
                        elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                            snake.direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                            snake.direction = (1, 0)

            if not snake.frozen:
                snake.move()

            if snake.body[0] == food.position:
                snake.grow()
                food.position = randomize_position()
                score += 1

            # Check collision with walls or itself
            if (snake.body[0][0] < 0 or snake.body[0][0] >= GRID_WIDTH or
                    snake.body[0][1] < 0 or snake.body[0][1] >= GRID_HEIGHT or
                    snake.body[0] in snake.body[1:]):
                if game_over(score):
                    break

            # Draw everything
            WIN.fill(WHITE)
            snake.draw(WIN)
            food.draw(WIN)

            display_text(f"Score: {score}", (WIDTH // 2, 20))

            if popup_shown:
                display_text("Click an arrow to start", (WIDTH // 2, HEIGHT - 20))

            # Update the display
            pygame.display.update()

            clock.tick(10)  # Adjust the speed of the snake


if __name__ == "__main__":
    main()
