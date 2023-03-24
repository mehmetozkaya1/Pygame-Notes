import pygame
# destek dosyaları için ayrı bir bölmeyi kullanıyoruz.
from csv import reader # csv modülü içerisinden reader'ı çağırıp csv dosyasını okuyacağız.
from os import walk # import_folder metodu için walk metodunu aldık.

def import_csv_layout(path): # bu metot ile csv dosyalarını işlenebilir hale getirip dünyamızı oluşturacağız.
  terrain_map = [] # bir liste oluşturuyoruz.
  with open(path) as level_map: # csv dosyasını with komutuyla açıyoruz.
    layout = reader(level_map, delimiter= ',') # reader komutuna okunacak dosyayı ve hangi yerlerden parçalanacağını belirtiyoruz.
    for row in layout: # layout içerisindeki her bir satırı yazdırıyoruz.
      terrain_map.append(list(row)) # Listeye tüm satırları liste olarak veriyoruz.
    return terrain_map # ve bu listeyi döndürüyoruz. Listelerden oluşan bir liste

# Bu işlem bize -1 ve 395 gibi sayılardan oluşmuş bir listeler bütünü verecek yukarıdaki world map gibi. -1'ler
# -1'ler bizim için boş olanları 395'ler ise bizim için bir entity'nin yerini tutacak. Yani 395'lerin içinden geçilmeyecek. Sınır alanları gibi.

def import_folder(path): # Bizim 3 farklı grass ve 20 farklı object'imiz var. Bu nedenler hepsini tek bir seferde resmini alıp bir surface a çeviren bir metot yazmamız gerekiyor.
  surface_list = []
  
  for _,__,img_files in walk(path): # walk metodu bizim için önce dosyanın konumunu sonra içindeki klasörleri bir liste şeklinde ve en sonda da içindeki dosyaları bir liste içerisinde getirir.
    # _ = dosya yolunu tutuyor gereksiz.
    # __ = alt klasörleri tutuyor gereksiz.
    # img_files = png'leri tutuyor gerekli.
    # Bu metot ile her bir fotoğrafın tam dosya konumuna ulaşıp onu pygame'e yükleyecek ve surface'a çevireceğiz.
    for image in img_files: # Her bir png için
      full_path = path + '/' + image # Her bir png için tam bir dosya yolu oluşturduk.
      image_surf = pygame.image.load(full_path).convert_alpha() # Her bir png'yi ise bir surface'a dönüştürüyoruz ve listeye atacağız.
      surface_list.append(image_surf)
  return surface_list # En son olarak da bu listeyi döndürüyoruz.