# Settings

WIDTH = 1280 # Ekran genişliği
HEIGHT = 720 # Ekran boyutu
FPS = 60 # FPS
TILESIZE = 64 # Her bir parçanın genişliği kaç px olsun.

# Nesneler için farklı hitbox değerleri
HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'invisible': 0
}

# ui bilgileri
BAR_HEIGHT = 20 # UI bar uzunluğu
HEALTH_BAR_WIDTH = 200 # Can barı genişliği
ENERGY_BAR_WIDTH = 140 # Enerji barı genişiliği
ITEM_BOX_SIZE = 80 # Silah ve büyü çerçevesi
UI_FONT = 'graphics/font/joystix.ttf' # UI fontu
UI_FONT_SIZE = 18 # UI font yazı büyüklüğü

# genel renkler
WATER_COLOR = '#71ddee' # Su rengi
UI_BG_COLOR = '#222222' # UI arkaplan rengi
UI_BORDER_COLOR = '#111111' # UI çerçeve rengi
TEXT_COLOR = '#EEEEEE' # Text rengi

# ui renkleri
HEALTH_COLOR = 'red' # Can barı rengi
ENERGY_COLOR = 'blue' # Enerji barı rengi
UI_BORDER_COLOR_ACTIVE = 'gold' # UI aktif çerçeve rengi

# geliştirme ekranı bilgileri
TEXT_COLOR_SELECTED = "#111111" # Seçili text rengi
BAR_COLOR = "#EEEEEE" # Bar rengi
BAR_COLOR_SELECTED = "#111111" # Seçili bar rengi
UPGRADE_BG_COLOR_SELECTED = "#EEEEEE" # Seçili arkaplan rengi

# silah bilgileri
weapon_data = { # Silahlarımızı içeren bir data.
    'sword': {'cooldown':100, 'damage':15, 'graphic': 'graphics/weapons/sword/full.png'},
    'lance': {'cooldown':400, 'damage':30, 'graphic': 'graphics/weapons/lance/full.png'},
    'axe': {'cooldown':300, 'damage':20, 'graphic': 'graphics/weapons/axe/full.png'},
    'rapier': {'cooldown':50, 'damage':8, 'graphic': 'graphics/weapons/rapier/full.png'},
    'sai': {'cooldown':80, 'damage':10, 'graphic': 'graphics/weapons/sai/full.png'},
}

# büyü bilgileri
magic_data = { # Büyü bilgilerini tutan bir data.
    'flame': {'strength':5,'cost':20,'graphic':'graphics/particles/flame/fire.png'},
    'heal': {'strength':20,'cost':10,'graphic':'graphics/particles/heal/heal.png'}
}

# düşmanlar
monster_data = { # Düşman bilgilerini tutan data.
    'squid': {'health':100, 'exp':100, 'damage':20, 'attack_type':'slash', 'attack_sound':'audio/attack/slash.wav', 'speed':3, 'resistance':3, 'attack_radius':80, 'notice_radius':360},
    'raccoon': {'health':300, 'exp':250, 'damage':40, 'attack_type':'claw', 'attack_sound':'audio/attack/claw.wav', 'speed':2, 'resistance':3, 'attack_radius':120, 'notice_radius':400},
    'spirit': {'health':100, 'exp':110, 'damage':8, 'attack_type':'thunder', 'attack_sound':'audio/attack/fireball.wav', 'speed':4, 'resistance':3, 'attack_radius':60, 'notice_radius':350},
    'bamboo': {'health':70, 'exp':120, 'damage':6, 'attack_type':'leaf_attack', 'attack_sound':'audio/attack/slash.wav', 'speed':3, 'resistance':3, 'attack_radius':50, 'notice_radius':300},
} # resistance düşmana vurulduğunda arkaya fırlatılma değeridir.

# WORLD_MAP = [ # Oyun dünyamız Her bir karakter arası TILESIZE = 64 px olacak. Artık gerek yok.
# ['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
# ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
# ['x',' ','p',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
# ['x',' ',' ','x',' ',' ',' ',' ',' ','x','x','x','x','x',' ',' ',' ',' ',' ','x'],
# ['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
# ['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
# ['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
# ['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
# ['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
# ['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
# ['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
# ['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x','x','x',' ',' ',' ','x'],
# ['x',' ',' ',' ',' ',' ',' ','x',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
# ['x',' ',' ',' ',' ',' ','x','x','x','x','x',' ',' ',' ',' ',' ',' ',' ',' ','x'],
# ['x',' ',' ',' ',' ',' ',' ','x','x','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
# ['x',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
# ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
# ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
# ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
# ['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
# ]