import pygame
import random
import time
import math
import os

pygame.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geo-Racer Matrix - Advanced Edition")
clock = pygame.time.Clock()

BG_COLOR = (30, 39, 46)
ROAD_COLOR = (44, 62, 80)
LINE_COLOR = (255, 255, 255)
PLAYER_COLOR = (56, 189, 248)
ENEMY_COLOR = (239, 68, 68)
TEXT_COLOR = (16, 185, 129)
COIN_COLOR = (253, 224, 71)
SHIELD_COLOR = (168, 85, 247)

font_large = pygame.font.SysFont("Courier New", 42, bold=True)
font_small = pygame.font.SysFont("Arial", 20, bold=True)

def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            try:
                return float(file.read())
            except:
                return 0.0
    return 0.0

def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(f"{score:.2f}")

high_score = load_high_score()

def draw_car(surface, x, y, color):
    pygame.draw.rect(surface, color, (x, y, 40, 70), border_radius=8)
    pygame.draw.rect(surface, (15, 23, 42), (x + 5, y + 15, 30, 40), border_radius=4)
    pygame.draw.circle(surface, (253, 224, 71), (x + 10, y + 5), 4)
    pygame.draw.circle(surface, (253, 224, 71), (x + 30, y + 5), 4)

class Player:
    def __init__(self):
        self.width = 40
        self.height = 70
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 120
        self.speed = 8
        self.shield_active = False
        self.shield_timer = 0

    def move(self, keys):
        if pygame.mouse.get_pressed()[0]: 
            mouse_x = pygame.mouse.get_pos()[0]
            target_x = mouse_x - (self.width // 2)
            self.x += (target_x - self.x) * 0.15 
            
        
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            
        
        if self.x < 100:
            self.x = 100
        elif self.x > WIDTH - 100 - self.width:
            self.x = WIDTH - 100 - self.width

        
        if self.shield_active and time.time() > self.shield_timer:
            self.shield_active = False

    def draw(self, surface):
        draw_car(surface, self.x, self.y, PLAYER_COLOR)
        if self.shield_active:
            
            pygame.draw.circle(surface, SHIELD_COLOR, (int(self.x + 20), int(self.y + 35)), 55, 3)
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Enemy:
    def __init__(self, speed_multiplier=1.0):
        self.width = 40
        self.height = 70
        self.x = random.choice([130, 230, 330, 430])
        self.y = random.randint(-400, -100)
        self.base_speed = random.uniform(5.0, 8.0)
        self.dy = self.base_speed * speed_multiplier

    def move(self, speed_multiplier):
        self.dy = self.base_speed * speed_multiplier
        self.y += self.dy
        if self.y > HEIGHT:
            self.y = random.randint(-400, -100)
            self.x = random.choice([130, 230, 330, 430])

    def draw(self, surface):
        draw_car(surface, self.x, self.y, ENEMY_COLOR)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Collectible:
    def __init__(self, c_type):
        self.type = c_type 
        self.radius = 15
        self.x = random.choice([150, 250, 350, 450])
        self.y = random.randint(-800, -200)
        self.dy = 5.0

    def move(self, speed_multiplier):
        self.y += self.dy * speed_multiplier
        if self.y > HEIGHT:
            self.y = random.randint(-1500, -500)
            self.x = random.choice([150, 250, 350, 450])
            self.type = random.choices(['coin', 'shield'], weights=[80, 20])[0]

    def draw(self, surface):
        color = COIN_COLOR if self.type == 'coin' else SHIELD_COLOR
        pygame.draw.circle(surface, color, (self.x, int(self.y)), self.radius)
        # Inner detail
        pygame.draw.circle(surface, (255, 255, 255), (self.x, int(self.y)), self.radius - 4, 1)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(-4, 4)
        self.dy = random.uniform(-4, 4)
        self.radius = random.randint(3, 8)
        self.life = 30 

    def move_and_draw(self, surface):
        self.x += self.dx
        self.y += self.dy
        self.radius = max(0, self.radius - 0.2)
        self.life -= 1
        pygame.draw.circle(surface, (255, random.randint(100, 200), 0), (int(self.x), int(self.y)), int(self.radius))

player = Player()
enemies = []
collectibles = []
particles = []
line_offset = 0
game_state = "START"
start_time = 0
time_bonus = 0
speed_multiplier = 1.0

running = True
while running:
    screen.fill(BG_COLOR)
    
    pygame.draw.rect(screen, (20, 28, 35), (0, 0, 100, HEIGHT))
    pygame.draw.rect(screen, (20, 28, 35), (500, 0, 100, HEIGHT))
    
    pygame.draw.rect(screen, ROAD_COLOR, (100, 0, 400, HEIGHT))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "START" or game_state == "GAMEOVER":
                game_state = "PLAYING"
                player = Player()
                speed_multiplier = 1.0
                enemies = [Enemy(speed_multiplier) for _ in range(4)]
                collectibles = [Collectible('coin'), Collectible('shield')]
                particles = []
                start_time = time.time()
                time_bonus = 0

    if game_state == "START":
        title = font_large.render("GEO-RACER MATRIX", True, PLAYER_COLOR)
        prompt = font_small.render("USE ARROWS OR MOUSE. CLICK TO START", True, LINE_COLOR)
        hs_text = font_small.render(f"HIGH SCORE: {high_score:.2f} SEC", True, COIN_COLOR)
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2))
        screen.blit(hs_text, (WIDTH//2 - hs_text.get_width()//2, HEIGHT//2 + 40))
        
    elif game_state == "PLAYING":
        
        elapsed_actual = time.time() - start_time
        speed_multiplier = 1.0 + (elapsed_actual * 0.02) 
        
       
        line_offset = (line_offset + 5 * speed_multiplier) % 40
        for y in range(-40, HEIGHT, 40):
            pygame.draw.rect(screen, LINE_COLOR, (WIDTH//2 - 5, y + line_offset, 10, 20))
            
       
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.draw(screen)
        
       
        for item in collectibles:
            item.move(speed_multiplier)
            item.draw(screen)
            
          
            if player.get_rect().colliderect(item.get_rect()):
                if item.type == 'coin':
                    time_bonus += 3.0 
                elif item.type == 'shield':
                    player.shield_active = True
                    player.shield_timer = time.time() + 5.0 
                
               
                item.y = random.randint(-1500, -500)
                item.x = random.choice([150, 250, 350, 450])
        
       
        for enemy in enemies:
            enemy.move(speed_multiplier)
            enemy.draw(screen)
            
           
            if player.get_rect().colliderect(enemy.get_rect()):
                if player.shield_active:
                    
                    enemy.y = random.randint(-400, -100)
                else:
                   
                    game_state = "GAMEOVER"
                    
                   
                    for _ in range(30):
                        particles.append(Particle(player.x + 20, player.y + 35))
                        
                    
                    final_score = elapsed_actual + time_bonus
                    if final_score > high_score:
                        high_score = final_score
                        save_high_score(high_score)

       
        total_score = elapsed_actual + time_bonus
        score_str = f"SCORE: {total_score:05.2f}"
        score_surface = font_small.render(score_str, True, TEXT_COLOR)
        screen.blit(score_surface, (10, 10))
        
        if player.shield_active:
            shield_text = font_small.render("SHIELD ACTIVE!", True, SHIELD_COLOR)
            screen.blit(shield_text, (WIDTH - 160, 10))
        
    elif game_state == "GAMEOVER":
        
        for p in particles[:]:
            p.move_and_draw(screen)
            if p.life <= 0:
                particles.remove(p)
                
        end_title = font_large.render("CRASH!", True, ENEMY_COLOR)
        score_text = font_small.render(f"FINAL SCORE: {total_score:.2f}", True, LINE_COLOR)
        hs_text = font_small.render(f"HIGH SCORE: {high_score:.2f}", True, COIN_COLOR)
        restart_prompt = font_small.render("CLICK TO RESTART", True, TEXT_COLOR)
        
        screen.blit(end_title, (WIDTH//2 - end_title.get_width()//2, HEIGHT//3))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 20))
        screen.blit(hs_text, (WIDTH//2 - hs_text.get_width()//2, HEIGHT//2 + 10))
        screen.blit(restart_prompt, (WIDTH//2 - restart_prompt.get_width()//2, HEIGHT//2 + 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
