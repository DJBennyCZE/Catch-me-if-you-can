import pygame
import random
import sys

# Inicializace Pygame
pygame.init()

# Velikost okna
WIDTH = 800
HEIGHT = 600

# Barvy
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Vytvoření okna
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch me, if you can!")

# Inicializace hodin
clock = pygame.time.Clock()

# Třída hráče
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.lives = 3

    def update(self):
        # Pohyb hráče pomocí kláves
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

        # Udržení hráče uvnitř okna
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Třída nepřátel
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed_x = random.randint(-3, 3)
        self.speed_y = random.randint(-3, 3)

    def update(self):
        # Pohyb nepřátel
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Odraz od stěn
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_y *= -1

# Skupiny sprite
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Okno s informacemi o autorovi
author_window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Informace o autorovi")

author_font = pygame.font.Font(None, 36)
author_text = author_font.render("Good luck!", True, WHITE)
info_text = author_font.render("Author: Benny; Press SPACE to continue...", True, WHITE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    author_window.fill(BLACK)
    author_window.blit(author_text, (50, 100))
    author_window.blit(info_text, (250, 300))

    pygame.display.flip()

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        break

# Vytvoření hráče
player = Player()
all_sprites.add(player)

# Vytvoření nepřátel
for _ in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Herní smyčka
running = True
start_time = pygame.time.get_ticks()  # Čas od spuštění hry v milisekundách
score = 0  # Skóre hráče

pause = False  # Proměnná pro stav pozastavení hry
pause_text = None  # Proměnná pro text pozastavení

while running:
    # Omezení FPS na 30
    clock.tick(30)

    # Zpracování událostí
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.lives > 0:
                if pause:
                    pause = False
                    pause_text = None
                else:
                    pause = True
                    pause_text = font.render("Game Paused. Press SPACE to continue.", True, WHITE)

    if not pause:
        # Aktualizace stavu hry
        all_sprites.update()

        # Detekce kolize hráče s nepřáteli
        if pygame.sprite.spritecollide(player, enemies, True):
            player.lives -= 1
            if player.lives <= 0:
                running = False
            else:
                pause = True
                pause_text = font.render("You lost a life. Press SPACE to continue.", True, WHITE)

        # Vykreslení obrazu
        window.fill(BLACK)
        all_sprites.draw(window)

        # Vykreslení životů
        font = pygame.font.Font(None, 30)
        lives_text = font.render("Lives: " + str(player.lives), True, WHITE)
        window.blit(lives_text, (10, 10))

        # Vykreslení stavové lišty s uplynulým časem
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000  # Převedení na sekundy
        time_text = font.render("Time: " + str(elapsed_time) + " s", True, WHITE)
        window.blit(time_text, (10, 40))

        # Aktualizace skóre každou sekundu
        if elapsed_time % 1 == 0:
            score += 10

        # Vykreslení skóre
        score_text = font.render("Score: " + str(score), True, WHITE)
        window.blit(score_text, (10, 70))

    if pause:
        # Vykreslení textu pozastavení
        window.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

    pygame.display.flip()

# Hláška "You lost!"
font = pygame.font.Font(None, 36)
lost_text = font.render("You lost!", True, WHITE)

# Vyčkání na stisk klávesy mezerník pro ukončení
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sys.exit()

    window.fill(BLACK)
    window.blit(lost_text, (WIDTH // 2 - lost_text.get_width() // 2, HEIGHT // 2 - lost_text.get_height() // 2))

    pygame.display.flip()


# Ukončení hry
pygame.quit()