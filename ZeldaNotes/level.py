# Level

# Level tüm spriteları içerecek.

# 2 farklı sprite grubu oluşturacağız.

# visible_sprites grubu oyuna çizilecek sprite ların bulunduğu grup olacak.
# obstacle_sprites grubu oyuna çizilmeyecek fakat oyuncu çarpışma yapabilecek. Oyun sınırları gibi

import pygame 
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade

class Level:
  def __init__(self):

    # Display ekranı oluşturacağız.
    self.display_surface = pygame.display.get_surface() # Yaptıklarımızı bir ekranda gösterecek nesne oluşturduk.
    self.game_paused = False # Oyunun durma durumu False ise yani oyun akıyor ise bir değişken oluşturduk.

    # Sprite grupları
     # self.visible_sprites = pygame.sprite.Group() # Oyunda görünecek varlıkların olduğu grup

    # visible_sprites'ı kendi oluşturduğumuz bir gruptan örnek yapmak istiyorum.

    self.visible_sprites = YSortCameraGroup() # Orjinal Group classının bir örneği olduğu için hala bir grup. Kendi oluşturduğumuz grubu veriyoruz.
    self.obstacle_sprites = pygame.sprite.Group() # Oyunda görünmeyen fakat çarpışma olacak varlıkların olduğu grup

    # saldırı sprite'ları
    self.current_attack = None # Ekranda silah nesnesinin bulunup bulunmadığını kontrol etmek için bir değişken oluşturuyoruz.
    self.attack_sprites = pygame.sprite.Group() # Silah ve büyülerin bulunacağı sprite grubu.
    self.attackable_sprites = pygame.sprite.Group() # Obje ve düşmanların bulunacağı sprite grubu.

    # sprite ayarlamaları
    self.create_map() # Dünyayı çizen metotu direkt Level objesinin init kısmında çağırıyoruz.

    # Kullanıcı arayüzü (UI)
    self.ui = UI()
    self.upgrade = Upgrade(self.player) # Upgrade sınıfından bir nesne oluşturduk.

    # Partiküller
    self.animation_player = AnimationPlayer() # Oyun başlangıcında implemente ediyoruz ki oyun yavaşlamasın.
    self.magic_player = MagicPlayer(self.animation_player) # MagicPlayer class'ından bir nesne oluşturduk ki burada da ulaşabilelim.

  def create_map(self): # Oyun dünyasını oluşturup çizecek metodu yazıyoruz.
  # 1- Eski deneme WORLD_MAP ' i çizdiren kısımları comment ediyoruz.
    """
    for row_index,row in enumerate(WORLD_MAP): # Dünya haritasındaki her bir liste ve o listenin indexi için
      # Row indexi bizim y konumu için 64 ile çarpacak olduğumuz index numarası yani ilk satır için 0 2. için 1 getirecek ve biz 64 ile çarpacağız.
      for col_index,col in enumerate(row): # Her bir satır içerisinde ise her bir kolona bakacağız böylece x değerleri için çarpacağımız index numarasını col_index şeklinde alacağız.
        x = col_index * TILESIZE # (64) # Her bir elemanın x pozisyonu
        y = row_index * TILESIZE # (64) # Her bir elemanın y pozisyonu
        if col == 'x': # Dünya haritamızdaki her bir x değeri bizim için bir taş çizeceğimiz anlamına geliyor.
          Tile((x,y),[self.visible_sprites,self.obstacle_sprites]) # Bir Tile oluşturuyoruz.(taş)
        if col == 'p': # Dünya haritamızdaki her bir p değeri bizim için bir oyuncu çizeceğimiz anlamına geliyor.
          self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites) # Bir Player oluşturuyoruz.(oyuncu)
          # Player'ın konumunu, bulunduğu grubu ve player'ın çarpışma yapabilmesi için gerekli objelerin bulunduğu sprite grubunu tanımlıyoruz.
    """
  # 2- CSV dosyasından bir map yükleyeceğiz. Yine aynı mantıkta dosyayı okuyup çizdireceğiz.
    layouts = { # Bir harita düzeni oluşturuyoruz.
        'boundary': import_csv_layout('map/map_FloorBlocks.csv'), # Sınırlarımız için csv dosyasını çalışılabilir hale getirecek bir metot yazacağız.
        # Metoda bir path vereceğiz ve bu dosyayı alıp işleyecek. İşledikten sonra aynı eski harita gibi yerleştirmek istiyorum.
        'grass': import_csv_layout('map/map_Grass.csv'), # csv dosyasını işleyip grassları oluşturacağız. Grassların konumunu alıyoruz aslında.
        'object': import_csv_layout('map/map_Objects.csv'), # csv dosyasını işleyip nesneleri oluşturacağız. Objectlerin konumunu alıuyoruz aslında.
        'entities': import_csv_layout('map/map_Entities.csv') # csv dosyasını işleyip entityleri oluşturacağız. Entitylerin konumunu alıyoruz aslında.
    }

    graphics = { # Bir grafik dictionary'si oluşturuyoruz.
        'grass': import_folder('graphics/Grass'), # Oluşturduğumuz metot ile verilen konumdaki tüm resimleri bir surface olarak getiriyoruz liste içerisinde.
        'objects': import_folder('graphics/objects') # Oluşturduğumuz metot ile verilen konumdaki tüm resimleri bir surface olarak getiriyoruz liste içerisinde.
    }

    for style,layout in layouts.items(): # Layout içerisindeli key'leri (boundary ve graphic gibi) style'a haritayı veren listeyi de layout'a atıyoruz.
      for row_index,row in enumerate(layout): # Layout içerisindeki her bir satır ve numarasını y ekseni için alıyoruz.
        for col_index,col in enumerate(row): # Her bir satırın kolon numarasını da x ekseni için alıyoruz.
          if col != '-1': # Eğer colon -1 değilse yani boş değil bir nesne var ise.
            x = col_index * TILESIZE # Her bir elemanın x pozisyonu
            y = row_index * TILESIZE # Her bir elemanın y pozisyonu

            if style == 'boundary': # Eğer style'ımız boundary ise yani sınır ise
              Tile((x,y),[self.obstacle_sprites],'invisible') # Yeni bir Tile oluşturuyoruz. (pos,group,sprite_type,surface parametrelerini alacak.)
              # x,y koordinatlarına ve görünmeyen obstacles_sprites grubuna atıyoruz. surface vermediğimiz için siyah bir blok oluşturacak fakat onu göremeyeceğiz.
            if style == 'grass': # Eğer grass ise style'ımız bir grass tile'ı oluşturacağız.
              random_grass_image = choice(graphics['grass']) # Random modülünden choice metodu yardımıyla rastgele bir surface seçiyoruz.
              Tile((x,y),[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],'grass',random_grass_image) # Ve grass tile'ımızı oluşturuyoruz.
              # Grass objesi aynı zamanda self.attackable_sprites içerisinde olmalı ki collision olduğunda yok olsun.
            if style == 'object': # Eğer object ise style'ımız bir object tile'ı oluşturacağız.
              surf = graphics['objects'][int(col)] # Tiles üzerinde her bir ağacın belli bir konumu var. Bu nedenle rastgele seçim yapamıyoruz.
              # Bunu önlemek için str kolon numarasını integer'a çevirerek o indeksteki fotoğrafı getiriyoruz. Yani liste içerisinden onu seçiyoruz.
              Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf) # Ve objemizi oluşturuyoruz.
              # Fakat bu işlem nesneler büyük olduğu fakat Tile classında 64*64 kabul ettiğimiz için üst üste oluşumlar yaratıyor. Bu problemi o class içerisinde çözüyoruz.
            if style == 'entities': # Eğer style'imiz entities ise:
              if col == '394': # Ve colon numarası 394 ise (394=player)
                self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack,self.create_magic) # Metodu çalıştırmıyoruz sadece çağırıyoruz. İle player oluşturuyoruz.
              else: # Eğer değilse her biri için bir düşman oluştur.
                if col == '390': # Eğer layouttaki sayı 390 ise bir bamboo
                  monster_name = 'bamboo'
                elif col == '391': # Eğer 391 ise bir spirit
                  monster_name = 'spirit'
                elif col == '392': # Eğer 392 ise bir raccoon
                  monster_name = 'raccoon'
                else: # Eğer hiçbiri değilse bir squid oluşturmak için monster_name'leri ayarla.
                  monster_name = 'squid'
                Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.damage_player,self.trigger_death_particles,self.add_exp) # Bir düşman nesnesi oluşturduk. Daha sonra her bir sayı değeri için farklı bir canavar oluşturacağız.
                # Ve tekrar collision için tüm obstacle_sprites'lara bakıyoruz ve bunu düşmanlar için de tanımlamalıyız.
                # sprite grupları arasına self.attackable_sprites'ı da ekliyoruz.
                # player'a hasar verebilmesini sağlayacak olan metodu da veriyoruz.
                # Ölüm animasyonu için bir metot daha veriyoruz.
                # add_exp ile öldüklerinde player'a exp vermelerini istiyoruz. Enemy içerisinde metodu çağıracağız.
    # 1-
     # self.player = Player((2000,1430),[self.visible_sprites],self.obstacle_sprites) # Karakterimizi çizdirdik ekrana.
    # 2- self.player oluştururken aşağıdaki create_attack metodunu da bir parametre olarak vermeliyiz ki attack inputunu alabilelim ve bu metodu oraya taşıyabilelim.
    #self.player = Player((2000,1430),[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack,self.create_magic) # Metodu çalıştırmıyoruz sadece çağırıyoruz.
    # Player nesnesinin tüm parametrelerini verdik. create_attack, destroy_attack ve create_magic metotlarına Level içerisinden de ulaşabilmek için Player'ın bir parametresi olarak veriyoruz.

  def create_attack(self): # Bu metot ile player içerisinde oluşturduğumuz attack inputu'nu burada da alabileceğiz. Level'da bir weapon oluşsun ki düşmanla etkileşime girebilsin.
    self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites]) # Weapon nesnemizi oluşturuyoruz. Her bir create_attack metodu çalıştığında. 2 parametresi var ve ilki player ikincisi ise group.
    # Ve current_attack değişkenine veriyoruz ki ekranda bir silah sprite'ı var mı yok mu kontrol edebilelim.
    # self.player'ı create_map içerisinde oluşturmuştuk bu şekilde çağırabiliriz.
    # Ve görünür olması için şu anlık sadece visible_sprites grubuna dahil ediyoruz.
    # create_attack metodunu player nesnesine bir parametre olarak veriyoruz ki player içerisinde kullanabilelim.
    # Silah sprite'ı oluştuğunda onu aynı zamanda self.attack_sprites içerisine koyacağım.

  def create_magic(self,style,strength,cost): # Bizim için büyü oluşturacak metodu yazıyoruz.
    if style == 'heal': # Eğer heal büyüsünü kullanıyorsak.
      self.magic_player.heal(self.player,strength,cost,[self.visible_sprites]) # MagicPlayer class'ından oluşturduğumuz magic_player nesnesi üzerinden heal metodunu çağırıyoruz.
      # paramatre olarak player'ı strength ve cost'u vereceğiz.

    if style == 'flame': # Eğer flame büyüsünü kullanıyorsak.
      self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])
      # player'ı vereceğiz.
      # cost ise costu olacak
      # visible_sprites da grubu olacak fakat sonradan attack_sprites'ı da ekleyeceğiz. EKLEDİK.

    # style hangi tarzda bir büyü olduğunu, strength büyü gücünü ve cost ise maliyetini tutacak.

  def destroy_attack(self): # Oluşturduğumuz silah sprite'larını ekrandan tekrar silecek olan metodu yazıyoruz.
    if self.current_attack: # Eğer ekranda bir silah sprite'ı varsa silebilsin diye kontrol ediyoruz.
      self.current_attack.kill() # Ve sprite'ı ekrandan siliyoruz.
    self.current_attack = None # En son olarak da tekrar değişkenimizi None yapıyoruz.

  def player_attack_logic(self): # bu metot ile attack_sprites içerisinin tamamını tek tek döneceğiz ve herhangi bir attackable_sprites ile collide yapmış mı ona bakacağız.
    if self.attack_sprites: # Eğer bir attack_sprites'ı varsa ekranda
      for attack_sprite in self.attack_sprites: # attack_sprites içerisindeki her bir attack_sprite için
        collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False) # pygame.sprite.spritecollide(sprite,group,DOKILL) parametrelerini alır. Son parametre dokunulan nesneyi yok eder.
        # self.attackable_sprites içerisindeki herhangi bir sprite ile collide yapıyor mu bakıyoruz. (spritecollide grup içerisindeki her bir sprite için kontrol ediyor.)
        # Bu komut bize bir liste döndürecek.
        if collision_sprites: # Eğer herhangi bir collision varsa.
          for target_sprite in collision_sprites: # Silahımızın temas ettiği her bir nesne için
            # Eğer sprite_type'ı bir çimen ise o yok olmalı.
            # Eğer bir düşman ise canı azalmalı.
            # target_sprite.kill() # Denemek için temas ettiğimiz tüm nesneleri yok ediyoruz.
            if target_sprite.sprite_type == 'grass': # her bir sprite için kendi oluşturduğumuz sprite_type değişkenine bakıyoruz.
               # Şimdi bu kısma eğer temas varsa çimen yok olma efekti ekleyeceğiz.
               pos = target_sprite.rect.center # Hedef sprite'ımızın konumunu alıyoruz ki oraya ekleyelim efekti.
               offset = pygame.math.Vector2(0,75) # Offset ekleyerek daha gerçekçi yapıyoruz.
               for leaf in range(randint(1,6)): # Her bir yok olma animasyonu için içerisinden 3-6 arasında efekt çağırıyorum ki gerçekçi olsun.
                self.animation_player.create_grass_particles(pos - offset,[self.visible_sprites])
               # Bu metot pos ve groups parametrelerini alıyor.
               target_sprite.kill() # Çimeni yok ediyoruz.
            else:
              target_sprite.get_damage(self.player,attack_sprite.sprite_type) # Düşmanın hasar almasını sağlayan metodu çağıracağız.
            # self.player parametresini player'ın ne yaptığını öğrenmek için aldık.
            # attack_sprite.sprite_type ile büyü mü yoksa silah mı kullandığımıza bakacağız.
            # get_damage metodunu Enemy içerisinde oluşturacağız.

  def damage_player(self,amount,attack_type): # Bu metot ile düşmanlar player'a hasar verebilecek. Bu metodu canavarları Level içerisinde oluşturuken bir parametre olarak vereceğim.
  # amount hasar miktarını alacak ve attack_type ise monster_data içerisinden saldırı türünü alacak ve ona göre partikül ekleyeceğiz.
    if self.player.vulnerable: # Eğer karakterimiz hasar alabilecek durumda ise.
      self.player.health -= amount # Amount kadar player'ın canını azaltıyoruz.
      self.player.vulnerable = False # Ve karakterimizin tekrar hasar alabilmesi için bir timer oluşturmak için hasar almayı kapatıyoruz. Timer ile bunu tekrar True yapacağız.
      self.player.hurt_time = pygame.time.get_ticks() # Timer için gereken zamanlayıcıyı oluşturacak olan zaman tutucu.
      
      # Partikül efektleri
      self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites]) # Partikülleri oluşturacak olan metot.
      # Karakter hasar alırken ne tür bir hasar almış ona bakacağız ve ona göre animasyon oluşturacağız. Attack_type'ı yukarıdaki metot içerisinden alıyoruz.
      # Animasyonu nerede oluşturacağım onun için pos
      # Ve hangi grupta olacak onun için de groups
      # Bu metodu particles içerisinde oluşturacağız.

  def trigger_death_particles(self,pos,particle_type): # Düşman öldüğünde animasyonları tetikleyecek olan metot.
    self.animation_player.create_particles(particle_type,pos,self.visible_sprites) # create_particles(animation_type,pos,groups)
    # animasyon türü için particle type'ı alacağım.
    # pos için pos alacağım
    # grup için ise görünür sprite'ları kullanacağım.
    # Bu metodu enemy oluşumunda parametre olarak vereceğim ki Level'da oluşturduğum metotu enemy içerisinde de kullanabileyim.

  def add_exp(self,amount): # Player'ın her düşman öldürdüğünde ondan xp alacağı metot.
    # Bu metodu Enemy içerisinde çağıracağım. Bu nedenle Level içeirisinde Enemy oluştururken parametre olarak vereceğim.
    self.player.exp += amount # Verilen miktar kadar karakterin exp'sini arttır.

  def toggle_menu(self): # Oyunda m tuşuna basıldığında menüyü açacak olan metot.
    self.game_paused = not self.game_paused # Oyunu bir başlatıp bir durdurmamızı sağlayacak.

  def run(self): # Oyunu güncelleyip çizecek olan metot.
    self.visible_sprites.custom_draw(self.player) # Kendi oluşturduğumuz çizme metodu ile çizdiriyoruz. Ve parametre olarak self.player'ı veriyoruz. Bunu her zaman çizeceğimiz için bloklar içerisine koymadık.
    # Görünecek olan spriteların bulunduğu grubu çiziyoruz.
    self.ui.display(self.player) # UI class'ı üzerinden oluşturduğumuz self.ui üzerinden display metodu aracılığıyla verdiğim player parametresinin statlarını gösteren bir arayüz oluşturacağız. Bunu her zaman çizeceğimiz için bloklar içerisine koymadık.

    if self.game_paused: # Eğer oyun durmuşsa
      self.upgrade.display() # Ekrana upgrade menüsünü oluşturan metodu çağırdım. (upgrade nesnesi üzerinden.)
      # Geliştirme ekranını açacağım
    else: # Eğer oyun devam ediyorsa.
      # Oyunu devam ettiriyoruz.
      self.visible_sprites.update() # update metodu ile spriteların hareketlerini kontrol edebiliriz. 
      self.visible_sprites.enemy_update(self.player) # Enemy class'ı için gerekli olan self.player parametresini veriyor ve düşman durumlarını güncelleyen metotu çağırıyorum. Fakat oyun devam ediyorsa hareketlerini güncelleyeceğiz. 
      self.player_attack_logic() # Silah ve düşman ya da nesne etkileşimine bakan metodu çağırıyoruz.

