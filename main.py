import pygame, sys, math, random

pygame.init()
WIDTH, HEIGHT = 960, 540
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practica 4- fondos y animaciones")
CLOCK = pygame.time.Clock()
FPS = 60

def make_text(txt, size=20, color=(230,230,240)):
    return pygame.font.SysFont(None, size).render(txt, True, color)

def clamp(v, a, b):
    return max(a, min(v, b))

# -------- Capas parallax --------
class StarLayer:
    def __init__(self, w, h, density=0.0008, speed=0.4):
        self.w, self.h = w, h
        self.speed = speed
        self.offset =0.0
        self.surf= pygame.Surface((w*2, h), pygame.SRCALPHA)
        self.surf.fill((0,0,0,0))
        count= int(w*h*density)
        for _ in range(count):
            x = random.randint(0, w*2-1)
            y = random.randint(0, h-1)
            c = random.randint(180,255)
            self.surf.set_at((x,y), (c,c,c,255))
           
    def update(self, dt_ms):
        self.offset = (self.offset + self.speed * dt_ms/16) % self.w
       
    def draw(self, screen):
        x = int(self.offset)
        screen.blit(self.surf, (-x,0))
        screen.blit(self.surf, (-x + self.w,0))
       
class HillsLayer:
    def __init__(self, w, h, color=(40,80,60), base=420, amp=28, freq=0.012, speed=1.0):
        self.w, self.h = w, h
        self.color = color
        self.base = base
        self.amp = amp
        self.freq = freq
        self.speed = speed
        self.offset = 0.0
        self.surf = pygame.Surface((w*2,h), pygame.SRCALPHA)
        self._render()
       
    def _render(self):
        self.surf.fill((0,0,0,0))
        for x in range(self.w*2):
            y = int(self.base + math.sin(x*self.freq) * self.amp)
            pygame.draw.line(self.surf, self.color, (x,y), (x,self.h))
        overlay = pygame.Surface((self.w*2, self.h), pygame.SRCALPHA)
        overlay.fill((*self.color,30))
        self.surf.blit(overlay,(0,0))

    def update(self, dt_ms):
        self.offset = (self.offset + self.speed * dt_ms) % self.w
       
    def draw(self, screen):
        x = int(self.offset)
        screen.blit(self.surf, (-x,0))
        screen.blit(self.surf, (-x + self.w,0))

