from jogador import Jogador

from caixa_de_colisao import CaixaColisao

class Mapa():
    def __init__(self):
        self.entidades = []
        self.jogador   = Jogador()
        self.entidades.append(self.jogador)

        box = CaixaColisao((100, 100), (100, 100))
        self.entidades.append(box)
 
    def render(self, screen):
        for entidade in self.entidades:
            entidade.render(screen)

    def tick(self):
        for entidade in self.entidades:
            entidade.tick()
    
    def input(self, tecla):
        self.jogador.input(tecla)
