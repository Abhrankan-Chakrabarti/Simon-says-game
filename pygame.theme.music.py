import pygame
import random

pygame.init()
pygame.mixer.init()

# 🎵 Load and play background music
pygame.mixer.music.load("nostalgic-344879.mp3")  # Ensure this file exists in the same folder
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop indefinitely

# Screen setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simon Says - 16 Colors")

# Themes with 16 button color definitions
THEMES = {
    "Dark": {
        "bg": pygame.Color("black"),
        "text": pygame.Color("white"),
        "buttons": [
            "red", "green", "blue", "yellow",
            "orange", "purple", "cyan", "magenta",
            "lime", "pink", "teal", "maroon",
            "navy", "olive", "brown", "gray"
        ]
    },
    "Light": {
        "bg": pygame.Color("white"),
        "text": pygame.Color("black"),
        "buttons": [
            "salmon", "lightgreen", "skyblue", "khaki",
            "coral", "plum", "lightcyan", "orchid",
            "palegreen", "hotpink", "turquoise", "rosybrown",
            "slateblue", "beige", "sandybrown", "gainsboro"
        ]
    },
    "Retro": {
        "bg": pygame.Color("darkblue"),
        "text": pygame.Color("lightyellow"),
        "buttons": [
            "crimson", "gold", "darkgreen", "orange",
            "darkred", "darkgoldenrod", "seagreen", "dodgerblue",
            "indigo", "coral", "mediumvioletred", "slategray",
            "firebrick", "peru", "mediumblue", "mediumseagreen"
        ]
    },
    "Neon": {
        "bg": pygame.Color("black"),
        "text": pygame.Color("aqua"),
        "buttons": [
            "aqua", "lime", "fuchsia", "yellow",
            "springgreen", "deeppink", "chartreuse", "cyan",
            "violet", "turquoise", "magenta", "orange",
            "red", "blue", "green", "gold"
        ]
    }
}

theme_names = list(THEMES.keys())
current_theme_index = 0

# Button setup (4x4)
BUTTONS = {}
BUTTON_SIZE = 150
for i in range(4):
    for j in range(4):
        idx = i * 4 + j
        rect = pygame.Rect(j * BUTTON_SIZE, i * BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE)
        BUTTONS[idx] = rect

# High score functions
def get_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# UI functions
def draw_buttons(highlight=None):
    theme = THEMES[theme_names[current_theme_index]]
    screen.fill(theme["bg"])
    for idx, rect in BUTTONS.items():
        color_name = theme["buttons"][idx]
        color = pygame.Color(color_name)
        if highlight == idx:
            color = theme["text"]
        pygame.draw.rect(screen, color, rect)
    pygame.display.flip()

def flash(index):
    draw_buttons(highlight=index)
    pygame.time.delay(500)
    draw_buttons()
    pygame.time.delay(250)

def show_message(text, delay=1000):
    theme = THEMES[theme_names[current_theme_index]]
    font = pygame.font.Font(None, 48)
    msg = font.render(text, True, theme["text"])
    rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(msg, rect)
    pygame.display.flip()
    pygame.time.delay(delay)
    draw_buttons()

def show_theme_label():
    theme = THEMES[theme_names[current_theme_index]]
    font = pygame.font.Font(None, 36)
    label = f"Theme: {theme_names[current_theme_index]}"
    text = font.render(label, True, theme["text"])
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 30))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.delay(1000)
    draw_buttons()

def wait_for_input():
    global current_theme_index
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    current_theme_index = (current_theme_index + 1) % len(theme_names)
                    draw_buttons()
                    show_theme_label()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for idx, rect in BUTTONS.items():
                    if rect.collidepoint(x, y):
                        flash(idx)
                        return idx

def wait_for_start(message="Click to Start"):
    global current_theme_index
    draw_buttons()
    theme = THEMES[theme_names[current_theme_index]]
    font_main = pygame.font.Font(None, 48)
    font_note = pygame.font.Font(None, 28)

    msg_main = font_main.render(message, True, theme["text"])
    msg_note = font_note.render("Press Ctrl + T to change theme", True, theme["text"])

    rect_main = msg_main.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    rect_note = msg_note.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))

    screen.blit(msg_main, rect_main)
    screen.blit(msg_note, rect_note)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    current_theme_index = (current_theme_index + 1) % len(theme_names)
                    draw_buttons()
                    wait_for_start(message)
                else:
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def main():
    while True:
        wait_for_start("Click to Start")
        running = True
        sequence = []
        level = 1
        high_score = get_high_score()
        draw_buttons()

        while running:
            show_message(f"Level {level}")

            if level in [5, 10, 20]:
                messages = {
                    5: "🎉 Great job! Keep going!",
                    10: "🔥 Amazing memory!",
                    20: "👑 You're a Simon Master!"
                }
                show_message(messages[level], delay=1500)

            sequence.append(random.choice(list(BUTTONS.keys())))

            for idx in sequence:
                flash(idx)

            for idx in sequence:
                user_input = wait_for_input()
                if user_input == "quit":
                    pygame.quit()
                    return
                if user_input != idx:
                    final_score = level - 1
                    show_message("Game Over!", delay=1000)
                    show_message(f"Level Reached: {final_score}", delay=1000)

                    if final_score > high_score:
                        save_high_score(final_score)
                        show_message("🎉 New High Score!", delay=1000)
                        show_message(f"High Score: {final_score}", delay=1500)
                    else:
                        show_message(f"High Score: {high_score}", delay=1500)

                    wait_for_start("Press R to Restart or Q to Quit")
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                return
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_r:
                                    waiting = False
                                elif event.key == pygame.K_q:
                                    pygame.quit()
                                    return
                    running = False
                    break
            else:
                level += 1
                continue
            break

if __name__ == "__main__":
    main()