class CloudLayer:
    def __init__(self, w,h, speed=1.8, count=10):
        self.w, self.h = w,h
        self.speed = speed
        self.offset = 0.0
        self.surf = pygame.Surface((w*2,h), pygame.SRCALPHA)
        for _ in range(count):
            cx = random.randint(0, w*2-1)
            cy = random.randint(40, h//2)
            r = random.randint(20,60)
            cloud = pygame.Surface((r*4, r*2), pygame.SRCALPHA)
            for i in range(6):
                pygame.draw.circle(cloud, (255,255,255,60), 
                                   (random.randint(r,3*r), random.randint(r//2,r)), 
                                   random.randint(r//2,r))
            self.surf.blit(cloud,(cx,cy))

    def update(self, dt_ms):
        self.offset = (self.offset + self.speed * dt_ms) % self.w
        
    def draw(self,screen):
        x = int(self.offset)
        screen.blit(self.surf, (-x,0))
        screen.blit(self.surf, (-x + self.w,0))

# -------- Sprites --------
def make_idle_frames(size=(48,48)):
    w,h = size
    frames = []
    for i in range(6):
        surf = pygame.Surface((w,h), pygame.SRCALPHA)
        pygame.draw.rect(surf, (240,220,90),(8,12,w-16,h-20), border_radius=10)
        dy = int(math.sin(i/6*math.tau)*2)
        pygame.draw.circle(surf,(30,30,30),(w//2-6,18+dy),4)
        pygame.draw.circle(surf,(30,30,30),(w//2+6,18+dy),4)
        pygame.draw.rect(surf,(30,30,30),(w//2-8,26+dy,16,3), border_radius=2)
        frames.append(surf)
    return frames

def make_run_frames(size=(48,48)):
    w,h = size
    frames = []
    for i in range(8):
        surf = pygame.Surface((w,h), pygame.SRCALPHA)
        pygame.draw.rect(surf,(240,120,90),(8,8,w-16,h-16), border_radius=10)
        phase = i/8*math.tau
        arm = int(math.sin(phase)*6)
        leg = int(math.cos(phase)*6)
        pygame.draw.rect(surf,(60,60,60),(4,18+arm,10,6), border_radius=3)
        pygame.draw.rect(surf,(60,60,60),(w-14,18-arm,10,6), border_radius=3)
        pygame.draw.rect(surf,(40,40,40),(12,h-14+leg,10,6), border_radius=2)
        pygame.draw.rect(surf,(40,40,40),(w-22,h-14-leg,10,6), border_radius=2)
        pygame.draw.circle(surf,(30,30,30),(w//2-6,18),4)
        pygame.draw.circle(surf,(30,30,30),(w//2+6,18),4)
        frames.append(surf)
    return frames

class AnimSprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frames_idle = make_idle_frames()
        self.frames_run = make_run_frames()
        self.frames = self.frames_idle
        self.frame_index = 0
        self.frame_time = 0.0
        self.frame_duration = 0.08
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.vel = pygame.Vector2(0,0)
        self.accel = 0.7
        self.friction = 0.86
        self.max_speed = 6.5
        self.facing_left = False
           
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x -= self.accel
            self.facing_left = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x += self.accel
            self.facing_left = False

    def apply_physics(self):
        self.vel.x = clamp(self.vel.x, -self.max_speed, self.max_speed)
        self.vel *= self.friction
        self.rect.x += int(self.vel.x)
        if self.rect.left < 0:
            self.rect.left = 0; self.vel.x = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH; self.vel.x = 0

    def choose_animation(self):
        moving = abs(self.vel.x) > 0.2
        target = self.frames_run if moving else self.frames_idle
        if target is not self.frames:
            self.frames = target
            self.frame_index = 0
            self.frame_time = 0.0
            self.frame_duration = 0.06 if target is self.frames_run else 0.10

    def animate(self, dt):
        self.frame_time += dt
        if self.frame_time >= self.frame_duration:
            self.frame_time = 0.0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        frame = self.frames[self.frame_index]
        self.image = pygame.transform.flip(frame, True, False) if self.facing_left else frame

    def update(self, dt):
        self.handle_input()
        self.apply_physics()
        self.choose_animation()
        self.animate(dt)

# -------- Fondo degradado con ciclo dia/noche --------
class DayNightCycle:
    def __init__(self):
        self.time = 0.0  # segundos
        self.cycle_length = 20.0  # duración de un día/noche en segundos

        # Colores de ejemplo: día azul claro → noche azul oscuro
        self.top_day = (135, 206, 250)
        self.bottom_day = (255, 220, 180)
        self.top_night = (10,12,22)
        self.bottom_night = (25,28,48)

    def update(self, dt):
        self.time = (self.time + dt) % self.cycle_length

    def get_colors(self):
        # interpolación suave entre día y noche usando seno
        t = math.sin((self.time/self.cycle_length) * math.tau) * 0.5 + 0.5
        top = tuple(int(self.top_day[i]*(1-t) + self.top_night[i]*t) for i in range(3))
        bottom = tuple(int(self.bottom_day[i]*(1-t) + self.bottom_night[i]*t) for i in range(3))
        return top, bottom

def draw_gradient_bg(screen, top, bottom):
    for y in range(HEIGHT):
        t = y/HEIGHT
        r = int(top[0]*(1-t) + bottom[0]*t)
        g = int(top[1]*(1-t) + bottom[1]*t)
        b = int(top[2]*(1-t) + bottom[2]*t)
        pygame.draw.line(screen,(r,g,b),(0,y),(WIDTH,y))

# -------- Main --------
def main():
    stars_far = StarLayer(WIDTH, HEIGHT, density=0.0010, speed=0.25)
    clouds = CloudLayer(WIDTH, HEIGHT, speed=1.2, count=10)
    hills = HillsLayer(WIDTH, HEIGHT, color=(35,90,70), base=400, amp=36, freq=0.010, speed=2.0)
    player = AnimSprite((WIDTH//2, 360))
    group = pygame.sprite.Group(player)

    daynight = DayNightCycle()
    
    running = True
    while running:
        dt_ms = CLOCK.tick(FPS)
        dt = dt_ms/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # actualizar parallax
        stars_far.update(dt_ms)
        clouds.update(dt_ms)
        hills.update(dt_ms)
        group.update(dt)

        # actualizar ciclo día/noche
        daynight.update(dt)
        top_color, bottom_color = daynight.get_colors()

        # dibujar fondo
        draw_gradient_bg(WINDOW, top_color, bottom_color)
        stars_far.draw(WINDOW)
        clouds.draw(WINDOW)
        hills.draw(WINDOW)
        group.draw(WINDOW)
        
        # HUD
        hud = [
            "Practica 4 - Fondos y Animaciones",
            f"FPS: {int(CLOCK.get_fps())} / frame: {player.frame_index} / anim: {'run' if player.frames is player.frames_run else 'idle'}",
            "Izq/Der o A/D para mover / Esc para salir",
            "Ciclo dia/noche activo."
        ]
        for i, line in enumerate(hud):
            WINDOW.blit(make_text(line,20), (10, 10 + i*20))
            
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()
