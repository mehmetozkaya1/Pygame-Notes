# upgrade.py dosyası ile exp ile geliştirme yapacağımız ekranı çizdireceğiz.

# Çalışma mantığı:
# 0-4'e kadar bir index numarası oluşturacağız ve her biri can enerji gibi statları temsil edecek.
# Her bir stat için ayrı bir class oluşturacağız. Her biri için de bir rect.
# Index numarasına göre seçtiğimiz rect'i belli edeceğiz.
# Sol ve sağ tuşları ile bu index numarasını değiştirirken, space tuşu ile de geliştirme işlemini yapacağız.

import pygame
from settings import *

class Upgrade: # Bu işlem için bir class oluşturuyoruz.
  def __init__(self,player): # Ve parametre olarak player'ı veriyoruz.

    # Genel ayarlar
    self.display_surface = pygame.display.get_surface() # Bir display ekranı oluşturduk.
    self.player = player # player'ı da parametre olarak verdik.
    self.attribute_nr = len(player.stats) # Player statları'ının sayısını tutan değişken
    self.attribute_names = list(player.stats.keys()) # Player stats dictionarisi içerisindeki key'leri alıp bir listeye çevirdik.
    self.max_values = list(player.max_stats.values()) # Her bir değerin maksimum değeri. player içerisinden max_stats dict'inin değerlerini list'e çevirip alacağız.
    self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE) # Ve ekranda göreceğimiz yazı font ve boyutu.

    # Eşya oluşturma
    self.height = self.display_surface.get_size()[1] * 0.8 # Her bir rect boyutu için ekran boyutunun y parametresini aldım ve yüzde 80'ini aldım.
    self.width = self.display_surface.get_size()[0] // 6 # Her bir rect boyutu için ekran boyutunun x parametresini aldım ve 6'ya böldüm. 1 parça da padding olacak.
    self.create_items() # init içerisinde direkt item'ları oluşturan metodu çağırıyoruz.

    # Seçim sistemi
    self.selection_index = 0 # Seçim için gereken index
    self.selection_time = None # Bir timer oluşturmamız lazım çünkü bir kere basıldığında 60 kere tetiklenecek.
    self.can_move = True # Ve tekrar seçim yapabilmemizi sağlayan değişken.

  def input(self): # Kullanıcıdan geliştirme yapmak için input alan metot.
    keys = pygame.key.get_pressed() # Tüm tuşları çağırıyoruz.

    if self.can_move: # Eğer hareket ettirebiliyorsak.
      if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr -1 : # Eğer sağ tuşa basıyorsak ve selection_index'imiz toplam attribute sayısının 1 eksiğinden(index hesabı) küçük ise çünkü en sağda isek daha fazla sağ yapamayız. Ayrıca 4'ün üstüne çıkmamızı da engelliyor.
        self.selection_index += 1 # Index'i 1 arttır.
        self.can_move = False # Hareket edebilmeyi False yap ta ki timer onu True yapana kadar.
        self.selection_time = pygame.time.get_ticks() # Timer için süreyi hesaplamaya başlıyoruz.
      elif keys[pygame.K_LEFT] and self.selection_index >= 1: # Eğer sol tuşuna basıyorsak ve selection_index'imiz 1'den büyük ya da eşit ise sola götürebilirsin.
        self.selection_index -= 1 # Index'i 1 azalt.
        self.can_move = False # Hareket edebilmeyi False yap ta ki timer onu True yapana kadar.
        self.selection_time = pygame.time.get_ticks() # Timer için süreyi hesaplamaya başlıyoruz.

      if keys[pygame.K_SPACE]: # Eğer boşluk tuşuna basıyorsak
        self.can_move = False # Hareket edebilmeyi False yap ta ki timer onu True yapana kadar.
        self.selection_time = pygame.time.get_ticks() # Timer için süreyi hesaplamaya başlıyoruz.
        # Timer kullanmazsak tek basışta 60 kere güncelleme yapar.
        self.item_list[self.selection_index].trigger(self.player) # item listemiz içeerisinden indexe göre elemanı seçip trigger metodunu çağırıyoruz.
        # Her space'e basıldığında gerçekleşecek işlem.
    
  def selection_cooldown(self): # Seçim işleminin tekrar gerçekleşebilmesi için gereken timer.
    if not self.can_move: # Eğer hareket ettiremiyor yani bir tuşa basmışsak
      current_time = pygame.time.get_ticks() # Zamanı hesaplamaya başla
      if current_time - self.selection_time >= 300: # Eğer şu anki zamanla hareket tuşuna bastıktan sonra hesaplanan zaman 300 ms'den büyük ise,
        self.can_move = True # Tekrar hareket edebilmeyi True yap.
  
  def create_items(self): # Her bir rect'i oluşturacak metot.
    self.item_list = [] # Tüm rect'leri tutacak olan liste.

    for item,index in enumerate(range(self.attribute_nr)): # Her bir rect için item ve index numarasını aldık. Item nesnesini oluştururken index'i vereceğiz.
      # Yatay pozisyon
      full_width = self.display_surface.get_size()[0] # Tüm ekranın genişliği
      increment = full_width // self.attribute_nr # Artış miktarımız ise toplam genişliğin stat sayısına bölümü
      left = (item * increment) + (increment - self.width) // 2 # Her bir rect arasına ve kenarına offset koyuyoruz.
      # item numarası arttıkça soldan bırakılan boşluk da artıyor. Bu şekilde yan yana oluşturabiliyorum.

      # Dikey pozisyon
      top = self.display_surface.get_size()[1] * 0.1 # Yukarıdan yüzde 10'luk bir boşluk bıraktık çünkü rect boyutu ekranın yüzde 80'i
      
      # Nesnenin oluşturulması
      item = Item(left,top,self.width,self.height,index,self.font) # Parametrelerini vererek bir rect eşyası oluşturuyoruz.
      self.item_list.append(item) # Ve bunu item listesine ekliyoruz.

  def display(self): # Neler yaptığımızı görmek için bir metot oluşturuyoruz.
    self.input() # Input'ları incele
    self.selection_cooldown() # Cooldown'a bak.

    for index, item in enumerate(self.item_list): # Rect item listesindeki her bir item için

      # Değerleri alma
      name = self.attribute_names[index] # Stat ismi
      value = self.player.get_value_by_index(index) # Player içinde oluşturacağım get_value_by_index metodu ile değerleri alacağım.(vereceğim index'e göre)
      max_value = self.max_values[index] # Maksimum değer
      cost = self.player.get_cost_by_index(index) # Player içinde oluşturacağım get_cost_by_index metodu ile değerleri alacağım.(vereceğim index'e göre)

      item.display(self.display_surface,self.selection_index,name,value,max_value,cost) # item nesnesi üzerinden Item class'ı içerisindeki display() metodunu çağırıyoruz ki hepsini çizebilelim.
      # Parametrelerini veriyoruz.

