# UI kısmını oluşturacağımız bölüm:

import pygame
from settings import *

class UI: # UI oluşturmak için bir UI sınıfı oluşturuyoruz.
  def __init__(self):
    
    # Genel bilgiler
    self.display_surface = pygame.display.get_surface() # Bir display ekranına ihtiyacımız var.
    self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE) # settings içerisindeki değişkenleri kullanarak fontu oluşturuyoruz.

    # bar ayarları
    self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT) # can barı için bir rect oluşturuyoruz. (Rect(left,top,width,height))
    self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT) # enerji barı için bir rect oluşturuyoruz. (Rect(left,top,width,height))

    # Silah sözlüğünü listeye çevirme işlemi (Silah UI kısmı için.)
    self.weapon_graphics = [] # Silah grafiklerini tutacak olan listeyi oluşturuyoruz.
    for weapon in weapon_data.values(): # Silah bilgileri'nin value kısımlarıyla ilgileneceğim ve elime bir sözlük daha gelecek.
      path = weapon['graphic'] # Silah'ların grafik kısımlarını bir path'e atıyoruz.
      weapon = pygame.image.load(path).convert_alpha() # Silah fotoğraflarını bir surface haline getiriyorum ve weapon değişkenine atıyoruz.
      self.weapon_graphics.append(weapon) # Listeme bu silah surface'ımı ekliyorum.
    
    # Büyü sözlüğünü listeye çevirme işlemi (Büyü UI kısmı için.)
    self.magic_graphics = [] # Büyü grafiklerini tutacak olan listeyi oluşturuyoruz.
    for magic in magic_data.values(): # Büyü bilgileri'nin value kısımlarıyla ilgileneceğim ve elime bir sözlük daha gelecek.
      path = magic['graphic'] # Büyü'lerin grafik kısımlarını bir path'e atıyoruz.
      magic = pygame.image.load(path).convert_alpha() # Büyü fotoğraflarını bir surface haline getiriyorum ve magic değişkenine atıyoruz.
      self.magic_graphics.append(magic) # Listeme bu büyü surface'ımı ekliyorum.

  def show_bar(self,current,max_amount,bg_rect,color): # Bu esnek metot ile şuanki can ya da enerji, maks can ya da enerji, rect arkaplan rengi ve renk değişkenlerini alarak ekrana gösteren bir metot yazıyoruz.
    # arkaplanın çizilmesi:
    pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect) # pygame.draw.rect(surface,color,rect) parametrelerini alır.

    # Statların pixel'e dönüşümü:
    ratio = current / max_amount # ratio değişkeni pixellere göre canın durumunu çizmek için gerekli olan oran değişkenimiz.
    current_width = bg_rect.width * ratio # arka plandaki rect'in uzunluğu ile ratio oranını çarparak bir genişlik elde ediyorum. Bu da bizim statımızın şu anki değeri olacak.
    current_rect = bg_rect.copy() # arkadaki rect'i kopyaladım.
    current_rect.width = current_width # Ve kopyaladığım rect'in genişliğini aldığım değişkenle değiştirdim.

    # Barın çizilmesi:
    pygame.draw.rect(self.display_surface,color,current_rect) # pygame.draw.rect(surface,color,rect) parametrelerini alır.
    # color değişkeni parametre olan değişken.
    pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3) # Var olan rect üzerine (bg_rect yani arkaplan) yeni bir rect çiziyorum fakat satır genişliğini 3 vererek aslında bir çerçeve oluşturuyorum.
    # UI_BORDER_COLOR ise settings den geliyor.

  def show_exp(self,exp):
    text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR) # self.font üzerinden render(info,AA(anti_aliasing(pixel olduğu için kullanmayacağız.)),color) metodunu çağırıyoruz.
    # TEXT_COLOR settings den gelen renk.
    # exp'yi ise player init içerisinde bulunan self.exp ile getireceğiz ve str'e çevireceğiz.
    x = self.display_surface.get_size()[0] - 20 # ekran botunu (x,y) ile geitirip x'ini aldık.
    y = self.display_surface.get_size()[1] - 20 # ekran botunu (x,y) ile geitirip y'ini aldık.
    text_rect = text_surf.get_rect(bottomright = (x,y))

    pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20)) # text rect'imizin üzerine bir arkaplan rect'i çiziyoruz.
    # Fakat siyah arkaplanın biraz daha geniş olabilmesi için text_rect üzerine inflate metodunu uygulayabiliriz.

    pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3) # text rect'imizin üzerine bir arkaplan rect'i çiziyoruz.
    # Arkaplanımız için bir çerçeve oluşturuyoruz. Son parametre bizim rect genişliğimiz.

    self.display_surface.blit(text_surf,text_rect) # Ve ekrana yazımız ve rect'ini çizdiriyoruz.

  def selection_box(self,left,top,has_switched): # Silah ve büyü seçenekleri için bir kutucuk oluşturacağız.
    # left ve top pozisyonları için gerekli olan parametreler.
    # has_switched parametresi ile de silah değiştiriyor muyum buna bakacağım. Eğer silah değiştiriyorsam silah UI çerçevesinin rengini silah değiştirme işlemi boyunca değiştireceğim.
    bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE) # pygame.Rect(left,top,w,h) parametrelerini alır. Arkaplan için bir rect oluşturuyoruz.
    # left ve top parametre olarak geliyor.
    # w, h değişkenleri için settingsden değişken getiriyoruz.
    pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect) # Oluşturduğumuz rect'i ekranımızıa verilen renkte çizdiriyoruz..

    if has_switched: # Eğer silah değiştirme işlemi yapıyorsak çerçeve rengini bu işlem boyunca farklı bir renk yapacağız.
      pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3) # (Eğer silah değiştirmiyorsak) Oluşturduğumuz rect'in etrafına bir çerçeve oluşturuyoruz. Renk değiştirip en son da genişlik değerini veriyoruz.
    else:
      pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3) # (Eğer silah değiştirmiyorsak) Oluşturduğumuz rect'in etrafına bir çerçeve oluşturuyoruz. Renk değiştirip en son da genişlik değerini veriyoruz.
    
    return bg_rect # weapon_overlay metodu png'yi yerleştirmek için bg_rect'in pozisyonuna ihtiyaç duyuyor bu nedenle de bg_rect'i döndürmeli.

  def weapon_overlay(self,weapon_index,has_switched): # Bu metot ile hangi silah seçiliyse kutucuğa onun fotoğrafını koyacağız. Bu nedenle silah indeksini getirmemiz gerekiyor.
    # has_switched parametresi selection_box için gerekli olan parametre.
    bg_rect = self.selection_box(10,630,has_switched) # Silah kutucuğumuzu çizdiriyoruz.
    # selection_box metodu bg_rect'i döndürüyor ve biz de bu bg_rect'i kullanabiliriz. Değişkenin ismini değiştirmeden tekrardan atıyoruaz.
    weapon_surf = self.weapon_graphics[weapon_index] # Silah index'imize göre listeden doğru olan surface seçimini yapıp rect'e yerleştirecek.
    weapon_rect = weapon_surf.get_rect(center = bg_rect.center) # Ve silah rect'ini de bg_rect ile merkezleri çakışacak şekilde yerleştiriyorum.

    self.display_surface.blit(weapon_surf,weapon_rect) # display ekranımıza rect ve surface'ı çizdiriyoruz.
    # weapon_surf için settings içerisindeki weapon_data içindeki silah indeksine göre seçim yaptıktan sonra oradaki png'nin surface'a dönüşmüş halini getireceğim.
    # weapon_rect ise merkezi bg_rect ile aynı yerde olacak olan rect olacak.

  def magic_overlay(self,magic_index,has_switched): # Bu metot ile hangi büyü seçiliyse kutucuğa onun fotoğrafını koyacağız. Bu nedenle büyü indeksini getirmemiz gerekiyor.
    # has_switched parametresi selection_box için gerekli olan parametre.
    bg_rect = self.selection_box(80,635,has_switched) # Büyü kutucuğumuzu çizdiriyoruz.
    # selection_box metodu bg_rect'i döndürüyor ve biz de bu bg_rect'i kullanabiliriz. Değişkenin ismini değiştirmeden tekrardan atıyoruaz.
    magic_surf = self.magic_graphics[magic_index] # Büyü index'imize göre listeden doğru olan surface seçimini yapıp rect'e yerleştirecek.
    magic_rect = magic_surf.get_rect(center = bg_rect.center) # Ve Büyü rect'ini de bg_rect ile merkezleri çakışacak şekilde yerleştiriyorum.

    self.display_surface.blit(magic_surf,magic_rect) # display ekranımıza rect ve surface'ı çizdiriyoruz.
    # magic_surf için settings içerisindeki magic_data içindeki büyü indeksine göre seçim yaptıktan sonra oradaki png'nin surface'a dönüşmüş halini getireceğim.
    # magic_rect ise merkezi bg_rect ile aynı yerde olacak olan rect olacak.

  def display(self,player): # oluşturduğumuz rect'leri ekrana çizmemizi sağlayan metot.
    # fakat can barını burada çizdirmeyeceğiz.
     # pygame.draw.rect(self.display_surface,'black',self.health_bar_rect) # pygame.draw.rect(surface,color,rect) parametrelerini alır.
    self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
    # player.health ile player'ın şuanki can durumunu alıyoruz.
    # player.stats['health'] ile player maks can değerini alıyoruz.
    # self.health_bar_rect ile can barının bulunacağı yeri alıyoruz.
    # HEALTH_COLOR ile can rengini alıyoruz.
    self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)
    # player.energy ile player'ın şuanki enerji durumunu alıyoruz.
    # player.stats['energy'] ile player maks enerji değerini alıyoruz.
    # self.energy_bar_rect ile can barının bulunacağı yeri alıyoruz.
    # ENERGY_COLOR ile can rengini alıyoruz.

    self.show_exp(player.exp) # Show_exp metodu ile de tecrübe puanımızı yazdıran bir metot yazacağız.
    # player'ı display metodu parametresinden getirdik.

    self.weapon_overlay(player.weapon_index,not player.can_switch_weapon) # Silahımızı ve büyümüzü ekrana çizdiriyoruz.
    # weapon_index ve can_switch_weapon parametrelerini de veriyoruz. (can_switch_weapon'ı not verip alıyoruz çünkü silah değiştirebilme durumunda değil silah değiştirirken yani değiştirememe durumunda renk değişimi yapacağız.)
    self.magic_overlay(player.magic_index,not player.can_switch_magic) # Aynısından bir de büyü kutucuğu için çizdiriyoruz.