# Entity dosyası

# Bu dosya içerisinde düşmanlar ve karakter için aynı olan move ve collision metotlarını entity class'ı içerisine alıp ikisi için de kullanacağız.

import pygame
from math import sin

class Entity(pygame.sprite.Sprite): # Entity class'ımızı oluşturuyoruz ve kalıtımını Sprite'lardan almasını istiyoruz.
  def __init__(self,groups): # init metodumuzu yazıyoruz.
    super().__init__(groups) # sprite sınıfını initialize ediyoruz.
    self.frame_index = 0
    self.animation_speed = 0.15
    self.direction = pygame.math.Vector2()
  
  def move(self,speed): # Entity'nin yürümesini sağlayacak metodu oluşturuyoruz.
    # speed parametresi entity'nin hızı olacak.

    # Fakat (1,1) gibi çift yönlü durumlarda entity aşırı hızlı gidiyor bu sebeple bu hızı normalleştirmemiz gerek:

    if self.direction.magnitude() != 0: # Direction'ımızın bir değeri olup olmadığına bakıyoruz.(x ve y vektörleri için)
      self.direction = self.direction.normalize() # Eğer öyleyse bu hızı normalleştiriyoruz.(0.7 gibi bir değer)

     # self.rect.center += self.direction * speed # entity rectangle'ının merkezini her saniye entitynin directionını, entity hızı ile çarpıp ekliyoruz.
    # Bu şekilde eğer yönümüz sola (-1,0) ise hız 5 ise (-5,0) kordinatlarına taşıyor ve hızlıca entityi çiziyoruz. Böylece entity hareket ediyor.

    # 1- # Yönleri ayırdık çünkü hangi yönder çarpışma olduğunu bilmek istiyoruz.
    """
      self.rect.x += self.direction.x * speed # entity rect'inin x konumuna direction * speed ekliyoruz.
      self.collision('horizontal') # Yatay çarpışmanın kontrolünü yapıyoruz.
      self.rect.y += self.direction.y * speed # entity rect'inin y konumuna direction * speed ekliyoruz.
      self.collision('vertical') # Dikey çarpışmanın kontrolünü yapıyoruz.
    """    
    # 2- # rect'leri hitboxlar ile değiştiriyoruz.

    self.hitbox.x += self.direction.x * speed # entity hitbox'inin x konumuna direction * speed ekliyoruz.
    self.collision('horizontal') # Yatay çarpışmanın kontrolünü yapıyoruz.
    self.hitbox.y += self.direction.y * speed # entity hitbox'inin y konumuna direction * speed ekliyoruz.
    self.collision('vertical') # Dikey çarpışmanın kontrolünü yapıyoruz.
    # Yönleri ayırdık çünkü hangi yönder çarpışma olduğunu bilmek istiyoruz.
    self.rect.center = self.hitbox.center # Rect'in merkeziyle hitbox'ın merkezini aynı yere koyduk ve ayarladık.

  def collision(self,direction): # Çarpışmaları gerçekleştirecek metodu yazıyoruz.
    # direction parametresi ile çarpışmanın hangi yönden olduğuna bakıyoruz.

  # 1- 
    """
    if direction == 'horizontal': # Eğer yatay eksendeysek.
      for sprite in self.obstacle_sprites: # obstacle_sprites grubundaki her bir sprite için
        if sprite.rect.colliderect(self.rect): # Eğer sprite karakterimiz ile çarpışıyorsa.
          if self.direction.x > 0: # Eğer entity yönü sağa doğruysa
            self.rect.right = sprite.rect.left # Çarpışmadan sonra entity rect'inin sağ tarafı, çarptığımız nesnenin rect'inin sol tarafının konumunda olmalı.
          if self.direction.x < 0: # Eğer karakterimiz sola doğruysa
            self.rect.left = sprite.rect.right # Çarpışmadan sonra entity rect'inin sol tarafı, çarptığımız nesnenin rect'inin sağ tarafının konumunda olmalı.
    
    if direction == 'vertical': # Eğer dikey eksendeysek.
      for sprite in self.obstacle_sprites: # obstacle_sprites grubundaki her bir sprite için
        if sprite.rect.colliderect(self.rect): # Eğer sprite entity ile çarpışıyorsa.
          if self.direction.y > 0: # Eğer entity yönü aşağı doğruysa
            self.rect.bottom = sprite.rect.top # Çarpışmadan sonra entity rect'inin alt tarafı, çarptığımız nesnenin rect'inin üst tarafının konumunda olmalı.
          if self.direction.y < 0: # Eğer entity yukarı doğruysa
            self.rect.top = sprite.rect.bottom # Çarpışmadan sonra entity rect'inin üst tarafı, çarptığımız nesnenin rect'inin alt tarafının konumunda olmalı.
    """
  # 2- rect'leri hitbox ile değiştirdik ki overlap yapabilelim.
    
    if direction == 'horizontal': # Eğer yatay eksendeysek.
      for sprite in self.obstacle_sprites: # obstacle_sprites grubundaki her bir sprite için
        if sprite.hitbox.colliderect(self.hitbox): # Eğer sprite entity hitboxı ile çarpışıyorsa.
          if self.direction.x > 0: # Eğer entity yönü sağa doğruysa
            self.hitbox.right = sprite.hitbox.left # Çarpışmadan sonra entity hitbox'ının sağ tarafı, çarptığımız nesnenin hitbox'inin sol tarafının konumunda olmalı.
          if self.direction.x < 0: # Eğer karakterimiz sola doğruysa
            self.hitbox.left = sprite.hitbox.right # Çarpışmadan sonra entity hitbox'inin sol tarafı, çarptığımız nesnenin hitbox'inin sağ tarafının konumunda olmalı.
    
    if direction == 'vertical': # Eğer dikey eksendeysek.
      for sprite in self.obstacle_sprites: # obstacle_sprites grubundaki her bir sprite için
        if sprite.hitbox.colliderect(self.hitbox): # Eğer sprite karakterimiz ile çarpışıyorsa.
          if self.direction.y > 0: # Eğer entity yönü aşağı doğruysa
            self.hitbox.bottom = sprite.hitbox.top # Çarpışmadan sonra entity hitbox'inin alt tarafı, çarptığımız nesnenin hitbox'inin üst tarafının konumunda olmalı.
          if self.direction.y < 0: # Eğer karakterimiz yukarı doğruysa
            self.hitbox.top = sprite.hitbox.bottom # Çarpışmadan sonra entity hitbox'inin üst tarafı, çarptığımız nesnenin hitbox'inin alt tarafının konumunda olmalı.

  def wave_value(self): # Entity'lerin hasar alınca transparan duruma geçmesi için gerekli olan alpha değerini 0-255 değeri arasında değiştiren metot.
    # alpha değeri için sinus dalgasını kullanacağız. Sinüs dalgası pozxitif değer alırken 255, negatif değer alırken 0 değerini alacak.
    value = sin(pygame.time.get_ticks()) # Zaman geçtikçe bir sinüs değeri alıyoruz.
    if value >= 0: # Eğer bu değer 0'dan büyükse
      return 255 # 255 döndür
    else: # Eğer 0'dan küçükse
      return 0 # 0 döndür.