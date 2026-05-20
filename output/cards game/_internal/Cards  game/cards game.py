# Card memory game
import pygame
import random
import json


# settings
WIDTH = 1280
HEIGHT = 720
FPS = 30

# Name of card
cards_values = [
    "CAT", "CAT",
    "SLEEP", "SLEEP",
    "BALL", "BALL",
    "FOREST", "FOREST",
    "HOM", "HOM",
    "CAKE", "CAKE",
    "FISH", "FISH",
    "NIGHT", "NIGHT",
    "TEA", "TEA",
    "SNOW", "SNOW",
    "MOON", "MOON",
    "WINDOW", "WINDOW",
    "BOOK", "BOOK",
    "BIRD", "BIRD",
    "APPLE", "APPLE",
    "CAR", "CAR"
]
# Random name
# random.shuffle(cards_values)

# Size
CARD_WIDTH = 110
CARD_HEIGHT = 140
button_width = 340
button_height = 90
CARD_MARGIN = 15


# Coordinate
title_y = 100
title_x = 250
button_x = 380
start_button_y = 280
exit_button_y = 410
CARD_START_X = 140
CARD_START_Y = 50

# Coordinates of button
start_button = pygame.Rect(button_x, start_button_y, button_width, button_height)
exit_button = pygame.Rect(button_x, exit_button_y, button_width, button_height)
continue_button = pygame.Rect(button_x, exit_button_y, button_width + 20, button_height)
select_button = pygame.Rect(button_x, start_button_y, button_width + 20, button_height)
top_button = pygame.Rect(button_x, start_button_y, button_width, button_height)


# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

MENU_COLOR = (255, 196, 195)
BUTTON_COLOR = (80, 80, 120)
BUTTON_HOVER = (110, 110, 170)
FIELD_COLOR = (240, 196, 239)
CARD_BUTTON_COLOR = (125, 86, 160)
CARD_BUTTON_HOVER = (155, 116, 190)


# Create Pygame window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра найди карточки")
clock = pygame.time.Clock()
game_state = "menu"

# Font
font_title = pygame.font.SysFont("comicsansms", 72)
font_button = pygame.font.SysFont("verdana", 42, bold=True)
font_card = pygame.font.SysFont("verdana", 40, bold=True)

# Settings of button
start_text = font_button.render("НАЧАТЬ ИГРУ", True, WHITE)
text_rect_start = start_text.get_rect(center=start_button.center)

exit_text = font_button.render("ВЫЙТИ", True, WHITE)
text_rect_exit = exit_text.get_rect(center=exit_button.center)

continue_text = font_button.render("ПРОДОЛЖИТЬ", True, WHITE)
text_rect_continue = continue_text.get_rect(center=continue_button.center)

select_text = font_button.render("ВВЕДИТЕ ИМЯ", True, WHITE)
text_rect_select = select_text.get_rect(center=select_button.center)

hover_select_text = font_button.render("_" * 8, True, WHITE)
hover_text_rect_select = hover_select_text.get_rect(midleft=(select_button.x + 60, select_button.centery))

top_text = font_button.render("ТОП", True, WHITE)
text_rect_top = top_text.get_rect(center=start_button.center)


# Add image

# Create table of cards
cards = []
index = 0
for i in range(4):
    for j in range(8):
        # Set coordinates
        target_x = CARD_START_X + j * (CARD_WIDTH + CARD_MARGIN)
        target_y = CARD_START_Y + i * (CARD_HEIGHT + CARD_MARGIN)

        # Set data of cards
        card = {
            "x": -300,
            "y": target_y,
            "target_x": target_x,
            "target_y": target_y,
            "speed": 20,
            "rect": pygame.Rect(-300, target_y, CARD_WIDTH, CARD_HEIGHT),
            "opened": False,
            "value": cards_values[index]
        }
        cards.append(card)
        index += 1

# Variables for checking cards
first_card = None
second_card = None

# Variables for win
result_saved = False

counter = 0

# Time
start_time = 0
seconds = 0

# Variables for adding name
player_name = ""
player_name_text = font_button.render(player_name, True, WHITE)

input_active = False

# Database
try:
    with open("leaders.json", "r", encoding="utf-8") as file:
        leaders = json.load(file)

except (FileNotFoundError, json.JSONDecodeError):
    leaders = []

# Music
pygame.mixer.music.stop()

