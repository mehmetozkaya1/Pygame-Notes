# Tile class'ı ile oyundaki ağaç taş gibi nesneleri oluşturacağız
# Oyuna gerçekçilik katmak için overlap(üst üste gelme) yapmamız gerekiyor. Bunun için 2 farklı alan oluşturacağız.
# İlk alan direkt bizim full rect'imiz, ikincisi ise hitbox alanımız olacak. Hitboxları y ekseninden küçülterek üst üste binmeyi sağlayabiliriz.

import pygame 
from settings import *

# 1- Tile class'ının eski hali
"""
class Tile(pygame.sprite.Sprite): # Tile class'ı bir sprite olacağı için ordan kalıtım aldık.
  def __init__(self,pos,groups): # Ayrıca pozisyon parametresi alıyoruz nereye yerleştireceğimizi bilmek için
    # groups ile Tile objesinin hangi grupta olduğuna bakabiliriz.
    super().__init__(groups) # Sprite class'ını da initialize ediyoruz. 
    self.image = pygame.image.load('graphics/test/rock.png').convert_alpha() # Ekrana çizeceğimiz Tile objesinin resmi için bir değişken oluşturuyor ve bir fotoğraf yüklüyoruz.
    self.rect = self.image.get_rect(topleft = pos) # Ekrana çizeceğimiz Tile objesinin bir temas alanını yaratıyoruz. # Bu bizim çizim için kullandığımız alan olacak.
    # Aldığımız position ile de konumunu ayarlıyoruz.
    self.hitbox = self.rect.inflate(0,-10) # inflate metodu verilen değerler kadar rect'i küçültür. Bu örnekte -5 birim yukarı -5 birim aşağıdan kısaltarak x eksenine dokunmayacağız.
"""
# 2- Tile classını daha esnek hale getiriyoruz.

class Tile(pygame.sprite.Sprite): # Tile class'ı bir sprite olacağı için ordan kalıtım aldık.
  def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))): # Ayrıca pozisyon parametresi alıyoruz nereye yerleştireceğimizi bilmek için
    # groups ile Tile objesinin hangi grupta olduğuna bakabiliriz.
    # sprite type ile hangi türden bir sprite olduğunu kontrol edeceğiz.
    # surface eğer herhangi bir yüzey yüklenmemişse bizim için siyah bir kare oluşturacak. Eğer yüklenmişse o png gösterilecek.
    super().__init__(groups) # Sprite class'ını da initialize ediyoruz. 
    self.sprite_type = sprite_type # Sprite türümüzün değişkenini oluşturduk.

    y_offset = HITBOX_OFFSET[sprite_type] # sprite_type'ına göre bir hitbox değeri alıyoruz.

    self.image = surface # Ekrana çizeceğimiz Tile objesinin resmi için bir değişken oluşturuyor ve bir fotoğraf yüklüyoruz. Parametreden gelen fotoyu koyacağız.
    
    if sprite_type == 'object': # Eğer sprite türümüz bir obje ise:
      # Bir offset yapmalıyız:
      self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILESIZE)) # X ekseninde bir değişim yapmıyoruz fakat y eksenini TILESIZE kadar yukarı kaydırıyoruz ki fotoğrafın en köşesine gelsin.
    else: # Eğer grass ise bir sorun yok aynen çizdirebiliriz.
      self.rect = self.image.get_rect(topleft = pos) # Ekrana çizeceğimiz Tile objesinin bir temas alanını yaratıyoruz. # Bu bizim çizim için kullandığımız alan olacak.
    # Aldığımız position ile de konumunu ayarlıyoruz.
    
    self.hitbox = self.rect.inflate(0,y_offset) # inflate metodu verilen değerler kadar rect'i küçültür. Bu örnekte settings içerisinden alacağımız değere göre bir offset veriyoruz.