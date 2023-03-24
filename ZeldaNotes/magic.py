# Büyüler

# Flame büyüsü hasar verdiği için yine attack sprites içerisinde olacak.

# Heal büyüsü ise sadece birkaç particle çıkarıp player canını bir miktar yükseltecek.

# Flame büyüsü için player'ın yönüne göre 5 tane yan yana ateş sprite'ı oluşacak ve bu ateş spritelarına
# her birine ayrı rastgele bir offset vereceğiz ki daha doğal dursun.

import pygame
from settings import *
from random import randint

class MagicPlayer():
  def __init__(self,animation_player): # particle efektlerini tutacak animation_player'ı aldık.
    self.animation_player = animation_player

    # Sesler
    self.sounds = {
        'heal': pygame.mixer.Sound('audio/heal.wav'), # Heal sesi
        'flame': pygame.mixer.Sound('audio/Fire.wav') # Flame sesi
    }

  def heal(self,player,strength,cost,groups): # Heal büyüsü için bir fonksiyon yapıyoruz.
    # player ile player'ın canını artıracağımız için ihtiyaç duyuyoruz.
    # strength
    # cost ile büyü maliyetine bakıyoruz.
    # groups ile hangi gruplarda olduğuna bakacağız.
    if player.energy >= cost: # Eğer karakterin enerjisi yetiyorsa çağırabiliriz büyüyü.
      self.sounds['heal'].play() # heal sesini çağır.

      player.health += strength # karakterin canını büyünün gücü kadar arttırıyoruz.
      player.energy -= cost # Karakterin enerjisini büyü maliyeti kadar azaltıyoruz.
      if player.health >= player.stats['health']: # Eğer karakterin canı 100 üstüne çıkarsa
        player.health = player.stats['health'] # Player canını maks can yap

    # particles
      self.animation_player.create_particles('aura',player.rect.center,groups)
      # create_particles 3 parametre alıyor. aura animasyon türü ve dict içerisinden alıyoruz.(Particles içerisinden). ikinci parametre ile konumunu veriyoruz ve hangi grupta olacağını veriyoruz.
      self.animation_player.create_particles('heal',player.rect.center,groups)
      # Ve iyileşme animasyonumuzu da alıyoruz.

  def flame(self,player,cost,groups): # Flame büyüsü için bir fonksiyon yazıyoruz.
    # Bu metodu Level içerisinde create_magic içerisinde çağıracağız.
    if player.energy >= cost: # Eğer enerjimiz yeterli ise,
      self.sounds['flame'].play() # flame sesini çal.
      player.energy -= cost # Enerjiyi bu kadar azalt

      if player.status.split("_")[0] == "right": # Eğer sağa dönük isek
        direction = pygame.math.Vector2(1,0) # Sağ vektör
      elif player.status.split("_")[0] == "left": # Eğer sola dönük isek
        direction = pygame.math.Vector2(-1,0) # Sol vektör
      elif player.status.split("_")[0] == "up": # Eğer yukarı dönük isek
        direction = pygame.math.Vector2(0,-1) # Yukarı vektör
      else: # Eğer aşağı dönük isek
        direction = pygame.math.Vector2(0,1) # Aşağı vektör

      # Yan yana 5 ateş oluşturmak için aşağıdaki i değerini kullanacağız.
      # Örneğin sana doğru oluşturmak istiyoruz. Ve direction'ımız (1,0)
      # Önce bu direction'ı i ile çarpacağız ve ardından da TILESIZE ile çarpacağız ve yan yana 5 ateş oluşacak.

      for i in range(1,6): # 5 adet ateş oluşturacağız. Bu i değişkeni ile offset vereceğimiz için 1'den başlattık.
        if direction.x: # Horizontal (yatay eksende) Yani direction'ın x değeri 0'dan farklı ise
          offset_x = (direction.x * i) * TILESIZE  # Yan yana oluşturacak olan offset
          x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3) # Her bir flame'in x pozisyonu. Player'ın merkezinin x'i + offset'in x'i kadar olmalı. Ayrıca random bir offset daha veriyoruz ki tahmin edilebilir olmasın.
          y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3) # Her bir flame'in y pozisyonu. Ayrıca random bir offset daha veriyoruz ki tahmin edilebilir olmasın.
          self.animation_player.create_particles('flame',(x,y),groups) # Ve animasyonunu oluşturuyoruz.
          # dict içerisinden 'flame' i alacağız.
          # Konum olarak x ve y'yi verdik.
          # Grup olarak da parametreden gelen değeri veriyoruz.

        else: # Vertical (dikey eksende ise) yani x değeri 0 ise.
          offset_y = (direction.y * i) * TILESIZE  # Yan yana oluşturacak olan offset
          x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3) # Her bir flame'in x pozisyonu. Player'ın merkezinin x'i + offset'in x'i kadar olmalı. Ayrıca random bir offset daha veriyoruz ki tahmin edilebilir olmasın.
          y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3) # Her bir flame'in y pozisyonu. Ayrıca random bir offset daha veriyoruz ki tahmin edilebilir olmasın.
          self.animation_player.create_particles('flame',(x,y),groups) # Ve animasyonunu oluşturuyoruz.
          # dict içerisinden 'flame' i alacağız.
          # Konum olarak x ve y'yi verdik.
          # Grup olarak da parametreden gelen değeri veriyoruz.