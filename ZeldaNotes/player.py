# Player class'ı ile oyundaki karakterimizi oluşturacağız.
# Oyuna gerçekçilik katmak için overlap(üst üste gelme) yapmamız gerekiyor. Bunun için 2 farklı alan oluşturacağız.
# İlk alan direkt bizim full rect'imiz, ikincisi ise hitbox alanımız olacak. Hitboxları y ekseninden küçülterek üst üste binmeyi sağlayabiliriz.

import pygame 
from settings import *
from support import *
from entity import Entity

class Player(Entity): # (1)Player sınıfı bir sprite olacak ve ordan kalıtım alacak. (2) Player sınıfı Entity sınıfından kalıtım alacak ve zaten Entity sınıfı da sprite'lardan kalıtım alıyor.
  def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic): # Ayrıca pozisyon parametresi alıyoruz nereye yerleştireceğimizi bilmek için
    # groups ile Player objesinin hangi grupta olduğuna bakabiliriz.
    # obstacle_sprites ile karakterin haritadaki nesnelerden haberi olmasını ve çarpışmasını sağlıyoruz.
    # create_attack parametresi Level içerisindeki create_attack metoduna ulaşabilmemiz için gerekli. Eğer saldırı inputu verilmişse alacağız ve kullanacağız.
    # create_magic parametresi Level içerisindeki create_magic metoduna ulaşabilmemiz için gerekli. Eğer büyü inputu verilmişse alacağız ve kullanacağız.
    super().__init__(groups) # Sprite class'ını da initialize ediyoruz. 
    self.image = pygame.image.load('graphics/test/player.png').convert_alpha() # Ekrana çizeceğimiz Player objesinin resmi için bir değişken oluşturuyor ve bir fotoğraf yüklüyoruz.
    self.rect = self.image.get_rect(topleft = pos) # Ekrana çizeceğimiz Player objesinin bir temas alanını yaratıyoruz.
    # Aldığımız position ile de konumunu ayarlıyoruz.
    self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player']) # Bu da overlap yapabilmemiz için gerekli olan hitbox'ımız.
    # Hitbox değerini settings'den aldık.

    # Grafik ayarları (animasyonlar)
    self.import_player_assets() # Karakter animasyonlarını yükleyen metodu init kısmında karakter çağırılken çalıştırıyoruz.
    self.status = 'down' # Karakterimizin hangi durumda olduğunu bu değişken ile belirleyerek ona göre animasyona ulaşıp animasyonu gerçekleştireceğiz. default olarak down'ı verdik.
    
    """ Bu değişkenleri entity sınıfının içerisinde tanımladık.
    self.frame_index = 0 # Karakter animasyonlarını içeren durum listeleri içerisinde sırayla fotoğrafları indexlerine göre döneceğimiz için bir index oluşturuyoruz.
    self.animation_speed = 0.15 # Karakter animasyonlarını içeren surface listesi içerisinde yukarıdaki index'imizi artıracak olan animasyon hızımızı belirliyoruz.
    """

    # Hareket için gerekliler:
    """ Bu değişkeni de Entity içerisinde tanımladık.
    self.direction = pygame.math.Vector2() # Karakterimizin yöneldiği yönü göstermek için bir değişken oluşturduk
    """
    # Bu değişken (x,y) şeklinde ve eğer sağa gidiyorsak 1,0, sola gidiyorsak -1,0
    # yukarı gidiyorsak 0,-1 aşağı gidiyorsak 0,1 değerlerini alacak.
     # self.speed = 5 # Karakterimizin yürümesi için bir hız değişkeni oluşturduk. Stats bölümünde yenisi var.
    self.attacking = False # Saldırıyor olma durumumuzun kontrolü için bir değişken oluşturduk.
    self.attack_cooldown = 400 # Tekrar saldırma süremiz için bir değişken oluşturduk.
    self.attack_time = None # Saldırı süremiz için bir değişken oluşturduk. Bu değişkeni her salırdığımızdan itibaren tutmaya başlayacağız.

    # Silahlar
    self.create_attack = create_attack # Level class'ı içerisinde oluşturduğumuz create_attack metodunu burada da kullanabilmek için tanımlıyoruz.
    self.destroy_attack = destroy_attack # Level class'ı içerisinde oluşturduğumuz destroy_attack metodunu burada da kullanabilmek için tanımlıyoruz.
    # destroy_attack metodunu cooldowns içerisinde çağırmalıyım. Çünkü saldırı bittikten sonra yani o cooldowndan sonra silahı ekrandan silmeli.
    self.weapon_index = 0 # Silah seçimi için bir index değeri oluşturuyoruz.
    # Oyun içerisinde input alarak silah değişimini yapacağız.
    self.weapon = list(weapon_data.keys())[self.weapon_index] # Weapon_data bizim silahlarımızı tutan dictionary ve keys kısmında silahlarımızın isimleri var. Dosya isimleri de aynı olduğu için kolaylıkla ulaşabiliriz.
    # weapon_index'imize göre bu keys yani silahlardan birini seçeceğiz. Bu nedenle bir listeye çeviriyoruz.
    self.can_switch_weapon = True # Silahı değiştirip değiştiremeyeceğimizi söyleyen değişken
    self.weapon_switch_time = None # Silah değiştirme süremiz için bir değişken oluşturduk. Bu değişken ile timer oluşturacağız.
    self.switch_duration_cooldown = 200 # Tekrar silah değiştirebilmemiz için gereken süre.

    # Büyüler
    self.create_magic = create_magic # Level class'ı içerisinde oluşturduğumuz create_magic metodunu burada da kullanabilmek için tanımlıyoruz.
    self.magic_index = 0 # Büyü seçimi için gerekli olan index değeri
    # Oyun içerisinde input alarak büyü değişimini yapacağız.
    self.magic = list(magic_data.keys())[self.magic_index] # magic_data bizim büyülerimizi tutan dictionary ve keys kısmında büyülerimizin isimleri var. Dosya isimleri de aynı olduğu için kolaylıkla ulaşabiliriz.
    # magic_index'imize göre bu keys yani büyülerden birini seçeceğiz. Bu nedenle bir listeye çeviriyoruz.
    self.can_switch_magic = True # Büyüyü değiştirip değiştiremeyeceğimizi söyleyen değişken
    self.magic_switch_time = None # Büyü değiştirme süremiz için bir değişken oluşturduk. Bu değişken ile timer oluşturacağız.
     # self.switch_duration_cooldown = 200 # Tekrar büyü değiştirebilmemiz için gereken süre. Silahla aynı old için gerek yok.

    # Statlar
    self.stats = {'health':100, 'energy':60, 'attack':10, 'magic':4, 'speed':6} # Karakterimizin statlarını oluşturduk.
    self.max_stats = {'health':300, 'energy':140, 'attack':20, 'magic':10, 'speed':10} # Karakterimizin tecrübelerle geliştirebileceği maksimum stat'lar
    self.upgrade_cost = {'health':100, 'energy':100, 'attack':100, 'magic':100, 'speed':100} # Her bir geliştirme için gereken tecrübe puanı miktarı.
    self.health = self.stats['health'] # Bir can değişkeni oluşturduk.
    self.energy = self.stats['energy'] # Bir enerji değişkeni oluşturduk.
    self.exp = 500 # UI için bir enerji oluşturduk.
    self.speed = self.stats['speed'] # Hız değişkenimizi oluşturduk. Eskisini silebiliriz.
    # Oyun içerisinde değişebilecek değişkenlerimizi ayrı bir değişkende tutuyoruz.

    # Hasar alabilme zamanlayıcısı
    self.vulnerable = True # Hasar alabilme
    self.hurt_time = None # Timer için gerekli zamanlayıcı
    self.invulnerability_duration = 500 # Tekrar hasar alabilmesi için geçmesi gereken süre

    self.obstacle_sprites = obstacle_sprites # obstacle_sprites grubunu player için de tanımlıyoruz.

    # Sesler
    self.weapon_attack_sound = pygame.mixer.Sound('audio/sword.wav') # saldırı sesimiz
    self.weapon_attack_sound.set_volume(0.4) # Saldırı ses düzeyimiz

  def import_player_assets(self): # Karakterin tüm animasyonlarını import edeceğiz.
    character_path = 'graphics/player/' # Tüm animasyonların temelinde bulunan dosya yolunu bir değişkene atıyoruz.

    self.animations = { # Karakterimizin 12 farklı animasyonu için bir dictionary oluşturduk.
        'up': [], 'down':[],'left':[],'right':[], # Yürüyüş animasyonları
		    'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[], # Boş durma animasyonları her yön için
		    'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[] # Her yön için saldırı animasyonları
    }
    # Karakter animasyonlarımızın bulunduğu dosyaların isimleri yukarıdaki dictionary'lerin key isimleri ile aynı. Bu şekilde kolayca ulaşabileceğiz.

    for animation in self.animations.keys(): # Verilen dictionary'nin tüm keyslerini animasyon olarak bakıyoruz.
      # Burada tüm animasyonlar için gerekli aynı isimli dosyaya ulaşacağım. (Aşağıda tam dosya yolunu oluşturduktan sonra.)
      full_path = character_path + animation # Bu bize 'graphics/player/up' gibi bir şey döndürecek.
      # Sıradaki işlem çok önemli. Yukarıdaki dosya yoluna ulaştıktan sonra önceden oluşturduğumuz ve tüm png'leri bir surface olarak bize veren metodu kullanarak dictionary içerisindeki values boşluklarını elde ettiğimiz surface'lar ile dolduracağız.
      self.animations[animation] = import_folder(full_path) # animasyonlar dictionary'si içerisindeki örneğin 'up' key'inin value'suna metot ile getirmiş olduğumuz surface'ları veriyoruz ve bunu tüm animasyonlar için yapıyoruz. 
    # Çıktı bize her animasyon için surface'lardan oluşan bir liste döndürecek.

  def input(self): # Klavyeden girilen inputları alan fonksiyon
    keys = pygame.key.get_pressed() # Klavyedeki tüm tuşları aldık.

    if not self.attacking: # Eğer saldırı yapıyor isek hiçbir klavye input'u almak istemiyorum.
      # Hareket
      if keys[pygame.K_UP]: # Eğer klavyede yukarı ok tuşuna basıyorsak
        self.status = 'up' # Karakterimiz yukarı yönde gidiyor olduğu için durumunu 'up' yapıyoruz ki animasyonuna kolayca ulaşabilelim.
        self.direction.y = -1 # Player direction'ının y'sini -1 yap.
      elif keys[pygame.K_DOWN]: # Eğer klavyede aşağı ok tuşuna basıyorsak
        self.status = 'down' # Karakterimiz aşağı yönde gidiyor olduğu için durumunu 'down' yapıyoruz ki animasyonuna kolayca ulaşabilelim.
        self.direction.y = 1 # Player direction'ının y'sini 1 yap.
      else: # Eğer bu tuşlara basılmıyorsa direction'ın y'si 0 olsun.
        self.direction.y = 0

      if keys[pygame.K_RIGHT]: # Eğer klavyede sağ ok tuşuna basıyorsak
        self.status = 'right' # Karakterimiz sağ yönde gidiyor olduğu için durumunu 'right' yapıyoruz ki animasyonuna kolayca ulaşabilelim.
        self.direction.x = 1 # Player direction'ının x'sini 1 yap.
      elif keys[pygame.K_LEFT]: # Eğer klavyede sol ok tuşuna basıyorsak
        self.status = 'left' # Karakterimiz sol yönde gidiyor olduğu için durumunu 'left' yapıyoruz ki animasyonuna kolayca ulaşabilelim.
        self.direction.x = -1 # Player direction'ının x'sini -1 yap.
      else: # Eğer bu tuşlara basılmıyorsa direction'ın x'si 0 olsun.
        self.direction.x = 0

      # Saldırı
      if keys[pygame.K_SPACE]: # Eğer space tuşuna basıyorsak (ve saldırma animasyonu içerisinde değilsek) saldır. Bu şekilde art arda saldırı yapmayı önlüyoruz. Fakat bastığımızda pygame birden çok kez tetikleniyor. Bu yüzden bir timer oluşturmamız lazım.
        self.attacking = True # Değişkenimizi True yapıyoruz çünkü bir saldırı işlemi içerisindeyiz.
        self.attack_time = pygame.time.get_ticks() # Oluşturduğum değişken ise sadece space'e basılınca tek seferlik zamanı hesaplıyor.
        self.create_attack() # Level class'ı içerisinden alıp burada çağırdığımız metodu çalıştırıyoruz her bir attack işleminde.
        self.weapon_attack_sound.play() # Ve her saldırıda bu sesi çalıyoruz.

      # Büyü
      if keys[pygame.K_LCTRL]: # Eğer sol ctrl'ye basıyorsak (ve saldırma animasyonu içerisinde değilsek) büyü kullan. Fakat bastığımızda pygame birden çok kez tetikleniyor. Bu yüzden bir timer oluşturmamız lazım.
        self.attacking = True # Değişkenimizi True yapıyoruz çünkü bir saldırı işlemi içerisindeyiz.
        self.attack_time = pygame.time.get_ticks() # Oluşturduğum değişken ise sadece LCTRL'e basılınca tek seferlik zamanı hesaplıyor.
        style = list(magic_data.keys())[self.magic_index] # Büyünün türü
        strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic'] # Büyünün gücü (Karakterin kendinde olan büyü hasarını da ekliyoruz.)
        cost = list(magic_data.values())[self.magic_index]['cost'] # Büyü maliyeti
        self.create_magic(style,strength,cost) # Create_magic için style,strength ve cost lazım. Kullanıcı her büyü kullandığında LCTRL ile Level class'ı içerisindeki bu metot çalışacak.
      
      # Silah değişimi
      if keys[pygame.K_q] and self.can_switch_weapon: # Eğer oyun içerisinde q tuşuna basarsak ve silah değiştirebiliyorsak(değişken True ise) silah değişsin fakat bunun için de bir timer(zamanlayıcı) lazım. Sürekli silah değişmesin diye. (pygame birden fazla tetikleyebilir.)
        self.can_switch_weapon = False # Silah değiştirebilmeyi False yap.
        self.weapon_switch_time = pygame.time.get_ticks() # q'ya basıldığı gibi süreyi hesaplamaya başlayacağız ve bu süreyi değişkende tutacağız. Timer yaparken kullanacağız.
        if self.weapon_index < len(list(weapon_data.keys())) - 1: # Eğer index'imiz liste uzunluğunun 1 eksiğinden küçükse.(index hesabı)
          self.weapon_index += 1 # Silah index'ini 1 artırıyoruz.
        else: # Eğer büyükse,
          self.weapon_index = 0 # Silah index'ini tekrar 0 yapıp başa döndürüyoruz.
        # Silah index'i artıyor fakat self.weapon'ı init içerisinde aldığımız için sürekli aynı silah geliyor. Bu nedenle q ya basıldığında self.weapon'ı güncellemeliyiz.
        self.weapon = list(weapon_data.keys())[self.weapon_index] # self.weapon'ı güncelleyerek yeni silaha geçiyoruz.

      # Büyü değişimi
      if keys[pygame.K_e] and self.can_switch_magic: # Eğer oyun içerisinde e tuşuna basarsak ve büyü değiştirebiliyorsak(değişken True ise) büyü değişsin fakat bunun için de bir timer(zamanlayıcı) lazım. Sürekli büyü değişmesin diye. (pygame birden fazla tetikleyebilir.)
        self.can_switch_magic = False # Büyü değiştirebilmeyi False yap.
        self.magic_switch_time = pygame.time.get_ticks() # e'ya basıldığı gibi süreyi hesaplamaya başlayacağız ve bu süreyi değişkende tutacağız. Timer yaparken kullanacağız.
        if self.magic_index < len(list(magic_data.keys())) - 1: # Eğer index'imiz liste uzunluğunun 1 eksiğinden küçükse.(index hesabı)
          self.magic_index += 1 # Büyü index'ini 1 artırıyoruz.
        else: # Eğer büyükse,
          self.magic_index = 0 # Büyü index'ini tekrar 0 yapıp başa döndürüyoruz.
        # Büyü index'i artıyor fakat self.magic'ı init içerisinde aldığımız için sürekli aynı büyü geliyor. Bu nedenle e ya basıldığında self.magic'ı güncellemeliyiz.
        self.magic = list(magic_data.keys())[self.magic_index] # self.magic'ı güncelleyerek yeni büyüye geçiyoruz.

  def get_status(self): # Karakterimizin durumunu getirecek olan metodumuzu yazıyoruz.

    # Boş durma durumları
    if self.direction.x == 0 and self.direction.y == 0: # Karakterimiz duruyor ama en son hangi pozisyonda duruyor bunu belirlememiz lazım.
      if not 'idle' in self.status and not 'attack' in self.status: # Eğer status içerisinde idle yoksa ve attack yoksa idle ekliyoruz. Bu şekilde sürekli idle eklemiş olmayacağız ve hem saldırıp hem de boş duruyor olmayacağız.
        self.status = self.status + '_idle' # Eğer karakterimiz duruyorsa onun en son bastığımız tuşa göre yönünü alıyor ve dosya isimleri uyum sağlasın diye sonuna _idle eksliyoruz.

    # Saldırı durumları
    if self.attacking: # Saldırı yapıyor olduğumuz zaman
      self.direction.x = 0 # x'i ve y'i 0 yapıyoruz ki saldırırken hareket edemeyelim.
      self.direction.y = 0
      if not 'attack' in self.status: # Eğer status içerisinde attack yoksa attack ekliyoruz. Bu şekilde sürekli attack eklemiş olmayacağız.
        if 'idle' in self.status: # Eğer statusün içerisinde hala _idle varsa (right_idle_attack gibi)
          self.status = self.status.replace('_idle','_attack') # idle'ı kaldırıp yerine attack yazdırabiliriz.
        else: # Eğer status içerisinde _idle yoksa direkt _attack ekleyebiliriz.
          self.status = self.status + '_attack' # Eğer karakterimiz duruyorsa onun en son bastığımız tuşa göre yönünü alıyor ve dosya isimleri uyum sağlasın diye sonuna _attack eksliyoruz.
    else: # Saldırı bittiği ya da yapmadığımız zaman
      if 'attack' in self.status: # Eğer durumumuzun içerisinde attack varsa aşağıdaki işlemi yap ki hata göndermesin.
        self.status = self.status.replace('_attack','') # Durmumuzu tekrar eski haline getiriyoruz ki sürekli saldırı animasyonunda kalmayalım.

  """ Entity class'ı içerisine kopyaladık ve orada hem düşmanlar hem de player için bir çarpışma ve hareket oluşturacağız.
  #####################################################################################################
  def move(self,speed): # Karakterin yürümesini sağlayacak metodu oluşturuyoruz.
    # speed parametresi karakterin hızı olacak.

    # Fakat (1,1) gibi çift yönlü durumlarda karakter aşırı hızlı gidiyor bu sebeple bu hızı normalleştirmemiz gerek:

    if self.direction.magnitude() != 0: # Direction'ımızın bir değeri olup olmadığına bakıyoruz.(x ve y vektörleri için)
      self.direction = self.direction.normalize() # Eğer öyleyse bu hızı normalleştiriyoruz.(0.7 gibi bir değer)

     # self.rect.center += self.direction * speed # Karakterimizin rectangle'ının merkezini her saniye karakterin directionını, karakterin hızı ile çarpıp ekliyoruz.
    # Bu şekilde eğer yönümüz sola (-1,0) ise hız 5 ise (-5,0) kordinatlarına taşıyor ve hızlıca karakteri çiziyoruz. Böylece karakterimiz hareket ediyor.

    # 1- # Yönleri ayırdık çünkü hangi yönder çarpışma olduğunu bilmek istiyoruz.
    
      # self.rect.x += self.direction.x * speed # Karakterin rect'inin x konumuna direction * speed ekliyoruz.
      # self.collision('horizontal') # Yatay çarpışmanın kontrolünü yapıyoruz.
      # self.rect.y += self.direction.y * speed # Karakterin rect'inin y konumuna direction * speed ekliyoruz.
      # self.collision('vertical') # Dikey çarpışmanın kontrolünü yapıyoruz.
       
    # 2- # rect'leri hitboxlar ile değiştiriyoruz.

    self.hitbox.x += self.direction.x * speed # Karakterin hitbox'inin x konumuna direction * speed ekliyoruz.
    self.collision('horizontal') # Yatay çarpışmanın kontrolünü yapıyoruz.
    self.hitbox.y += self.direction.y * speed # Karakterin hitbox'inin y konumuna direction * speed ekliyoruz.
    self.collision('vertical') # Dikey çarpışmanın kontrolünü yapıyoruz.
    # Yönleri ayırdık çünkü hangi yönder çarpışma olduğunu bilmek istiyoruz.
    self.rect.center = self.hitbox.center # Rect'in merkeziyle hitbox'ın merkezini aynı yere koyduk ve ayarladık.

  def collision(self,direction): # Çarpışmaları gerçekleştirecek metodu yazıyoruz.
    # direction parametresi ile çarpışmanın hangi yönden olduğuna bakıyoruz.

  # 1- 
  
    # if direction == 'horizontal': # Eğer yatay eksendeysek.
    #   for sprite in self.obstacle_sprites: # obstacle_sprites grubundaki her bir sprite için
    #     if sprite.rect.colliderect(self.rect): # Eğer sprite karakterimiz ile çarpışıyorsa.
    #       if self.direction.x > 0: # Eğer karakterimizin yönü sağa doğruysa
    #         self.rect.right = sprite.rect.left # Çarpışmadan sonra karakterimizin rect'inin sağ tarafı, çarptığımız nesnenin rect'inin sol tarafının konumunda olmalı.
    #       if self.direction.x < 0: # Eğer karakterimiz sola doğruysa
    #         self.rect.left = sprite.rect.right # Çarpışmadan sonra karakterimizin rect'inin sol tarafı, çarptığımız nesnenin rect'inin sağ tarafının konumunda olmalı.
    
    # if direction == 'vertical': # Eğer dikey eksendeysek.
    #   for sprite in self.obstacle_sprites: # obstacle_sprites grubundaki her bir sprite için
    #     if sprite.rect.colliderect(self.rect): # Eğer sprite karakterimiz ile çarpışıyorsa.
    #       if self.direction.y > 0: # Eğer karakterimizin yönü aşağı doğruysa
    #         self.rect.bottom = sprite.rect.top # Çarpışmadan sonra karakterimizin rect'inin alt tarafı, çarptığımız nesnenin rect'inin üst tarafının konumunda olmalı.
    #       if self.direction.y < 0: # Eğer karakterimiz yukarı doğruysa
    #         self.rect.top = sprite.rect.bottom # Çarpışmadan sonra karakterimizin rect'inin üst tarafı, çarptığımız nesnenin rect'inin alt tarafının konumunda olmalı.
  
  # 2- rect'leri hitbox ile değiştirdik ki overlap yapabilelim.
    
    if direction == 'horizontal': # Eğer yatay eksendeysek.
      for sprite in self.obstacle_sprites: # obstacle_sprites grubundaki her bir sprite için
        if sprite.hitbox.colliderect(self.hitbox): # Eğer sprite karakterimizin hitboxı ile çarpışıyorsa.
          if self.direction.x > 0: # Eğer karakterimizin yönü sağa doğruysa
            self.hitbox.right = sprite.hitbox.left # Çarpışmadan sonra karakterimizin hitbox'ının sağ tarafı, çarptığımız nesnenin hitbox'inin sol tarafının konumunda olmalı.
          if self.direction.x < 0: # Eğer karakterimiz sola doğruysa
            self.hitbox.left = sprite.hitbox.right # Çarpışmadan sonra karakterimizin hitbox'inin sol tarafı, çarptığımız nesnenin hitbox'inin sağ tarafının konumunda olmalı.
    
    if direction == 'vertical': # Eğer dikey eksendeysek.
      for sprite in self.obstacle_sprites: # obstacle_sprites grubundaki her bir sprite için
        if sprite.hitbox.colliderect(self.hitbox): # Eğer sprite karakterimiz ile çarpışıyorsa.
          if self.direction.y > 0: # Eğer karakterimizin yönü aşağı doğruysa
            self.hitbox.bottom = sprite.hitbox.top # Çarpışmadan sonra karakterimizin hitbox'inin alt tarafı, çarptığımız nesnenin hitbox'inin üst tarafının konumunda olmalı.
          if self.direction.y < 0: # Eğer karakterimiz yukarı doğruysa
            self.hitbox.top = sprite.hitbox.bottom # Çarpışmadan sonra karakterimizin hitbox'inin üst tarafı, çarptığımız nesnenin hitbox'inin alt tarafının konumunda olmalı.
  #####################################################################################################
  """
  def cooldowns(self): # Bu metot ile timer tutmamız gereken hareketler için bir cooldown ooluşturuyoruz.
    current_time = pygame.time.get_ticks() # Anlık zamanı sürekli olarak hesaplıyoruz.

    # Saldırı Zamanlayıcısı
    if self.attacking: # Eğer saldırı yapıyorsak aşağıdaki işlemleri yap.
      if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']: # Eğer sürekli hesaplanan oyun zamanından saldırı süremizi çıkarırsak ve bu da saldırı cooldown'ından fazla veya eşit ise (silah ve karakter cooldown'ının toplamı)
        self.attacking = False # Saldırı bitmiş demektir ve tekrar saldırı yapabilmemiz için self.attacking'i False yapıyoruz.
        self.destroy_attack() # Saldırı cooldown'ı bittikten sonra silahı ekrandan siliyoruz.

    # Silah Zamanlayıcısı
    if not self.can_switch_weapon: # Silah değiştirirken bu değişken False oluyor bu nedenle not kullanıyoruz. Yani silah değişirken,
      if current_time - self.weapon_switch_time >= self.switch_duration_cooldown: # Eğer sürekli hesaplanan oyun zamanından q'ya bastığımızda hesaplanan zamanı çıkarırsak ve bu da silah değiştirme cooldown'ından fazla veya eşit ise
        self.can_switch_weapon = True # Silahı değiştirmiş demektir ve tekrar silah değiştirebilmemiz için self.can_switch_weapon'ı True yapıyoruz.

    # Büyü Zamanlayıcısı
    if not self.can_switch_magic: # Büyü değiştirirken bu değişken False oluyor bu nedenle not kullanıyoruz. Yani büyü değişirken,
      if current_time - self.magic_switch_time >= self.switch_duration_cooldown: # Eğer sürekli hesaplanan oyun zamanından e'ya bastığımızda hesaplanan zamanı çıkarırsak ve bu da büyü değiştirme cooldown'ından fazla veya eşit ise
        self.can_switch_magic = True # Büyü değiştirmiş demektir ve tekrar büyü değiştirebilmemiz için self.can_switch_magic'ı True yapıyoruz.

    # Tekrar hasar alabilme zamanlayıcısı
    if not self.vulnerable: # Eğer hasar almışsak
      if current_time - self.hurt_time >= self.invulnerability_duration: # Cooldown sağlanıyorsa
        self.vulnerable = True # Hasar alabilmeyi tekrardan True yap.

  def animate(self): # Bu metot ile oyuncunun status'üne göre animasyon fotoğraflarını tek tek gezen bir döngü oluşturacağız.
    animation = self.animations[self.status] # Animasyonumu öğrenmek için animations dictionary'm içerisindeki self.status durumuna gideceğim ve o da bize yardımcı metodumuz ile doldurmuş olduğumuz surface listelerini getirecek.

    # Animasyon döngü işlemleri
    self.frame_index += self.animation_speed # Sürekli index'leri döndürecek olan index'i animasyon hızımızı sürekli ekleyerek döndürüyoruz.
    if self.frame_index >= len(animation) -1: # Eğer index'imiz liste içerisindeki animasyon png'lerinin index numarasının üstüne çıkarsa,
      self.frame_index = 0 # index'imizi tekrar 0 yapıyoruz ki sürekli dönsün.

    # Animasyonların ayarlanması
    self.image = animation[int(self.frame_index)] # Karakterin fotoğrafını doğru animasyon png'lerinin içinde bulunduğu listeden index yardımı ile seçiyoruz. Integer'a çevirmemiz gerekiyor ki tam sayı alalım.
    self.rect = self.image.get_rect(center = self.hitbox.center) # Her hareketin ardına da düzenin bozulmamsı için yeni bir rect oluşturuyoruz.

    # Player'ın hasar alması. Bunun için Level içerisinde birkaç tane metot oluşturacağız. Ve hasar vermeyi Enemy'e vereceğiz.
    # Player'ın hasar alınca titremesi

    if not self.vulnerable: # Eğer karakter hasar almışsa
      alpha = self.wave_value() # Entity içerisindeki 255 ya da 0 transparanlık değeri döndüren metot ile değeri alıyoruz.
      self.image.set_alpha(alpha)
    else: # Eğer hasar almamışsa
      self.image.set_alpha(255)

  def get_full_weapon_damage(self): # Toplam silah hasarını getirecek metod. Canavarın canını azaltacak miktar.
    base_damage = self.stats['attack'] # Karakterin temel hasarı
    weapon_damage = weapon_data[self.weapon]['damage'] # Silahın hasarı
    return base_damage + weapon_damage # Karakter ve silahın toplam hasarı
  
  def get_full_magic_damage(self):
    base_damage = self.stats['magic'] # Karakterin temel büyü hasarı
    spell_damage = magic_data[self.magic]['strength'] # Büyü hasarı
    return base_damage + spell_damage # Karakter ve büyünün toplam hasarı

  def get_value_by_index(self,index): # Indeks değeri ile stat değerlerini getiren metot.
    return list(self.stats.values())[index] # Stat değerleri içerisinden index ile değeri getiriyoruz.

  def get_cost_by_index(self,index): # Indeks değeri ile stat maliyetlerini getiren metot.
    return list(self.upgrade_cost.values())[index] # upgrade_cost dict içerisinden değerleri alıyor ve index ile seçiyorum.

  def energy_recovery(self): # Oyun içinde enerjimizi yenileyecek olan metot.
    if self.energy < self.stats['energy']: # Eğer şu anki enerjimiz maksimum enerjimizin altında ise,
      self.energy += 0.01 * self.stats['magic'] # Enerjiyi 0.01 * 4 arttır.
    else: # Olur da maks üstüne çıkarsa enerjimiz.
      self.energy = self.stats['energy'] # enerjiyi maks yap.

  def update(self): # Bu metot ile karakteri sürekli güncelleyip birden fazla metotu bir anda çağırabileceğiz.
    self.input() # Input metodunu çağırıyoruz.
    self.cooldowns() # Cooldowns metodunu çağırıp timer'ı sürekli tutturuyoruz. Böylece art arda saldırı yapmanın önüne geçebildik. Bu saldırı ve büyü için de geçerli.
    self.get_status() # Ve metodumuzu çağırarak sürekli olarak oyuncunun durumunu kontrol ediyoruz.
    self.animate() # Ve animasyonları gerçekleştirecek metodumuzu update içerisinde çağırıyoruz.
    self.move(self.stats['speed']) # move metodunu çağırıyor ve hız parametresi için stat'lar içerisinden hız'ı veriyoruz.
    self.energy_recovery() # enerjimizi yenileyen metodumuz.
