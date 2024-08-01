import pygame

class Button:
    def __init__(self, x, y, sx, sy, bcolour, fbcolour,
                 font, fcolour, text):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.fontsize = 25
        self.bcolour = bcolour
        self.fbcolour = fbcolour
        self.fcolour = fcolour
        self.text = text
        self.CurrentState = False
        self.buttonf = pygame.font.SysFont(font,
                                       self.fontsize)
 
    def showButton(self, display):
        if(self.CurrentState):
            pygame.draw.rect(display, self.fbcolour,
                         (self.x, self.y, self.sx, self.sy))
        else:
            pygame.draw.rect(display, self.fbcolour,
                         (self.x, self.y, self.sx, self.sy))
        textsurface = self.buttonf.render(self.text,
                                          False, 
                                          self.fcolour)
        display.blit(textsurface, ((self.x + (self.sx/2) -
                                    (self.fontsize/2)*(len(self.text)/2)
                                    - 5, (self.y + (self.sy/2)
                                          - (self.fontsize/2)-4))))
 
    def focusCheck(self, mousepos, mouseclick):
        if(mousepos[0] >= self.x and mousepos[0]
            <= self.x + self.sx and mousepos[1] >= self.y
                and mousepos[1] <= self.y + self.sy):
            self.CurrentState = True
            return mouseclick[0]
 
        else:
            self.CurrentState = False
            return False