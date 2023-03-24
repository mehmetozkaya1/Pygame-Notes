# Weapons
# Her saldırı gerçekleştirdiğimizde silahımızın bir sprite'ı oluşacak ve ardından tekrar sileceğiz.
# Silahımızın sprite'ını player'ın direction'ına göre oluşturacağız.
# Silah nesnesini Level içerisinde oluşturmalıyım ki düşmanla etkileşime girebilsin. Fakat sorun şu ki biz saldır input'unu player içerisinden alıyoruz.
# Bu nedenle Level içerisine create_attack adında bir metot oluşturacağız.

import pygame

class Weapon(pygame.sprite.Sprite): # Bir silah sınıfı oluşturuyoruz ve bir sprite olacağı için Sprite sınıfından inheritance alıyoruz.
  def __init__(self,player,groups): # init ediyoruz.
    # Silahı player'ın yanında ve o yönde oluşturacağımız için player değişkeni gerekiyor.
    # Ve ayrıca groups açarak silahı çizeceğimiz için visible sprites olması gerekiyor.
    super().__init__(groups) # Sprite class'ını da init ettik.

    self.sprite_type = 'weapon' # Bir sprite_type oluşturuyoruz.

    direction = player.status.split("_")[0] # Player'ın durumunu getiriyoruz yönü ve animasyon png'sini getirebilmek için.
    # Fakat status içerisinde idle ve attack durumları da var ve bunları kullanmak istemiyorum bu nedenle split metodunu kullanıyorum.
    # Ve parçaladığım durumun sadece 0. indexteki elemanını yani yönünü alacağım. (up-down-left-right)

    # Silah grafiği:
    # Silah png'lerimiz player'ın direction'ına göre ayarlandı. (up,down.. gibi)
    # Bu nedenle silah png'lerimize ulaşırken player direction'ını kullanacağız.
    # Hangi silahı seçeceğimizi belirlemek için player içerisinde değişkenlerimizi oluşturduk.(weapon ve weapon_index)
    full_path = f'graphics/weapons/{player.weapon}/{direction}.png' # weapons klasörü içerisinden index ile ulaştığımız silahın klasörünün içerisine giriyor ve yönümüze göre silah png'sini seçiyoruz.
    self.image = pygame.image.load(full_path).convert_alpha() # Silahımızın fotoğrafı için surface tutan bir değişken oluşturuyoruz ve yukarıda ulaştığımız silah yön ve konumuna uygun png'yi getiriyoruz.

    # Silah yerleştirimi:
    if direction == 'right': # Eğer yönümüz sağa doğruysa silahın rect'inin sol tarafı player rect'inin sağ tarafında olmalı.
      self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0,16)) # Karakterin kolu resmin aşağısında olduğu için silahı biraz daha aşağıda oluşturuyoruz.
    elif direction == 'left': # Eğer yönümüz sola doğruysa silahın rect'inin sağ tarafı player rect'inin sol tarafında olmalı.
      self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0,16)) # Karakterin kolu resmin aşağısında olduğu için silahı biraz daha aşağıda oluşturuyoruz.
    elif direction == 'up': # Eğer yönümüz yukarı doğruysa silahın rect'inin alt tarafı player rect'inin üst tarafında olmalı.
      self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10,0)) # Karakterin kolu biraz solda olduğu için biraz daha solda oluşturuyoruz.
    else: # Eğer yönümüz aşağı doğruysa silahın rect'inin üst tarafı player rect'inin alt tarafında olmalı.
      self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10,0)) # Karakterin kolu biraz solda olduğu için biraz daha solda oluşturuyoruz.