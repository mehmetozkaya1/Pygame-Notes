# Düşmanlar

import pygame
from settings import *
from entity import Entity
from support import *

class Enemy(Entity): # Bir düşman sınıfı oluşturuyoruz ve Entity'den kalıtım alıyor.
  def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_exp):
    # monster_name canavarın ismi olacak ve enemy_data içerisindeki key'lerden gelecek.
    # pos düşmanın oyun başında nerede konumlanacağını belirtecek.
    # groups ise hangi sprite grubunda olacağını belirtecek.
    # Ve tekrar collision için tüm obstacle_sprites'lara bakıyoruz ve bunu düşmanlar için de tanımlamalıyız.
    # damage_player ise damage_player'ı tutacak olan değişken. Bu metod ile player'a hasar verilebilecek.
    # trigger_death_particles ise öldüğünde animasyonları oluşturacak metot.
    # add_exp ile öldüklerinde exp vermelerini sağlıyoruz.

    # Genel Ayarlar
    super().__init__(groups) # Kalıtım aldığı sınıfı init ediyoruz.
    self.sprite_type = 'enemy' # Eğer bir düşmana saldırıyorsak canı azalacak ya da ölecek. Fakat bir Tile'a saldırıyorsak o bizle etkileşime girmeyecek sadece yok olacak.

    # grafik ayarları
    self.import_graphics(monster_name) # monster_name parametresinden gelen canavar ismine göre grafik yüklemesi yapan metotu çağırıyorum.
    self.status = 'idle' # Canavarın default durumu idle olsun istiyoruz.
    # self.image = pygame.Surface((64,64)) # Düşmanımız için geçici olarak bir siyah kare oluşturduk. (Eski)
    self.image = self.animations[self.status][self.frame_index] # animasyonlar dict içerisinden, canavarın durumuna göre png getiriyoruz ve frame_index'imize göre Surface'lardan birini seçiyoruz.
    
    # Canavar hareketleri
    self.rect = self.image.get_rect(topleft = pos) # Ve düşman png'mizin bir rect'ini oluşturduk.
    self.hitbox = self.rect.inflate(0,-10) # Canavarlar için bir hitbox oluşturduk. Entity class'ı hareket ve collision için hitbox'a ihtiyaç duyuyor.
    self.obstacle_sprites = obstacle_sprites # Ve tekrar collision için tüm obstacle_sprites'lara bakıyoruz ve bunu düşmanlar için de oluşturmalıyız.

    # Canavar bilgileri
    self.monster_name = monster_name # Canavar ismini alan değişken
    monster_info = monster_data[self.monster_name] # Canavar bilgilerini getiren değişken
    self.health = monster_info['health'] # Yukarıdaki değişken üzerinden can bilgisini aldık.
    self.exp = monster_info['exp'] # Canavar exp'si
    self.speed = monster_info['speed'] # Canavar hızı
    self.attack_damage = monster_info['damage'] # Canavar saldırı hasarı
    self.resistance = monster_info['resistance'] # Canavar geri sekmesi
    self.attack_radius = monster_info['attack_radius'] # Canavar saldırı alanı
    self.notice_radius = monster_info['notice_radius'] # Canavar fark etme alanı
    self.attack_type = monster_info['attack_type'] # Canavar saldırı türü.

    # Player ile etkileşim
    self.can_attack = True # Sürekli player'a vurulu halde kalmasın diye bir değişken oluşturuyoruz.
    self.attack_time = None # Düşmanın tekrar saldırabilmesi için bir timer oluşturacağız. Bu da saldırdığı andan itibaren hesaplanan süre olacak.
    self.attack_cooldown = 400 # Tekrar saldırı yapılabilmesi için gereken süre.
    self.damage_player = damage_player
    self.trigger_death_particles = trigger_death_particles
    self.add_exp = add_exp

    # Ölümsüzlük zamanlayıcısı
    self.vulnerable = True # Hasar alabilir mi?
    self.hit_time = None # Timer için hesaplanacak vuruş süresi
    self.invincibility_duration = 300 # Her çarpışmadan sonraki hasar almama süresi.

    # Sesler
    self.death_sound = pygame.mixer.Sound("audio/death.wav") # Canavar ölüm sesi
    self.hit_sound = pygame.mixer.Sound("audio/hit.wav") # Canavar hasar yeme sesi
    self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
    # monster_info, monster_data içerisinden seçili canavarın değerlerini getirir.
    # ardından da bu dict içerisinden saldırı sesini getireceğiz.

    self.death_sound.set_volume(0.2) # Ses düzeyi ayarı
    self.hit_sound.set_volume(0.2) # ses düzeyi ayarı
    self.attack_sound.set_volume(0.3)

  def import_graphics(self,name): # Canavar animasyonlarını getiren metod.
    self.animations = {'idle': [], 'move': [], 'attack': []} # animasyonları tutacak olan dict.
    # Eğer canavar bizim etki alanımız dışında ise idle olacak.
    # Yakınındaysak bize doğru hareket edecek.
    # Çok yakındaysak saldıracak.
    # Her bir canavar 3 farklı dosya içeriyor isimleri idle move ve attack. Her bir dosyada da farklı o işlem animasyonları var.

    main_path = f'graphics/monsters/{name}/' # Bu path ile hangi canavar ismi verildiyse onun path'ine gideceğiz. # Monster_name'ini bir Enemy oluştururken vereceğiz.
    for animation in self.animations.keys(): # Yukarıdaki listedeki durumlar için
      self.animations[animation] =  import_folder(main_path + animation) # Her bir durum için örneğin idle durumu için listeyi dolduruyoruz.
      # import_folder metodunu tekrar kullanabiliriz. Örneğin graphics/monsters/raccoon/idle klasörüne gidip tüm png'leri bir surface yapacak. Aynısını move ve attack için de yapacak.

  def get_player_distance_direction(self,player): # Player mesafesini ve yönünü alan metot.
    enemy_vec = pygame.math.Vector2(self.rect.center) # Canavarın merkezini bir vektöre dönüştürüyoruz.
    player_vec = pygame.math.Vector2(player.rect.center) # Player'ın merkezini bir vektöre dönüştürüyoruz.
    distance = (player_vec - enemy_vec).magnitude() # Vektör farkını alıyoruz fakat bu bize bir vektör veriyor.
    # Mesafeyi bulabilmek için ise magnitude metodunu kullanıyoruz.

    if distance > 0: # normalize metodu 0 ile çalışamayacağı için sıfır dışındaki durumlar için kullanıyoruz.
      direction = (player_vec - enemy_vec).normalize() # Aynı fark vektörünü biz hızla çarpıp hareket sağlayacağız.
    # Fakat bu vektör hızla çarpılınca çok büyük bir değer geliyor. Bu sebeple normalize metodunu kullanacağız.
    else: # Eğer distance = 0 ise player ve canavar üst üste demektir yani canavar durabilir.
      direction = pygame.math.Vector2()

    return (distance,direction)

  def get_status(self,player): # Bu metot ile player'ın konumunu alabilecek ve player konumuna göre canavarın ne yapması gerektiğini alacağız.
    distance = self.get_player_distance_direction(player)[0] # Bu değişken player ile canavar arası mesafeyi ölçecek.

    if distance <= self.attack_radius and self.can_attack: # Eğer mesafe, saldırı mesafesinden az ya da eşitse ve canavar saldırabilecek durumda ise,
      if self.status != 'attack': # attack durumu sona erdiğinde.
        self.frame_index = 0 # animasyon bittikten sonra tekrar 0 yapıyorum ki sürekli son png'de kalmasın.
      self.status = 'attack' # Canavar durumunu saldır yap.
    elif distance <= self.notice_radius: # Eğer mesafe, fark etme mesafesinden az ya da eşitse,
      self.status = 'move' # Canavar durumunu hareket et yap.
    else: # Eğer mesafe çok uzaksa,
      self.status = 'idle' # Canavar durumunu boş dur yap.

  def actions(self,player):
    if self.status == 'attack': # Eğer saldırı durumundaysa saldır.
      # print('attack') # Eğer ben buraya direkt self.can_attack = False yaparsam saldırı animasyonu bitmeden saldırı sona erer. Bu nedenle saldırı animasyonu bittikten sonra bunu yapmalıyım.
      self.attack_time = pygame.time.get_ticks() # Saldırı durumu başladığından itibaren zamanı tutmaya başlayacak.
      self.damage_player(self.attack_damage,self.attack_type) # Ve player'a hasar vereceğiz. Amount ve attack_type değişkenleri lazım
      # Parametre olarak yukarıda oluşturduğum değişkenleri veriyoruz.  
      self.attack_sound.play() # Ve saldırı ses efektini çalıyoruz. 
    elif self.status == 'move': # Eğer hareket et durumundaysa hareket et.
      self.direction = self.get_player_distance_direction(player)[1] # canavarın yönü için metodun getirdiği 1. indexi alıyoruz.
    else: # Eğer hiçbiri değilse en sonki konumunda kal.
      self.direction = pygame.math.Vector2() # Direction 0 oluyor ve hareket etmiyor.

  def animate(self):
    animation = self.animations[self.status] # Canavarın şu anki durumu

    self.frame_index += self.animation_speed # Entity'den gelen değişkenlerle animasyon hızımızı ayarlıyoruz.
    if self.frame_index >= len(animation): # Eğer fame_index'imiz örneğin idle için png sayısından fazla ise 0 yapacağız.
      if self.status == 'attack': # Ve eğer saldırıyorsak. Yani 4 saldırı fotomuz olsun. Bizim index'imiz 4 ün üstüne çıktığı an saldırı bitmiş demektir. Bu nedenle burada can_attack = False yapabiliriz.
        self.can_attack = False
      self.frame_index = 0
    
    self.image = animation[int(self.frame_index)] # Canavar png'sini sıra ile alıyorum.
    self.rect = self.image.get_rect(center = self.hitbox.center) # Ve rect'i yerleştiriyoruz.

    # Düşmanın hasar alınca titremesi:
    if not self.vulnerable: # Eğer düşman hasar almışsa:
      alpha = self.wave_value() # 0 ile 255 arasında değişen bir transparanlık değeri lazım ve bunu da Entity sınıfı içerisinde oluşturacağız. Çünkü hem player hem de düşmanlar hasar aldığında transparan hale geçmeli.
      self.image.set_alpha(alpha) # Ve surface a uyguluyoruz.
    else: # Eğer düşman hasar almamışsa normal durumda.
      self.image.set_alpha(255) # Transparanlık ekliyoruz. 255 maksimum değer yani tamamen görünür halde.

  def cooldowns(self): # Bu metot ile düşmanın tekrar saldırabilmesi için gereken süreyi ayarlayacak ve bir timer oluşturacağız.
    current_time = pygame.time.get_ticks() # Oyunda sürekli hesaplanan geçerli zaman
    
    # Düşman tekrar saldırma Timer'ı
    if not self.can_attack: # Eğer self.attack = False ise
      if current_time - self.attack_time >= self.attack_cooldown: # Eğer cooldown sağlanmışsa
        self.can_attack = True # Tekrar saldırabilir hale getir.
      # self.attack_time'ı ise actions içerisinden alacağız.
    
    # Düşmanın tekrardan hasar alabilme Timer'ı:
    if not self.vulnerable: # Eğer False ise hasar alma durumu
      if current_time - self.hit_time >= self.invincibility_duration: # Ve eğer cooldown sağlanmış ise
        self.vulnerable = True # Hasar alabilmeyi tekrar True yap.

  def get_damage(self,player,attack_type): # Canavarın hasar almasını sağlayan metot. Fakat pygame collision'ı saniyede 60 kere algıladığı için direkt ölüyorlar. Bu sebeple bir Timer oluşturmamız lazım.
    # player parametresi self.player'ı alacak.
    # attack_type ise attack_sprite.sprite_type'ı tutacak ki büyü mü yoksa silah mı kullandık bilelim.
    if self.vulnerable: # Eğer canavar hasar alabiliyor ise.
      self.hit_sound.play() # Hasar yeme ses efektini çal.
      self.direction = self.get_player_distance_direction(player)[1] # Player directionunu aldık.
      if attack_type == 'weapon': # Eğer silah ile vuruş yapmışsak.
        self.health -= player.get_full_weapon_damage() # Düşman canını get_full_weapon_damage metodu ile getirdiğim toplam silah hasarı kadar azaltacağım. Player içerisindeki
        # Bu metodu player içerisinde oluşturacağım.
      else: # Büyü hasarı ise
        self.health -= player.get_full_magic_damage() # Düşman canını get_full_magic_damage metodu ile getirdiğim toplam büyü hasarı kadar azaltacağım. Player içerisindeki
      
      self.hit_time = pygame.time.get_ticks() # Ve atak yaptıktan sonra da zaman tutmaya başlıyoruz.
      self.vulnerable = False # Her işlemden sonra tekrar hasar almayı False yapıyorum ve timer ile bunu bir süre sonra (self.invinciblitiy_time kadar) tekrar True yapıcam.

  def check_death(self): # Eğer canavarın canı 0'ın altına düşmüşse ölümünü kontrol eden metot.
    if self.health <= 0: # Eğer canı 0 veya altındaysa,
      self.kill() # Yok et.
      self.trigger_death_particles(self.rect.center,self.monster_name) # Level class'ı içerisindeki trigger_death_particles metodunu çağırıyoruz ki düşman öldüğünde efekt çıkarsın. (pos, particle_type) parametrelerini alıyor.
      # Particle düşmanın merkezinde oluşacak ve particle types için ise canavar ismini kullanacağız. Çünkü particles içerisindeki dict e baktığımızda canavar ölüm efektleri isimleriyle adlandırılmış.
      self.add_exp(self.exp) # Ve Level içerisinde oluşturduğum öldüklerinde exp vermelerini sağlayan metodu çağırıyorum.
      # self.exp ile her bir canavarın exp'sini veriyoruz.
      self.death_sound.play() # Ölme ses efektini çalıyoruz.

  def hit_reaction(self): # Bu metot ile düşman hasar aldığında geri savrulmasını sağlayacağız.
    if not self.vulnerable: # Eğer düşman daha yeni hasar almış ise.
      self.direction *= -self.resistance # Düşmanın yönünü resistance değerinin negatifi ile çarparak arka tarafa doğru yönlenmesini sağlıyorum.
    # tekrar hasar alabilir duruma gelene kadar direction ters yönde olacak ve savrulacak.

  def update(self):
    self.hit_reaction() # Hasar aldığında geriye savrulsun.
    self.move(self.speed) # Move metodunu entity class'ı üzerinden alıyoruz ve değişken olarak canavar hızını veriyoruz.
    self.animate() # Animasyonları çağırıyoruz.
    self.cooldowns() # Saldırı cooldown'ını çağırıyoruz.
    self.check_death() # Canavarın ölüp ölmediğini kontrol ediyoruz.

  def enemy_update(self,player): # Düşman durumlarını kontrol eden metot. Level class'ı içerisinde çağırdık ve bu şekilde player'a ulaşabildik.
    self.get_status(player)
    self.actions(player)
