import pygame
import pygame.examples
from pygame.locals import *
from sys import exit
from os import path
from random import randint, randrange


pygame.init()

largura = 640
altura = 480

tela = pygame.display.set_mode((largura,altura))
branco = (255,255,255)

relogio = pygame.time.Clock()
titulo = pygame.display.set_caption('Dino Game')

diretorio_principal = path.dirname(__file__)
diretorio_spritesheet = path.join(diretorio_principal, 'spritesheet')
diretorio_soms = path.join(diretorio_principal, 'soms')


spritesheet = pygame.image.load(path.join(diretorio_spritesheet, 'dinoSpritesheet.png'))
spritesheet.convert_alpha()

class Dino(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(path.join(diretorio_soms, 'jump_sound.wav'))
        self.som_pulo.set_volume(1)
        
        self.imgs_dino = []
        self.add_img_dino()
        
        self.index = 0
        self.image = self.imgs_dino[self.index]
        self.rect = self.image.get_rect()
        self.rect.y = 368
        self.rect.x = 130
        self.pulo = False
        self.desce = False
        

    def add_img_dino(self):
        for i in range(3):
            
            #spritesheet.subsurface serve para separar as imgs
            #o primeiro parametro é a posição da img e o segundo é o tamanho da img
            img = spritesheet.subsurface((i * 32,0), (32,32))
            img = pygame.transform.scale(img, (32*3,32*3))
            self.imgs_dino.append(img)
            
    def pular(self):
        self.pulo = True
        self.som_pulo.play()
        
    def update(self):
        
        if self.pulo:
            self.rect.y -= 20
            if self.rect.y <= 200:
                self.pulo = False
                self.desce = True
                
        if self.desce:
            self.rect.y += 20
            if self.rect.y == 368:
                self.pulo = False
                self.desce = False
                
                
        self.index += 0.25
        
        if self.index > 2:
            self.index = 0
        
        
        self.image = self.imgs_dino[int(self.index)]
        
class Nuvem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.subsurface((224,0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*3,32*3))

        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = largura - randrange(30, 300, 90)

    def update(self):
        self.rect.x -= 20
        if self.rect.topright[0] <= 0:
            self.rect.x = 640
            self.rect.y = randrange(50, 200, 50)
            
class Chao(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.subsurface((192,0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*3,32*3))

        self.rect = self.image.get_rect()
        self.rect.y = 400
        self.rect.x = x

    def update(self):
        self.rect.x -= 20
        if self.rect.topright[0] <= 0:
            self.rect.x = 640       
        

todas_sprites = pygame.sprite.Group()
dino = Dino()

for i in range(4):
    nuvem = Nuvem()
    todas_sprites.add(nuvem)
    
for i in range(20):
    chao = Chao(i*32)
    todas_sprites.add(chao)

todas_sprites.add(dino)



while True:
    
    relogio.tick(20)
    tela.fill(branco)
    for event in pygame.event.get():
        if event.type ==  QUIT:
            pygame.quit()
            exit()
            
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if dino.rect.y == 368:
                    dino.pular()
        
        
    todas_sprites.draw(tela)
    todas_sprites.update()
    
    pygame.display.flip()