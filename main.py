import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Asset Loading
RUNNING_FRAMES = [
    pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png")),
]
JUMPING_FRAME = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING_FRAMES = [
    pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png")),
]

SMALL_CACTUS_IMAGES = [
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png")),
]
LARGE_CACTUS_IMAGES = [
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png")),
]

BIRD_FRAMES = [
    pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("Assets/Bird", "Bird2.png")),
]

CLOUD_IMAGE = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
BACKGROUND_IMAGE = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


# Dinosaur Class
class Dino:
    X_POS = 80  # X position of the Dino on the screen
    Y_POS_RUNNING = 310  # Y position while running
    Y_POS_DUCKING = 340  # Y position while ducking
    JUMP_SPEED = 8.5  # Initial speed during a jump

    def __init__(self):
        # Set images for running, ducking, and jumping
        self.run_frames = RUNNING_FRAMES
        self.duck_frames = DUCKING_FRAMES
        self.jump_frame = JUMPING_FRAME

        # Initial state
        self.is_ducking = False
        self.is_running = True
        self.is_jumping = False

        # Step index for animation cycling
        self.step_index = 0
        self.jump_velocity = self.JUMP_SPEED
        self.image = self.run_frames[0]  # Start with the running image

        # Dino rectangle for collision and positioning
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS_RUNNING

    def update(self, user_input):
        # Check and update state based on user input
        if self.is_ducking:
            self.duck()
        elif self.is_running:
            self.run()
        elif self.is_jumping:
            self.jump()

        if self.step_index >= 10:  # Reset step index for animation
            self.step_index = 0

        # Handle key presses
        if user_input[pygame.K_UP] and not self.is_jumping:
            self.is_ducking = False
            self.is_running = False
            self.is_jumping = True
        elif user_input[pygame.K_DOWN] and not self.is_jumping:
            self.is_ducking = True
            self.is_running = False
            self.is_jumping = False
        elif not self.is_jumping and not user_input[pygame.K_DOWN]:
            self.is_ducking = False
            self.is_running = True

    def duck(self):
        # Switch to ducking image and update rectangle position
        self.image = self.duck_frames[self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS_DUCKING
        self.step_index += 1

    def run(self):
        # Switch to running image and update rectangle position
        self.image = self.run_frames[self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS_RUNNING
        self.step_index += 1

    def jump(self):
        # Handle jumping logic
        self.image = self.jump_frame
        if self.is_jumping:
            self.rect.y -= self.jump_velocity * 4
            self.jump_velocity -= 0.8
        if self.jump_velocity < -self.JUMP_SPEED:
            self.is_jumping = False
            self.jump_velocity = self.JUMP_SPEED

    def draw(self, screen):
        # Draw Dino on the screen
        screen.blit(self.image, (self.rect.x, self.rect.y))


# Cloud Class
class Cloud:
    def __init__(self):
        # Initialize cloud position and load image
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD_IMAGE
        self.width = self.image.get_width()

    def update(self):
        # Move cloud to the left and reset position if off-screen
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, screen):
        # Draw cloud on the screen
        screen.blit(self.image, (self.x, self.y))


# Base Obstacle Class
class Obstacle:
    def __init__(self, images, obstacle_type):
        self.images = images
        self.type = obstacle_type
        self.rect = self.images[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        # Move obstacle to the left and remove if off-screen
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        # Draw obstacle on the screen
        screen.blit(self.images[self.type], self.rect)


# Specific Obstacle Classes
class SmallCactus(Obstacle):
    def __init__(self, images):
        super().__init__(images, random.randint(0, 2))
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, images):
        super().__init__(images, random.randint(0, 2))
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, images):
        super().__init__(images, 0)
        self.rect.y = 250
        self.animation_index = 0

    def draw(self, screen):
        # Animate bird by switching frames
        if self.animation_index >= 9:
            self.animation_index = 0
        screen.blit(self.images[self.animation_index // 5], self.rect)
        self.animation_index += 1


# Main Game Function
def main_game():
    global game_speed, x_bg_position, y_bg_position, score_points, obstacles
    run_game = True
    clock = pygame.time.Clock()
    player = Dino()
    cloud = Cloud()
    game_speed = 20
    x_bg_position = 0
    y_bg_position = 380
    score_points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def display_score():
        global score_points, game_speed
        score_points += 1
        if score_points % 100 == 0:
            game_speed += 1
        score_text = font.render(f"Score: {score_points}", True, (0, 0, 0))
        screen_rect = score_text.get_rect()
        screen_rect.center = (1000, 40)
        SCREEN.blit(score_text, screen_rect)

    def update_background():
        global x_bg_position, y_bg_position
        bg_width = BACKGROUND_IMAGE.get_width()
        SCREEN.blit(BACKGROUND_IMAGE, (x_bg_position, y_bg_position))
        SCREEN.blit(BACKGROUND_IMAGE, (x_bg_position + bg_width, y_bg_position))
        if x_bg_position <= -bg_width:
            x_bg_position = 0
        x_bg_position -= game_speed

    while run_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

        SCREEN.fill((255, 255, 255))
        user_input = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(user_input)

        # Spawn obstacles
        if not obstacles:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS_IMAGES))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS_IMAGES))
            else:
                obstacles.append(Bird(BIRD_FRAMES))

        # Update obstacles
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                game_menu(death_count)

        update_background()
        cloud.draw(SCREEN)
        cloud.update()
        display_score()

        clock.tick(30)
        pygame.display.update()


# Game Menu
def game_menu(death_count):
    global score_points
    run_menu = True
    while run_menu:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            menu_text = font.render("Press Any Key to Start", True, (0, 0, 0))
        else:
            menu_text = font.render("Press Any Key to Restart", True, (0, 0, 0))
            score_text = font.render(f"Your Score: {score_points}", True, (0, 0, 0))
            score_rect = score_text.get_rect()
            score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score_text, score_rect)

        menu_rect = menu_text.get_rect()
        menu_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(menu_text, menu_rect)
        SCREEN.blit(RUNNING_FRAMES[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run_menu = False
            if event.type == pygame.KEYDOWN:
                main_game()


# Start the game
game_menu(death_count=0)