class Item:
  def __init__(self,l,t,w,h,index,font):
    # l soldan alınan boşluk
    # t üstten alınan boşluk
    # w genişliği
    # h yüksekliği
    # index hangi stat'ın rectini seçtiğimiz.
    # font ise font
    self.rect = pygame.Rect(l,t,w,h) # Bir rect oluşturuyoruz ve sol üst genişlik ve uzunluk değerlerine daha önce oluşturduğumuz değerleri veriyoruz.
    self.index = index # Her bir rect'in index numarasını da tutuyoruz.
    self.font = font # Fontumuzu da alıyoruz.

  def display_names(self,surface,name,cost,selected): # Stat isimlerini oluşturacak olan metot.
    # Seçili olma durumu için selected değişkeni oluşturduk.
    
    if selected: # Eğer self.index == selection_num ise
      color = TEXT_COLOR_SELECTED # Text rengini değiştir.
    else: # Değilse
      color = TEXT_COLOR # Aynı kalsın
    
    # Başlık texti
    title_surf = self.font.render(name,False,color) # Başlık alanı için bir surface oluşturduk. Bunu font üzerinden  renderlayarak yaptık. (yazı,AA,renk)
    title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20)) # Ve bir rect oluşturuyoruz.

    # maliyet texti
    cost_surf = self.font.render(f'{int(cost)}',False,color) # Cost alanı için bir surface oluşturduk. Font üzerinden renderladık.
    cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20)) # Ve rect'ini oluşturuyoruz.

    # çizim
    surface.blit(title_surf,title_rect) # Ve ekranımıza çizdiriyoruz.
    surface.blit(cost_surf,cost_rect) # Ve ekranımıza çizdiriyoruz.

  def display_bar(self,surface,value,max_value,selected):
    # surface hangi yere çizileceğini, value anlık değeri, max_value max değeri, selected ise seçili olma durumunu gösterecek.

    # Çizim ayarları
    top = self.rect.midtop + pygame.math.Vector2(0,60) # Rect'in en yukarısından 60 birim aşağıda.
    bottom = self.rect.midbottom - pygame.math.Vector2(0,60) # Rect'in en aşağısından 60 birim yukarıda.
    color = BAR_COLOR_SELECTED if selected else BAR_COLOR # Eğer seçili veya değilse farklı renkler kullanıyoruz.

    # Bar ayarı
    full_height = bottom[1] - top[1] # bottom ve top'ın y değerlerini alıp çıkardık ki çizginin tüm uzunluğunu bulalım.
    # Ayrıca aşağıdan yukarıyı çıkardım çünkü y ekseni
    relative_number = (value / max_value) * full_height # Eğer 100 canımız varsa ve maks canımız 300 ise ben barın bu çizginin 1/3 'ünde olmasını istiyorum.
    # Ardından bu değeri toplam uzunluk ile çarpıyorum ki pixel'e çevirebilelim.
    value_rect = pygame.Rect(top[0] - 15,bottom[1] - relative_number,30,10) # (left,top,width,height)
    # left için aşağı ya da yukarının x değerini almam yeterli. Bundan da bar yüksekliğinin yarısını çıkarıyorum ki tam ortada olsun.
    # top için ise toplam y değerinden asıl değerimi çıkarıyorum. (aslında en aşağıdan o değer kadar yukarı taşıyorum.)

    # Ekrana çizim
    pygame.draw.line(surface,color,top,bottom,5) # Bir çizgi çiziyoruz. Yukarıdan aşağı ve başlangıç bitiş yerleri bulunan.
    # 5 kalınlığı
    pygame.draw.rect(surface,color,value_rect) # Barımızı çiziyoruz.

  def trigger(self,player): # space'e basıldığında geliştirmeyi yapacak metot.
    upgrade_attribute = list(player.stats.keys())[self.index] # Her space'e basıldığında liste içerisinden index'e göre olan değeri getiriyor.

    if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]: # Eğer exp'miz yeterli ise ve maks değerin altında isek
      player.exp -= player.upgrade_cost[upgrade_attribute] # Karakter exp'sini cost kadar azalt.
      player.stats[upgrade_attribute] *= 1.2 # Seçili değeri %20 arttırıyoruz.
      player.upgrade_cost[upgrade_attribute] *= 1.4 # Ayrıca istenilen exp değerini de %40 arttırıyoruz.

    if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]: # Eğer stat maksimum değerine ulaşırsa
      player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute] # İkisini birbirine eşitle.

  def display(self,surface,selection_num,name,value,max_value,cost): # Ekrana çizen metot.
    # surface üzerine çizeceğimiz yüzeyi tutacak.
    # selection_number seçili rect'in çerçevesini parlatacak
    # name ile hangi stat rect'i olduğunu yazacağız.
    # value ile geçerli olan değeri yazacağız.
    # max_value ile gelişebilecek maksimum değeri yazacağız.
    # cost ile her bir geliştirme bedelini yazacağız.

    if self.index == selection_num: # Eğer indeksimiz seçtiğimiz rect'in indexine eşitse highlighted yap.
      pygame.draw.rect(surface,UPGRADE_BG_COLOR_SELECTED,self.rect) # draw.rect(surface,color,çizilecek rect)
      pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4) # draw.rect(surface,color,çizilecek rect,border_width) # Border oluşturduk.
    else: # Eğer değilse normal şekilde dursun
      pygame.draw.rect(surface,UI_BG_COLOR,self.rect) # draw.rect(surface,color,çizilecek rect)
      pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4) # draw.rect(surface,color,çizilecek rect,border_width) # Border oluşturduk.

    self.display_names(surface,name,cost,self.index == selection_num) # İkinci parametre True ya da False döndürecek.
    self.display_bar(surface,value,max_value,self.index == selection_num) # Barları gösterecek olan metot