import pygame, requests as rq, numpy as np
from bs4 import BeautifulSoup

pygame.init()

class Words:

    endpoint = [
        "https://en.wikipedia.org/wiki/List_of_Harry_Potter_characters#Characters_by_surname"    
    ]
    response = rq.get(endpoint[0])

    the_soup = BeautifulSoup(response.text, "html.parser")
    found_names = the_soup.find_all("a", {"class":"mw-redirect"})

    names = []

    for _ in found_names:
        names.append(_.text)

    filtered_names = np.unique(np.array(names))
    filtered_names = [_ for _ in filtered_names if len(_) < 20]
    filtered_names = [_ for _ in filtered_names if "independent" not in _]
    filtered_names = [_ for _ in filtered_names if "." not in _]
    filtered_names = [_ for _ in filtered_names if "'" not in _]
    filtered_names = [_ for _ in filtered_names if not _[0].islower()]
    
    characters_names = [_.upper() for _ in filtered_names]


class Designs:
    # set up 6 images of hangman
    images = []
    for _ in range(7):
        image = pygame.image.load("images\hangman" + str(_) + ".png")
        images.append(image)
    
    # font    
    letter_font = pygame.font.SysFont("comicsans", 28)
    display_word_font = pygame.font.SysFont("comicsans", 32)
    promt_text_font = pygame.font.SysFont("comicsans", 38)
    copyright_text_font = pygame.font.SysFont("comicsans", 12)
        
    # color
    bg_color = (255,255,255)
    button_color = (60, 62, 69)
    text_color = (0, 0 ,0)
    