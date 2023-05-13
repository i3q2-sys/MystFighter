import pygame
from characterai import pyCAI
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import threading
import time
import pyganim


WIDTH = 1280
HEIGHT = 200
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 24
LINE_SPACING = 4
MARGIN = 40
MAX_LINES = 5
MAX_CHARS_PER_LINE = 200
offset = 380

smirk_words = ['smirk','smirks','smirking','smiles','smile','smiling', 'laughs', 'laugh']
blush_words = ['blush','blushing','blushes','blushed']
annoyed_words = ['frowns', 'angry', 'screams', 'scream', 'hate', 'menacing', 'mad', 'sword', 'dagger', 'knife', 'stabs']
confused_words = ['confused', 'confusion', 'what?', 'confused']

curr_emotion = 'neutral'

lock = threading.Lock()


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

def check_list(list, text):
    for word in list:
        if word in text:
            return True

    return False


def emotion_guesser(text):

    if check_list(smirk_words, text):
        return 'smirk'
    elif check_list(blush_words, text):
        return 'blush'
    elif check_list(confused_words, text):
        return 'confused'
    elif check_list(annoyed_words, text):
        return 'annoyed'
    else:
        return 'neutral'

def render():
    
    global screen
    global background
    global character
    global character_x
    global character_y
    global dialogue_square
    global dialogue
    global MARGIN
    global offset
    global response
    global curr_emotion
    global characters
    
    while True:

        start_time = time.time()

        with lock:
            screen.blit(background, (0, 0))
            screen.blit(characters[curr_emotion], (character_x, character_y))
            screen.blit(dialogue_square, (0,0))

            text_surfaces = render_text(dialogue)
            y = MARGIN + offset
            for surface in text_surfaces:
                screen.blit(surface, (MARGIN, y))
                y += surface.get_height() + LINE_SPACING
            size = y;

            text_surfaces = render_text("You: " + response)
            y = size + 10
            for surface in text_surfaces:
                screen.blit(surface, (MARGIN, y))
                y += surface.get_height() + LINE_SPACING

            # Update the Pygame display
            pygame.display.flip()

        elapsed_time = time.time() - start_time
        if elapsed_time < 1/30:
            time.sleep(1/30 - elapsed_time)


sia = SentimentIntensityAnalyzer()
token = '3bacec01844a43fd5e72089cfa8ea2cedb38335b'
character_id = 'nqAvzK4hFInlT_4CF9hbKPKMSsQgpAKTMuS3-Pduz-0'
client = pyCAI(token)


pygame.init()

# Define the screen dimensions
screen_width = 1280
screen_height = 720

sound = pygame.mixer.Sound('sound.mp3')

# Create the Pygame window
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))
menu = pygame.image.load("menu.png").convert()

characters = {'neutral': pygame.image.load("character/Character_neutral.png").convert_alpha()}
characters['annoyed'] = pygame.image.load("character/Character_angry.png").convert_alpha()
characters['blush'] = pygame.image.load("character/Character_blush.png").convert_alpha()
characters['confused'] = pygame.image.load("character/Character_confused.png").convert_alpha()
characters['smirk'] = pygame.image.load("character/Character_smirk.png").convert_alpha()


dialogue_square = pygame.image.load("dialogue.png").convert_alpha()
character_x = 960
character_y = 0
dialogue = "Hello, what's your name?"
response = ""
font = pygame.font.Font("NotoSansHK-Regular.otf", FONT_SIZE)
response_text = font.render(response, True, (255, 255, 255))

next_step = False

while not next_step:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            next_step = True
    pass
    screen.blit(menu,(0,0))
    pygame.display.flip()

intro = (
    'After traveling for a day, the warm squares of light coming from the tavern’s windows finally grow bigger as I approach the building. My feet ache, and my heart quickens in front of certainty. ',
    'I was certain the man I had been chasing for a while was right inside that tavern. Despite my curiosity, I had to keep in mind that, as a bounty hunter, this was just another commission.',
    'I decide to take a look at the small pieces of information I gathered during these last days.',
    ' ',
    'Finally, I push open the door and step inside the building.',
    'I see him, sitting on one of the stools, his body leaning on the bar’s counter in a relaxed pose. Yet somehow I know he’s still vigilant. ',
    'I’m also aware of my own surroundings, but remain clueless about what will happen when I approach him and strike up a conversation.',
    'Will he see through me? Will he run? Will he attack? Or maybe… Will I manage to discover his secrets? Is he really the man everyone in the Kingdom thinks he is? Whatever the outcome, I’ll be ready.',
    'I approached the stranger feeling fully confident.'
)

i = 0

while i < 9:

    screen.blit(background, (0, 0))

    if (i == 3):

        i = i

    else:
        text_surfaces = render_text(intro[i])
        y = MARGIN + offset
        for surface in text_surfaces:
            screen.blit(surface, (MARGIN, y))
            y += surface.get_height() + LINE_SPACING
        size = y;

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # User clicked the close button
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(i)
            i = i + 1
    pygame.display.flip()

sound.play(loops=-1)

t = threading.Thread(target=render)
t.start()

# Define a game loop
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            t.stop()
            pygame.quit()
            sys.exit()
    
        elif event.type == pygame.KEYDOWN:
            # If the player presses a key, add it to the response
            
            if event.unicode.isprintable():
                response += event.unicode
            
            elif event.key == pygame.K_BACKSPACE:
                response = response[:-1]

            elif event.key == pygame.K_RETURN:
                dialogue = ""
                aux_res = response
                response = ""
                dialogue = client.chat.send_message(character_id, aux_res)
                print("RECIEVED")
                curr_emotion = emotion_guesser(dialogue)
                print(curr_emotion)
                dialogue = "Koldoan: " + dialogue


# Quit Pygame
pygame.quit()