import pygame
from threading import Thread
import time
from mapa import Mapa

class Coracao():
    def __init__(self) -> None:
        Thread.__init__(self)
        pygame.init()

        # Definir as dimensões da janela
        window_info          = pygame.display.Info() 
        self.WINDOW_WIDTH    = window_info.current_w * 0.5
        self.WINDOW_HEIGHT   = window_info.current_h * 0.5
        self.FPS_PADRAO      = 60.0
        self.UPDATE_CAP      = 1.0/self.FPS_PADRAO
        self.mapa            = Mapa()
        
        # Criar a janela
        self.window      = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.screen      = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT)) 
        pygame.display.set_caption("Game Janina")
        Thread(self.run())

    def toggle_fullscreen(self):
        window_info   = pygame.display.Info()
        is_fullscreen = self.window.get_flags() & pygame.FULLSCREEN
        if is_fullscreen:
            pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT)) 
        else:
            pygame.display.set_mode((window_info.current_w, window_info.current_h), pygame.FULLSCREEN)
        
    def run(self):
        self.running    = True
        render          = False
        firstTime       = 0
        lastTime        = time.time()  # retorna o tempo atual em segundos
        passedTime      = 0
        unprocessedTime = 0
        frameTime       = 0
        frames          = 0
        fps             = 0

        while self.running:
            render = False
            firstTime  = time.time()
            passedTime = firstTime - lastTime  # tempo que passou desde a ultima vez que o loop foi executado
            lastTime   = firstTime             # atualiza o tempo da ultima vez que o loop foi executado

            unprocessedTime += passedTime  # tempo nao processado
            frameTime += passedTime

            # enquanto nao processou td q deveria (devido a lag em render ou coisas assim)
            while unprocessedTime >= self.UPDATE_CAP:
                # Isso garante que o tempo de atualizacao seja constante
                # e nao dependa do tempo de renderizacao. Igualando o 
                # jogo para todos os computadores, apenas aumentando o
                # fps para computadores mais potentes
                unprocessedTime -= self.UPDATE_CAP  # Tempo comido
                render = True

                self.tick()

                if frameTime >= 1.0:
                    frameTime = 0
                    fps       = frames
                    frames    = 0
                    # print("FPS: " + str(fps))

            # Depois de processar o tempo, renderiza
            if render:
                self.render(self)
                frames += 1
            else:
                time.sleep(0.001)
                
        self.dispose()
      
    def tick(self): # metodo chamado a cada frame
        self.input()
        self.mapa.tick()

    def render(self, gc): # metodo chamado a cada frame
        # Limpar a telaa
        self.screen.fill((255,255,255))
        # Renderizar o mapa
        self.mapa.render(self.screen)
       
        window_info     = pygame.display.Info() 
        resized_surface = pygame.transform.scale(self.screen, (window_info.current_w, window_info.current_h)) 

        self.window.blit(resized_surface, (0,0))

        # Atualizar a tela
        pygame.display.update()

    def input(self):
        # Verificar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.toggle_fullscreen()
            
            # se uma tecla foi pressionada
            if event.type == pygame.KEYDOWN:
                # se a tecla foi A
                if event.key == pygame.K_a:
                    self.mapa.input("A")
                if event.key == pygame.K_s:
                    self.mapa.input("S")
                if event.key == pygame.K_d:
                    self.mapa.input("D")
                if event.key == pygame.K_w:
                    self.mapa.input("W")
                # se apertar shift esquerdo
                if event.key == pygame.K_LSHIFT:
                    self.mapa.input("SHIFT")
                
            # se uma tecla foi solta
            if event.type == pygame.KEYUP:
                # se a tecla foi A
                if event.key == pygame.K_a:
                    self.mapa.input("a")
                if event.key == pygame.K_s:
                    self.mapa.input("s")
                if event.key == pygame.K_d:
                    self.mapa.input("d")
                if event.key == pygame.K_w:
                    self.mapa.input("w")
                if event.key == pygame.K_LSHIFT:
                    self.mapa.input("shift")

    def dispose(self): # metodo chamado quando o jogo fecha
            pass

Coracao()
