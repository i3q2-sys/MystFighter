import pygame
from characterai import pyCAI
from transformers import pipeline   

WIDTH = 1280
HEIGHT = 200
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 24
LINE_SPACING = 4
MARGIN = 20
MAX_LINES = 5
MAX_CHARS_PER_LINE = 200
offset = 450
from transformers import pipeline
sentiment_pipeline = pipeline("sentiment-analysis")
data = "I fucking love you"
print(sentiment_pipeline(data))


# split text into lines
def split_lines(text):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        if font.size(line + word)[0] > WIDTH - 2 * MARGIN:
            lines.append(line)
            line = ""
        line += word + " "
    if line:
        lines.append(line)
    return lines


def render_text(text):
    lines = split_lines(text)[:MAX_LINES]
    surfaces = []
    for line in lines:
        surfaces.append(font.render(line, True, TEXT_COLOR))
    return surfaces


token = '3bacec01844a43fd5e72089cfa8ea2cedb38335b'
character_id = 'WsqG34NBsbCr3hxN7gJA_y5khYtVQzTD71IqdtfO57Y'
client = pyCAI(token, headless=False)


pygame.init()

# Define the screen dimensions
screen_width = 1280
screen_height = 720

# Create the Pygame window
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load("background.png").convert()
character = pygame.image.load("character.png").convert_alpha()
dialogue1 = pygame.image.load("dialogue.png").convert_alpha()
dialogue2 = pygame.image.load("dialogue.png").convert_alpha()
character_x = 640
character_y = 0
dialogue = "Hello, what's your name?"
response = "You: "
font = pygame.font.Font(None, 36)
response_text = font.render(response, True, (255, 255, 255))

# Define a game loop
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            dialogue_complete = True
    
        elif event.type == pygame.KEYDOWN:
            # If the player presses a key, add it to the response
            
            if event.unicode.isprintable():
                response += event.unicode
            
            elif event.key == pygame.K_BACKSPACE:
                response = response[:-1]

            elif event.key == pygame.K_RETURN:

                screen.blit(background, (0, 0))
                screen.blit(character, (character_x, character_y))
                response_text = font.render(" ", True, (255, 255, 255))
                dialogue_text = font.render(" ", True, (255, 255, 255))
                screen.blit(dialogue_text, (50, 500))
                screen.blit(response_text, (50, 550))
                pygame.display.flip()

                dialogue = client.chat.send_message(character_id, response)
                dialogue = "Koldoan: " + dialogue
                response = "You: "


    
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x, character_y))
    screen.blit(dialogue1, (MARGIN,MARGIN + offset))
    screen.blit(dialogue2, (MARGIN,MARGIN + offset + 135))



    text_surfaces = render_text(dialogue)
    y = MARGIN + offset
    for surface in text_surfaces:
        screen.blit(surface, (MARGIN, y))
        y += surface.get_height() + LINE_SPACING
    size = y;

    text_surfaces = render_text(response)
    y = size + 10
    for surface in text_surfaces:
        screen.blit(surface, (MARGIN, y))
        y += surface.get_height() + LINE_SPACING


    # Update the Pygame display
    pygame.display.flip()

# Quit Pygame
pygame.quit()