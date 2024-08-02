import pygame
from pygame.locals import *

class CreditsScreen:
    def __init__(self, game: pygame.Surface):
        self.game = game
        pygame.mixer.init()
        pygame.mixer.music.load("./resources/audio/music/New_Synthwave.wav")
        pygame.mixer.music.play()
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        self.clock = pygame.time.Clock()
        self.texts = []
        self.initialize_credits()
        
    def initialize_credits(self):
        credits_list = ["Мир грифонов"," ---------- ","Разработка - Станислав Лапутин", "Руководитель - Екатерина Евдокимова", " ---------- ", "Музыка", " --- ", "Станислав Лапутин - Stasis",
                        "Станислав Лапутин - tutorial", "Станислав Лапутин - BAP2HA",
                    "Kevin MacLeod - Cipher", "Kevin MacLeod - Darkest Child", "Kevin MacLeod - Divertissement Pizzicato", "Cerror - Maandban", "coda - test1.nsf", "RednGreen - Cursed Cathedral",
                    "Ein Fall Fur Zwei Theme (1981)", "Lost Transmission (SNES original)", "RushJet1","Entering Graciously", "4mat - Empty", "DubMood - Team Haze Chiptune", " ", "---", " ",
                    "Спасибо за игру!", " ", "2024","",""]
        for i, line in enumerate(credits_list):
            s = self.font.render(line, 1, (255, 255, 255))
            r = s.get_rect(centerx=self.game.get_rect().centerx, y=self.game.get_height() + i * 45)
            self.texts.append((r, s))
        
    def handle_mouse_click(self, pos: tuple[int, int]):
        if 100 < pos[0] < 200 and 100 < pos[1] < 200:
            self.game.switch_screen(self.game.second_screen)

    def draw(self):
        self.game.fill(pygame.Color('#000000'))

        for r, s in self.texts:
            r.move_ip(0, -1)
            self.game.blit(s, r)

        if all(r.bottom < 0 for r, s in self.texts):
            return True

        self.clock.tick(60)
        return False