pygame.mixer.music.load("assets/sounds/menu_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

win_sound = pygame.mixer.Sound("assets/sounds/win_wav.mp3")
click_sound = pygame.mixer.Sound("assets/sounds/click_wal.mp3")

# Game while
running = True
while running:

    # FPS
    clock.tick(FPS)
    # Events
    for event in pygame.event.get():
        # Closing the game with not gameplay way
        if event.type == pygame.QUIT:
            running = False

        # Checking keys
        if game_state == "game over":

            result_saved = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if top_button.collidepoint(pygame.mouse.get_pos()):
                    game_state = "top menu"
                    click_sound.play()

            # Closing the game with gameplay way
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(pygame.mouse.get_pos()):
                    running = False
                    start_time = pygame.time.get_ticks()

        if game_state == "menu":

            # Go to Name select menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(pygame.mouse.get_pos()):
                    game_state = "name select"
                    click_sound.play()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(pygame.mouse.get_pos()):
                    running = False
                    start_time = pygame.time.get_ticks()

        # Name select menu
        if game_state == "name select":

            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(pygame.mouse.get_pos()):
                    game_state = "game"
                    start_time = pygame.time.get_ticks()
                    pygame.mixer.music.stop()
                    click_sound.play()

                    pygame.mixer.music.load("assets/sounds/game_music.mp3")
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.1)

                if select_button.collidepoint(pygame.mouse.get_pos()):
                    input_active = True
                    click_sound.play()

            if input_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 10:

                        if event.unicode.isalpha() or event.unicode == " ":
                            player_name += event.unicode

        # Gameplay
        if game_state == "game":

            # Clicking on the card
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Pair check
                for card in cards:
                    if card["rect"].collidepoint(pygame.mouse.get_pos()):
                        click_sound.play()

                        if first_card is None:
                            first_card = card
                            card["opened"] = True

                        elif second_card is None and card != first_card:
                            second_card = card
                            card["opened"] = True

                            if first_card["value"] == second_card["value"]:
                                first_card = None
                                second_card = None
                                counter += 2

                            else:
                                # Forced rendering (for the second card command)
                                screen.fill(FIELD_COLOR)

                                current_time = pygame.time.get_ticks()

                                seconds = (current_time - start_time) // 1000

                                timer_text = font_button.render(
                                    f"Время: {seconds}",
                                    True,
                                    WHITE
                                )

                                screen.blit(timer_text, (0, -8))

                                # Create rent
                                for card in cards:
                                    card_rect = pygame.Rect(
                                        card["x"],
                                        card["y"],
                                        CARD_WIDTH,
                                        CARD_HEIGHT
                                    )
                                    # Draw of field
                                    pygame.draw.rect(
                                        screen,
                                        CARD_BUTTON_COLOR,
                                        card_rect,
                                        border_radius=15
                                    )
                                    # Card tip
                                    if card_rect.collidepoint(pygame.mouse.get_pos()):
                                        pygame.draw.rect(screen, CARD_BUTTON_HOVER, card_rect, border_radius=15)
                                    # Open card
                                    if card["opened"]:
                                        font_card = pygame.font.SysFont("verdana", 12, bold=True)
                                        card_text = font_card.render(card["value"], True, WHITE)
                                        text_rect_card = card_text.get_rect(center=card_rect.center)
                                        screen.blit(card_text, text_rect_card)

                                # Display flip
                                pygame.display.flip()

                                # Closing
                                pygame.time.delay(1000)

                                first_card["opened"] = False
                                second_card["opened"] = False

                                first_card = None
                                second_card = None

                    # End of game
                    if counter == 32 and result_saved == False:
                        result_saved = True

                        pygame.time.delay(30)

                        seconds = (pygame.time.get_ticks() - start_time) // 1000

                        leaders.append({
                            "name": player_name,
                            "time": seconds
                        })

                        leaders.sort(key=lambda x: x["time"])

                        leaders = leaders[:5]

                        with open("leaders.json", "w", encoding="utf-8") as file:
                            json.dump(leaders, file, ensure_ascii=False, indent=4)

                        # Set game over
                        game_state = "game over"
                        counter = 0
                        first_card = None
                        second_card = None
                        for card in cards:
                            card["opened"] = False
                        player_name = ""

                        # Music
                        pygame.mixer.music.stop()
                        win_sound.play()
                        pygame.mixer.music.stop()

                        pygame.mixer.music.load("assets/sounds/game_music.mp3")
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.1)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                with open("leaders.json", "w", encoding="utf-8") as file:
                    json.dump([], file, ensure_ascii=False, indent=4)

    # Updates
    mouse_pos = pygame.mouse.get_pos()
    # Animation
    for card in cards:

        if card["x"] < card["target_x"]:

            card["x"] += card["speed"]
            card["rect"].topleft = (card["x"], card["y"])

            if card["x"] > card["target_x"]:
                card["x"] = card["target_x"]
                card["rect"].topleft = (card["x"], card["y"])

    # Render

    # Menu
    if game_state == "menu":

        screen.fill(MENU_COLOR)
        # Menu text
        title_text = font_title.render("НАЙДИ КАРТОЧКИ", True, (60, 60, 60))
        screen.blit(title_text, (title_x, title_y))

        pygame.draw.rect(screen, BUTTON_COLOR, start_button, border_radius=20)
        screen.blit(start_text, text_rect_start)

        pygame.draw.rect(screen, BUTTON_COLOR, exit_button, border_radius=20)
        screen.blit(exit_text, text_rect_exit)

        # Button tip
        if start_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER, start_button, border_radius=20)
            screen.blit(start_text, text_rect_start)
        if exit_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER, exit_button, border_radius=20)
            screen.blit(exit_text, text_rect_exit)

    # Game over
    if game_state == "game over":
        screen.fill(MENU_COLOR)
        current_time = 0
        start_time = 0

        # Text at end
        title_text = font_title.render("ВЫ  ПОБЕДИЛИ", True, (60, 60, 60))
        screen.blit(title_text, (title_x, title_y))

        pygame.draw.rect(screen, BUTTON_COLOR, top_button, border_radius=20)
        screen.blit(top_text, text_rect_top)

        pygame.draw.rect(screen, BUTTON_COLOR, exit_button, border_radius=20)
        screen.blit(exit_text, text_rect_exit)

        # Button tip
        if start_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER, top_button, border_radius=20)
            screen.blit(top_text, text_rect_top)
        if exit_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER, exit_button, border_radius=20)
            screen.blit(exit_text, text_rect_exit)

    # Top menu
    if game_state == "top menu":
        screen.fill(MENU_COLOR)

        title = font_title.render("ТОП ИГРОКОВ", True, WHITE)

        screen.blit(title, (title_x, title_y - 50))

        # Table backgrounds
        pygame.draw.rect(
            screen,
            (70, 70, 100),
            (250, 250, 500, 420),
            border_radius=20
        )

        # Table
        top_y = 280
        place = 1

        for player in leaders:
            text = font_button.render(
                f'{place}. {player["name"]} - {player["time"]} сек',
                True,
                WHITE
            )

            screen.blit(text, (270, top_y))

            top_y += 50
            place += 1

    # Name select menu
    if game_state == "name select":

        screen.fill(MENU_COLOR)

        # Button of name
        select_title_text = font_title.render("ИМЯ ИГРОКА", True, (60, 60, 60))
        screen.blit(select_title_text, (title_x + 81, title_y))

        if select_button.collidepoint(mouse_pos):

            pygame.draw.rect(screen, BUTTON_HOVER, select_button, border_radius=20)

            if input_active:
                player_name_text = font_button.render(player_name, True, WHITE)
                player_name_rect = player_name_text.get_rect(center=select_button.center)

                screen.blit(player_name_text, player_name_rect)

                screen.blit(hover_select_text, hover_text_rect_select)

        else:
            pygame.draw.rect(screen, BUTTON_COLOR, select_button, border_radius=20)
            screen.blit(select_text, text_rect_select)

        # Exit button
        pygame.draw.rect(screen, BUTTON_COLOR, continue_button, border_radius=20)
        screen.blit(continue_text, text_rect_continue)

        if continue_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER, continue_button, border_radius=20)
            screen.blit(continue_text, text_rect_continue)

    # Game mode
    if game_state == "game":
        screen.fill(FIELD_COLOR)

        current_time = pygame.time.get_ticks()

        seconds = (current_time - start_time) // 1000

        timer_text = font_button.render(
            f"Время: {seconds}",
            True,
            WHITE
        )

        screen.blit(timer_text, (0, -8))

        # Create rent
        for card in cards:
            card_rect = pygame.Rect(
                card["x"],
                card["y"],
                CARD_WIDTH,
                CARD_HEIGHT
            )
            # Draw of field
            pygame.draw.rect(
                screen,
                CARD_BUTTON_COLOR,
                card_rect,
                border_radius=15
            )
            # Card tip
            if card_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, CARD_BUTTON_HOVER, card_rect, border_radius=15)
            # Open card
            if card["opened"]:
                font_card = pygame.font.SysFont("verdana", 12, bold=True)
                card_text = font_card.render(card["value"], True, WHITE)
                text_rect_card = card_text.get_rect(center=card_rect.center)
                screen.blit(card_text, text_rect_card)

    # Display flip
    pygame.display.flip()


pygame.quit()
