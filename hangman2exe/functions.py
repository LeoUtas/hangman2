import pygame, math, pandas as pd
from elements import Designs, Words
from random import choice
from datetime import datetime
    

pygame.init()

# set up width, height and caption for the main window
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# prepare to draw the letter buttons
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
letterA = chr(65) # because the letter A is 65
visibility = True # use later to remove chosen letters
space_pos = ((WIDTH - RADIUS)/2, 520)
space_line = pygame.Rect(WIDTH/3-6, 498, WIDTH/3, 45.5)

# prepare to draw leter buttons at coordinate x, y
for _ in range(26):
    x = startx + GAP * 2 + (RADIUS * 2 + GAP) * (_ % 13)
    y = starty + ((_//13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(ord(letterA) + _), visibility])
letters.append([space_pos[0], space_pos[1], " ", visibility])

hangman_stage = 0
word_guessed = [] 
score = 0

def display_score(*args):
    window.fill(Designs.bg_color)
    text = Designs.letter_font.render(f"Score: {args[0]}", 1, args[1])
    window.blit(text, (480, 66))
    pygame.display.update()

def record_score(*args): #bug: over-write the old data
    
    date_time = datetime.now().strftime("%d%m%Y%H%M")
    
    df = pd.DataFrame({"Score":[args[0]], "Time":[date_time]})
    df.to_csv("data/score_data.csv", mode="a", header=False)
    

# def a function to draw letter buttons
def draw_button(*args):
    
    window.fill(Designs.bg_color)
        
    display_word = ""
    for _ in args[0]:
        if _ in word_guessed:
            display_word += _ + ""
        else:
            display_word += "_"
    text = Designs.display_word_font.render(display_word, 1, Designs.button_color)
    window.blit(text, (400, 200))
    
    text = Designs.letter_font.render(f"Score: {args[1]}", 1, Designs.text_color)
    window.blit(text, (460, 66))
            
    text = Designs.letter_font.render(f"Max: {args[2]}", 1, Designs.text_color)
    window.blit(text, (590, 66))
        
    for _ in letters:
        x, y, letter, visibility = _
        pygame.draw.circle(window, Designs.button_color, (x, y), RADIUS, 2)
        
        if visibility:
            # to draw the buttons
            pygame.draw.circle(window, Designs.button_color, (x, y), RADIUS, 2)
            text = Designs.letter_font.render(letter, 1, Designs.button_color)
            window.blit(text,(x - text.get_width()/2, y - text.get_height()/2))
            pygame.draw.rect(window,Designs.button_color, space_line, border_radius=10, width=2)
    
    text = Designs.copyright_text_font.render("names source: en.wikipedia.org", 1, Designs.text_color)
    window.blit(text, (36, 580))
    
    window.blit(Designs.images[hangman_stage], (150, 100))
    pygame.display.update()

# def a greeting message when starting the game
def greeting():
    window.fill(Designs.bg_color)
    text = Designs.promt_text_font.render("This hangman game is about guessing", 1, Designs.text_color)
    window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2.8 - text.get_height()/2))
    text = Designs.promt_text_font.render("names in Harry Potter", 1, Designs.text_color)
    window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))    
    
    pygame.display.update()
    pygame.time.delay(3000)
    return True
    
# def a func to display "won" or "killed" messages   
def display_messages(*args):
    pygame.time.delay(1000)
    window.fill(Designs.bg_color)
    
    if args[2] == False:
        text = Designs.promt_text_font.render(args[0], 1, args[1])
        window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2.6 - text.get_height()/2))        
    else:
        text = Designs.promt_text_font.render(args[0], 1, args[1])
        window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2.6 - text.get_height()/2))
        text = Designs.promt_text_font.render(args[2], 1, args[1])
        window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/1.8 - text.get_height()/2))
    
    pygame.display.update()
    pygame.time.delay(3000)
    
    
# def a function to promt keep playing or quit the game
def promt():
    window.fill(Designs.bg_color)
    promt = Designs.promt_text_font.render("'Yes'to play or 'No' to quit?", 1, Designs.text_color)
    window.blit(promt, (WIDTH/2 - promt.get_width()/2, HEIGHT/2.6 - promt.get_height()/2))
    yes = Designs.promt_text_font.render("Yes", 1, Designs.text_color)
    window.blit(yes, (WIDTH/3 - yes.get_width()/2, HEIGHT/1.8 - yes.get_height()/2))
    no = Designs.promt_text_font.render("No", 1, Designs.text_color)
    window.blit(no, (WIDTH*2/3 - no.get_width()/2, HEIGHT/1.8 - no.get_height()/2))
    
    yes_pos = (WIDTH/3 - yes.get_width()/2 + 30, HEIGHT/1.65 - yes.get_height()/2)
    no_pos = (WIDTH*2/3 - no.get_width()/2 + 22, HEIGHT/1.65 - no.get_height()/2)
    
    pygame.draw.circle(window, Designs.text_color, (yes_pos[0], yes_pos[1]), RADIUS + 22, 3)
    pygame.draw.circle(window, Designs.text_color, (no_pos[0], no_pos[1]), RADIUS + 22, 3)
    pygame.display.update()
    
    return yes_pos, no_pos  


# def the main game_play function
def game_play():
    
    WORD = choice(Words.characters_names)    
    print(WORD)
    
    global space_key
    global hangman_stage
    global word_guessed
    global score
        
    hangman_stage = 0
    word_guessed = []
    
    FPS = 60
    clock = pygame.time.Clock()
    run = True
        
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos() # get positions of mouse clicks
                # print(pos_x, pos_y)
                
                for i in letters:
                    x, y, letter, visibility = i
                    if visibility: # to handle the visibility of guessed letters
                        distance = math.sqrt((x - pos_x)**2 + (y - pos_y)**2)
                        
                        if distance < RADIUS:
                            i[3] = False
                            word_guessed.append(letter)
                            if letter not in WORD:
                                hangman_stage += 1
                
        # call the func to draw letter buttons
        try:
            df = pd.read_csv("data/score_data.csv")
            max_score = int(df.iloc[:,[1]].max())
            draw_button(WORD, score, max_score)
        except FileNotFoundError:
            df = pd.DataFrame({"Score":[None],"Time":[None]})
            df.to_csv("data/score_data.csv")
        
        except ValueError: draw_button(WORD, 0, 0)
        
        # to handle the winning or losing in game play            
        won = True         
        for _ in WORD:
            if _ not in word_guessed:
                won = False
                break
        
        if won:
            run = False
            display_messages("Yay, you won!", Designs.text_color, False)
            score += 1
            record_score(score)
            df = pd.read_csv("data/score_data.csv")
            max_score = df.iloc[:,[1]].max()
            draw_button(WORD, score, max_score)
            return score            
        
        if hangman_stage == 6:
            run = False
            display_messages("pOops, you killed the man!", Designs.text_color, f"the word is {WORD}")    
            print(WORD)
            return score         
    