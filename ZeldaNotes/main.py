# Main

import pygame, sys
from settings import *
from level import Level

class Game:
  def __init__(self):

    # Genel ayarlar.
    pygame.init() # Pygame modülünü başlatıyoruz.
    self.screen = pygame.display.set_mode((WIDTH,HEIGHT)) # Bir ekran oluşturuyoruz.
    pygame.display.set_caption("ZeldaLike") # Pencere ismini veriyoruz.
    self.clock = pygame.time.Clock() # bir Clock nesnesi oluşturuyoruz.

    self.level = Level() # Bir level nesnesi oluşturuyoruz.

    # Ses
    main_sound = pygame.mixer.Sound('audio/main.ogg') # Arkaplan şarkısını oluşturduk.
    main_sound.set_volume(0.5) # Ve sesi ayarlıyoruz.
    main_sound.play(loops = -1) # Ve sonsuz çalmasını sağlıyoruz.

  def run(self): # Oyun sürerken gerçekleşecekleri yazacağımız metot.
    while True: # Sonsuz döngü
      for event in pygame.event.get(): # Tüm olayları getiriyoruz.
        if event.type == pygame.QUIT: # Eğer olayımız çıkış yapmaksa
          pygame.quit() # pygame'den çıkış yapıyoruz.
          sys.exit() # Ve tüm dosyalardan çıkış yapıyoruz.
        if event.type == pygame.KEYDOWN: # Eğer herhangi bir tuşa basıyorsak.
          if event.key == pygame.K_m: # Ve klavyede m tuşuna basıyorsak.
            self.level.toggle_menu() # Level içerisindeki toggle_menu metodunu çalıştır.

      self.screen.fill(WATER_COLOR) # Ekranı deniz rengine boyuyoruz ki çok kenara gidersek siyahlık görmeyelim.
      self.level.run() # level objesinden run metotunu çalıştırıyoruz. (Oyunu çizecek)
      pygame.display.update() # Update metodu ile ekranı sürekli güncelliyoruz.
      self.clock.tick(FPS) # Fps i veriyoruz. (Genelde 60 idealdir.)

if __name__ == "__main__": # Eğer main dosyasında isek
  game = Game() # bir oyun objesi oluştur
  game.run() # ve run metodunu çalıştır.