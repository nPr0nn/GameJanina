import pygame 

class CaixaColisao():
    def __init__(self, pos, dim, color=(0,0,0)):
        self.pos   = pos
        self.dim   = dim
        self.color = color 

    def tick(self):
        pass

    def render(self, screen):
        rect = pygame.Rect(self.pos[0] - self.dim[0]/2, self.pos[1] - self.dim[1]/2, self.dim[0], self.dim[1])
        pygame.draw.rect(screen, self.color, rect, width=2) 
        pass
