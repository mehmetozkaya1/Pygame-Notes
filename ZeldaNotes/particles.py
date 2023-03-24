# Patiküller

import pygame
from support import import_folder
from random import choice

class AnimationPlayer:
  def __init__(self):
    self.frames = {
			# Büyü animasyonları
			'flame': import_folder('graphics/particles/flame/frames'), # flame büyüsü efektleri
			'aura': import_folder('graphics/particles/aura'), # aura büyüsü efektleri
			'heal': import_folder('graphics/particles/heal/frames'), # heal büyüsü efektleri
			
			# Saldırı animasyonları 
			'claw': import_folder('graphics/particles/claw'), # Claw atağı animasyonları
			'slash': import_folder('graphics/particles/slash'), # slash atağı animasyonları
			'sparkle': import_folder('graphics/particles/sparkle'), # sparkle atağı animasyonları
			'leaf_attack': import_folder('graphics/particles/leaf_attack'), # leaf_attack atağı animasyonları
			'thunder': import_folder('graphics/particles/thunder'), # thunder atağı animasyonları

			# Canavar ölüm animasyonları
			'squid': import_folder('graphics/particles/smoke_orange'),
			'raccoon': import_folder('graphics/particles/raccoon'),
			'spirit': import_folder('graphics/particles/nova'),
			'bamboo': import_folder('graphics/particles/bamboo'),
			
			# Yapraklar yokolma animasyonları 
			'leaf': (
				import_folder('graphics/particles/leaf1'),
				import_folder('graphics/particles/leaf2'),
				import_folder('graphics/particles/leaf3'),
				import_folder('graphics/particles/leaf4'),
				import_folder('graphics/particles/leaf5'),
				import_folder('graphics/particles/leaf6'),
				self.reflect_images(import_folder('graphics/particles/leaf1')),
				self.reflect_images(import_folder('graphics/particles/leaf2')),
				self.reflect_images(import_folder('graphics/particles/leaf3')),
				self.reflect_images(import_folder('graphics/particles/leaf4')),
				self.reflect_images(import_folder('graphics/particles/leaf5')),
				self.reflect_images(import_folder('graphics/particles/leaf6'))
				)
			}
    # pygame bir şeyi yok ettiğikten sonra yeniden import ederken oyunu oldukça yavaşlatır. Bu nedenle yeni bir class oluşturduk.

  def reflect_images(self,frames):
    new_frames = [] # Dönmüş frame'leri tutan bir liste oluşturduk.
    for frame in frames: # Frames içerisindeki her bir frame için.
    # Bu frames ise yukarıdaki dict içerisinde tek tek yüklediğimiz animasyonlar için verildi.
      flipped_frame = pygame.transform.flip(frame,True,False) # Flip metodu bir nesneyi döndürmeye yarıyor.
      # True x ekseninde döndürmek için, False ise y ekseninde döndürmemek için verildi.
      new_frames.append(flipped_frame) # Dönmüş frame'leri listeye ekliyoruz.
    return new_frames # Ve bu listeyi döndürüyoruz.

  def create_grass_particles(self,pos,groups):
    animation_frames = choice(self.frames['leaf']) # animasyon frame'i olarak yukarıdaki dict içerisinden, leaf tuple'ından rastgele bir liste seçiyoruz.

    ParticleEffect(pos,animation_frames,groups) # Bir partikül efekti oluşturuyoruz.
    # Partikül efekti için position'ı Level içerisinde grass yok olurken verdik.(hedef sprite merkez konumu)
    # animation frames için de yukarıda rastgele bir seçim yaptık ve bir liste aldık.
    # groups ise Level içerisinde visible_sprites olarak verdik ki görebilelim.
    # Paritcle effect ise bunları kullanıp animasyonu gerçekleştirecek.

  def create_particles(self,animation_type,pos,groups): # Karakterin ne tür bir hasar aldığına bağlı olarak oluşacak animasyon metodu.
    animation_frames = self.frames[animation_type] # Yukarıdaki dict içerisinden animasyon türüne göre bir liste getireceğiz. Framelerden oluşan
    ParticleEffect(pos,animation_frames,groups) # Ve particleEffect classından çağırıyorum.
  # Enemies içerisinde actions kısmında her saldırı yapıldığında damage_player çağırılıyor. Ve damage player 2 parametre alıyor. Biri hasar diğeri de hasar türü. Biz hasar türünü kullanacağız.

class ParticleEffect(pygame.sprite.Sprite): # Partiküllerin bulunacağı sınıf
  def __init__(self,pos,animation_frames,groups):
    # pos partikülün konumunu belirtecek.
    # animation_frames ise her bir partikülün oluşması için gereken frame'ler
    # groups ise hangi grupta bulunacağı. 
    super().__init__(groups) # Sprite class'ını init ediyoruz.
    self.sprite_type = 'magic' # Düşman hasar aldığında Enemy içerisindeki get_damage metodu çalışıyor fakat büyülerimizin sprite_type'ı yok. Bu nedenle burada bir sprite_type oluşturduk.
    self.frame_index = 0 # Her bir frame'i dönecek olan index'imiz.
    self.animation_speed = 0.15 # Her bir frame'i dönme hızımız.
    self.frames = animation_frames # Animasyon frame'lerini tutan değişken
    self.image = self.frames[self.frame_index] # Ve animasyon frame'i için aldığımız frame içerisinden frame indeximiz ile sırayla seçiyoruz.
    self.rect = self.image.get_rect(center = pos) # Ve frame'lerin rect'ini oluşturuyoruz. Ve rect'in konumu her birinin merkezi olacak.

  def animate(self): # Animasyonları gerçekleştirecek metot.
    self.frame_index += self.animation_speed # Animasyon geçiş hızını frame index'imize ekliyoruz.
    if self.frame_index >= len(self.frames): # Eğer indeksimiz listemizin uzunluğunun üstüne çıkarsa 
      self.kill() # O sprite'ı kaldıracağız.
    else: # Eğer çıkmaz ise
      self.image = self.frames[int(self.frame_index)] # Fotoğraf olarak frames'ler içerisinden index ile seçeceğiz.
    
  def update(self): # partiküllerin durumunu güncelleyen metot.
    self.animate() # Animasyonları çağırıyoruz.