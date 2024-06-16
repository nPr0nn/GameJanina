
import pygame
import time

from threading import Thread
from .World import World

from . import grass 

class Heart():
    def __init__(self) -> None:
        Thread.__init__(self)
        pygame.init()

        # Definir as dimensões da janela
        window_info          = pygame.display.Info() 
        self.WINDOW_WIDTH    = window_info.current_w
        self.WINDOW_HEIGHT   = window_info.current_h
        self.FPS_PADRAO      = 60.0
        self.UPDATE_CAP      = 1.0/self.FPS_PADRAO
        
        # Criar a janela
        self.window      = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), 0, 32)
        scale            = 0.25
        self.screen      = pygame.Surface((self.WINDOW_WIDTH * scale, self.WINDOW_HEIGHT * scale)) 

        gm = grass.GrassManager('assets/grass', tile_size=10, stiffness=600, max_unique=5, place_range=[0, 1])
        gm.enable_ground_shadows(shadow_radius=4, shadow_color=(0, 0, 1), shadow_shift=(1, 2))

        self.world       = World(gm, scale)
        
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
        currTime        = 0
        lastTime        = time.time()  # retorna o tempo atual em segundos
        deltaTime       = 0
        unprocessedTime = 0
        frameTime       = 0
        frames          = 0
        fps             = 0

        while self.running:
            render = False
            currTime   = time.time()
            deltaTime  = currTime - lastTime  # tempo que passou desde a ultima vez que o loop foi executado
            lastTime   = currTime             # atualiza o tempo da ultima vez que o loop foi executado

            unprocessedTime += deltaTime  # tempo nao processado
            frameTime       += deltaTime

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
                self.render(self, deltaTime)
                frames += 1
            else:
                time.sleep(0.001)
                
        self.dispose()
      
    def tick(self): # metodo chamado a cada frame
        self.input()
        self.world.tick()

    def render(self, gc, deltaTime): # metodo chamado a cada frame
        # Limpar a telaa
        self.screen.fill((27,66,52))
        # Renderizar o mapa
        self.world.render(self.screen, deltaTime)
       
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
                    self.world.input("A")
                if event.key == pygame.K_s:
                    self.world.input("S")
                if event.key == pygame.K_d:
                    self.world.input("D")
                if event.key == pygame.K_w:
                    self.world.input("W")
                # se apertar shift esquerdo
                if event.key == pygame.K_LSHIFT:
                    self.world.input("SHIFT")
                
            # se uma tecla foi solta
            if event.type == pygame.KEYUP:
                # se a tecla foi A
                if event.key == pygame.K_a:
                    self.world.input("a")
                if event.key == pygame.K_s:
                    self.world.input("s")
                if event.key == pygame.K_d:
                    self.world.input("d")
                if event.key == pygame.K_w:
                    self.world.input("w")
                if event.key == pygame.K_LSHIFT:
                    self.world.input("shift")

    def dispose(self): # metodo chamado quando o jogo fecha
            pass
