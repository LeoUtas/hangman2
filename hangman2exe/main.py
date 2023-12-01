import pygame, sys, math
from functions import game_play, RADIUS, promt, letters, greeting
from random import choice
from elements import Words

pygame.init()
greeting()

while True:
    
    for _ in range(0,len(letters)):
        letters[_][3] = True
    yes_pos, no_pos = promt()
    
    for event in pygame.event.get():            
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_x, pos_y = pygame.mouse.get_pos()
                                
            distance_yes = math.sqrt((yes_pos[0] - pos_x)**2 + (yes_pos[1] - pos_y)**2)
            distance_no = math.sqrt((no_pos[0] - pos_x)**2 + (no_pos[1] - pos_y)**2)
                            
            if distance_yes < RADIUS + 22:
                WORD = choice(Words.characters_names)
                score = game_play()
                # print(score)                
                                
            elif distance_no < RADIUS + 22:
                pygame.quit()
                sys.exit()   
