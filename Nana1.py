import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60
GAME_SPEED = 5
GRAVITY = 0.5
JUMP_HEIGHT = -12
NANA_GROUND_OFFSET = int(SCREEN_HEIGHT * 0.061)  # Nana's position from bottom
CATCH_IMAGE_TIME = 1000
CATCH_RESET_TIME = 1000  # 1 second to reset catch image
BACKGROUND_COLOR = (255, 255, 255)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Nana's Food Hunt")
clock = pygame.time.Clock()

# Load images
background_img = pygame.image.load('background.png').convert_alpha()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_over_img = pygame.image.load('game_over.png').convert_alpha()
game_over_img = pygame.transform.scale(game_over_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
final_img = pygame.image.load('final.png').convert_alpha()
final_img = pygame.transform.scale(final_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
hooray_img = pygame.image.load('hooray.png').convert_alpha()
hooray_img = pygame.transform.scale(hooray_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Nana images and scaling
nana_scale_factor = 0.4
nana_images = {
    'static': pygame.image.load('Nana.png').convert_alpha(),
    'left': pygame.image.load('left.png').convert_alpha(),
    'right': pygame.image.load('right.png').convert_alpha(),
    'jump': pygame.image.load('jump.png').convert_alpha(),
    'catch': pygame.image.load('catch.png').convert_alpha()
}
for key, image in nana_images.items():
    nana_images[key] = pygame.transform.scale(image, (int(image.get_width() * nana_scale_factor), int(image.get_height() * nana_scale_factor)))

# Ingredient images and scaling
ingredient_scale_factor = 0.18
ingredient_types = ['Juicy_Steak', 'Fish_Fillet', 'Cheese_Wedge', 'Carrots_Bundle', 'Can_of_Dog_Food', 'Bone-In_Ham', 'Bag_of_Kibble']
ingredient_images = {name: pygame.image.load(f'{name}.png').convert_alpha() for name in ingredient_types}
for name, image in ingredient_images.items():
    ingredient_images[name] = pygame.transform.scale(image, (int(image.get_width() * ingredient_scale_factor), int(image.get_height() * ingredient_scale_factor)))

# Nana's properties
nana = {
    'rect': nana_images['static'].get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - NANA_GROUND_OFFSET)),
    'image': nana_images['static'],
    'jumping': False,
    'velocity': 0,
    'catch_timer': 0
}

# Ingredients properties
ingredients = []
spawn_ingredient_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_ingredient_event, 1000)

# Score
score = 0

# Game state
game_active = True

# Functions
def handle_keys():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not nana['jumping']:
        nana['jumping'] = True
        nana['velocity'] = JUMP_HEIGHT
        nana['image'] = nana_images['jump']
    else:
        if keys[pygame.K_LEFT]:
            nana['rect'].x -= GAME_SPEED
            if not nana['jumping']:  # Only change image if not jumping
                nana['image'] = nana_images['left']
        elif keys[pygame.K_RIGHT]:
            nana['rect'].x += GAME_SPEED
            if not nana['jumping']:  # Only change image if not jumping
                nana['image'] = nana_images['right']
        else:
            if not nana['jumping']:  # Only reset to static if not jumping
                nana['image'] = nana_images['static']   
      # Add boundaries for Nana's movement
        if nana['rect'].left < 0:
            nana['rect'].left = 0
        elif nana['rect'].right > SCREEN_WIDTH:
            nana['rect'].right = SCREEN_WIDTH

def update_nana():
    if nana['jumping']:
        nana['rect'].y += nana['velocity']
        nana['velocity'] += GRAVITY
        if nana['rect'].bottom >= SCREEN_HEIGHT - NANA_GROUND_OFFSET:
            nana['rect'].bottom = SCREEN_HEIGHT - NANA_GROUND_OFFSET
            nana['jumping'] = False
            nana['velocity'] = 0

    # Check if catch image should be reset
    if nana['catch_timer'] != 0:
        current_time = pygame.time.get_ticks()
        if current_time - nana['catch_timer'] >= CATCH_IMAGE_TIME:
            nana['image'] = nana_images['static']
            nana['catch_timer'] = 0


def create_ingredient():
    name = random.choice(ingredient_types)
    img = ingredient_images[name]
    x_pos = random.randrange(int(SCREEN_WIDTH * 0.2), int(SCREEN_WIDTH * 0.8))
    rect = img.get_rect(midbottom=(x_pos, 0))
    ingredients.append({'name': name, 'rect': rect, 'image': img})

def update_ingredients():
    global score
    for ingredient in ingredients[:]:  # Notice the [:] which makes a copy of the list
        ingredient['rect'].y += GAME_SPEED
        if ingredient['rect'].top > SCREEN_HEIGHT:
            ingredients.remove(ingredient)
            score -= 1  # Decrease the score when an ingredient falls to the ground


def check_catch():
    global score
    for ingredient in ingredients[:]:
        if nana['rect'].colliderect(ingredient['rect']):
            score += 1
            ingredients.remove(ingredient)
            nana['image'] = nana_images['catch']
            nana['catch_timer'] = pygame.time.get_ticks()  # Start the timer when Nana catches an ingredient



def draw():
    screen.fill(BACKGROUND_COLOR)
    screen.blit(background_img, (0, 0))
    for ingredient in ingredients:
        screen.blit(ingredient['image'], ingredient['rect'])
    screen.blit(nana['image'], nana['rect'])
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

def game_over():
    screen.blit(game_over_img, (0, 0))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

def win_game():
    screen.blit(final_img, (0, 0))
    pygame.display.flip()
    pygame.time.wait(5000)
    hooray_animation()

def hooray_animation():
    for alpha in range(0, 256, 2):
        hooray_img.set_alpha(alpha)
        screen.blit(hooray_img, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)
    pygame.time.wait(2000)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == spawn_ingredient_event:
            create_ingredient()

    handle_keys()
    check_catch()
    update_nana()  # This function will now check and reset Nana's image when necessary
    update_ingredients()
    draw()

    if score < 0:
        game_over()
        break

    if score >= 20:
        win_game()
        break

    clock.tick(FPS)

pygame.quit()

