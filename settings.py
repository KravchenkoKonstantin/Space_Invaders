# Экран
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Игрок
PLAYER_SPEED = 5
PLAYER_LIVES = 3
INVINCIBILITY_DURATION = 2000  # мс после попадания
PLAYER_SHOOT_COOLDOWN = 300    # мс между выстрелами

# Пули
PLAYER_BULLET_SPEED = -10
ENEMY_BULLET_SPEED = 5

# Враги
ENEMY_ROWS = 3
ENEMY_COLS = 8
ENEMY_BASE_SPEED = 1.0
ENEMY_DROP_DISTANCE = 20
ENEMY_SHOOT_PROB = 0.002

# Волны
WAVE_SPEED_MULTIPLIER = 0.2 
WAVE_ENEMY_COUNT_INCREASE = 1 
BOSS_EVERY_WAVE = 5

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
CYAN  = (0, 255, 255)

IMAGE_PATH = "assets/images/"
BACKGROUND_IMG = IMAGE_PATH + "background.png"
PLAYER_IMG = IMAGE_PATH + "player.png"
ENEMY_IMGS = {
    'basic': IMAGE_PATH + "enemy_basic.png",
    'armored': IMAGE_PATH + "enemy_armored.png",
    'fast': IMAGE_PATH + "enemy_fast.png"
}
BOSS_IMG = IMAGE_PATH + "boss.png"