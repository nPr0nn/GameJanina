import time
import pygame

from caixa_de_colisao import CaixaColisao 

class Jogador():
    def __init__(self):
        self.pos = [0,0] # x, y
        self.vel = [0,0] # velx, vely
        self.velPadrao = 5
        self.pressionados = {'A':0, 'S':0, 'D':0, 'W':0, 'a':0, 's':0, 'd':0, 'w':0}

        self.colBox = CaixaColisao((self.pos[0], self.pos[1]), (60, 60), (0,255,0))
        
    def tick(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[0] = 0
        self.vel[1] = 0

        if self.pressionados['A'] == 1:
            self.vel[0] -= self.velPadrao
        if self.pressionados['D'] == 1:
            self.vel[0] += self.velPadrao
        if self.pressionados['W'] == 1:
            self.vel[1] -= self.velPadrao
        if self.pressionados['S'] == 1:
            self.vel[1] += self.velPadrao

        self.colBox.pos = self.pos

    def render(self, screen):
        radius = 5
        pygame.draw.circle(screen, (0,0,0), self.pos, radius, 0)
        self.colBox.render(screen)
        pass

    def input(self, tecla: str):
        if tecla.isupper():
            self.pressionados[tecla]         = 1
            self.pressionados[tecla.lower()] = 0
        if tecla.islower():
            self.pressionados[tecla]         = 1
            self.pressionados[tecla.upper()] = 0 