class YSortCameraGroup(pygame.sprite.Group): # Kendim bir sınıf oluşturdum ve bunun bir grup olduğunu söyledim
  def __init__(self):

    # genel ayarlar
    super().__init__()
    self.display_surface = pygame.display.get_surface() # Burası içerisine yeni bir display ekranı oluşturduk.

    self.half_width = self.display_surface.get_size()[0] // 2 # Ekranın genişliğinin yarısını alıyoruz.
    self.half_height = self.display_surface.get_size()[1] // 2 # Ekranın uzunluğunun yarısını alıyoruz.

    self.offset = pygame.math.Vector2() # Kamera için  kaymayı tutacağımız bir vektör oluşturduk. Default'u (0,0) verir.
  
    # zeminin oluşturulması (fotoğraftan oluşacak ve her zaman en altta olacak bu nedenle for döngüsünün üstüne yazdık.)
    self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert() # Zeminin fotoğrafıonı yükledik.
    self.floor_rect = self.floor_surf.get_rect(topleft = (0,0)) # Fotoğrafı verilen rect'ini oluşturduk.

  def custom_draw(self,player): # Kendi yaptığımız çizim metodunu yazıyoruz. Çünkü kamera için hepsini tek tek tekrar çizdireceğiz.
    # player parametresi kamera için oyuncunun konumuna ulaşmamız için gerekli

    # kayma miktarını getirmek
    self.offset.x = player.rect.centerx - self.half_width # x eksenindeki kayma miktarı için oyuncunun rect'inin x koordinatından sayfa genişliğinin yarısını çıkarıyoruz.
    self.offset.y = player.rect.centery - self.half_height # y eksenindeki kayma miktarı için oyuncunun rect'inin y koordinatından sayfa uzunluğunun yarısını çıkarıyoruz.

    # zemini çizme
    floor_offset_pos = self.floor_rect.topleft - self.offset # kamera için zeminin kayma miktarını aldık.
    self.display_surface.blit(self.floor_surf,floor_offset_pos) # Display ekranımıza verilen resmi kayma miktarıyla çiziyoruz.

    # 1- 
       # for sprite in self.sprites(): # Gruptaki tüm sprite'lar için
    # 2- Y pozisyonlarına göre sıralama yapacağız çünkü karakterden sonra çizilenler karakterin önünde kalıyor.
    for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery): # Tüm spriteların y konumlarını alıyoruz ve buna göre sorted metodunda sıralama yapılacağını söylüyoruz.(self.sprites()(gruptaki spritelar) üzerinde yapılacak bu işlem)
      # Y posizyonlarına göre çizdiriyoruz. Yani her çizildiğinde konunları alıp sıralıyoruz bu şekilde overlap'i sağladık.
      offset_pos = sprite.rect.topleft - self.offset # Her bir sprite'ın sol üst konumuna belirtmiş olduğumuz kaymayı çıkararak yeni bir değişkene atadık.
       # self.display_surface.blit(sprite.image,sprite_rect) # Display ekranınıa her bir sprite'ın image ve rect'ini çiziyoruz.
      self.display_surface.blit(sprite.image,offset_pos) # Aldığımız değerleri verilen konumda çizdiriyoruz.

  def enemy_update(self,player): # Her bir düşmanı güncelleyecek metot. Ayrıca player parametresini de verebiliyorum. Bunu run metodu içerisinde çağıracağım.
    enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy'] # Tüm düşman sprite'larını içeren liste
    # Tüm spriteslar arasından sadece enemyleri alacağım. Mesela Tile class'ı ve Enemy class'ı kendine ait bir sprite_type'ı var.
    # hasattr metodu önce neye bakacağını sonra da hangi attr'a bakacağına bakar. Eğer varsa ve enemy ise al ve listeye ekle diyoruz.
    for enemy in enemy_sprites: # Her bir düşman için
      enemy.enemy_update(player) # Düşman hareketlerini ve durumunu kontrol eden metodu çalıştır.