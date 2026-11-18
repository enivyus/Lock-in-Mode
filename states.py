import random
from abc import ABC, abstractmethod

import pygame
from settings import (WIDTH, HEIGHT, TEXT_COLOR, BULLET_COLOR, BOSS_COLOR,
                      HOMEWORK_COLOR, QUIZ_COLOR, COFFEE_COLOR, SLEEP_COLOR,
                      HP_GOOD_COLOR, HP_WARN_COLOR, HP_BAD_COLOR, BAR_BG_COLOR,
                      PAPER_LINE_COLOR, MARGIN_LINE_COLOR, PAUSE_OVERLAY_COLOR)
from entities import Player, Homework, Quiz, MidtermBoss, Coffee, Sleep
from events import ENEMY_KILLED, PLAYER_HIT
from observers import ScoreManager
import sprites


def draw_center(screen, font, text, color, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (WIDTH // 2 - surface.get_width() // 2, y))


class GameState(ABC):
    """แม่แบบของทุกหน้าจอ"""

    def __init__(self, game):
        self.game = game

    def enter(self):
        pass

    def exit(self):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass


class MenuState(GameState):
    """หน้าเมนู: SPACE เริ่มเกม, Q ออก"""

    SHOOT = [
        ("homework", "Homework  10 pts"),
        ("quiz", "Quiz  15 pts"),
        ("boss", "Midterm  200 pts"),
    ]
    COLLECT = [
        ("coffee", "Coffee  faster 5 s"),
        ("sleep", "Sleep  +30 HP"),
    ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.change_state(PlayState(self.game))
            elif event.key == pygame.K_q:
                self.game.quit()

    def update(self, dt):
        pass

    def draw(self, screen):
        draw_center(screen, self.game.big_font, "LOCK-IN MODE", TEXT_COLOR, 40)
        draw_center(screen, self.game.font, "Survive the semester", TEXT_COLOR, 130)

        self._draw_column(screen, "SHOOT these", BOSS_COLOR, self.SHOOT, 120)
        self._draw_column(screen, "COLLECT these", SLEEP_COLOR, self.COLLECT, 470)

        draw_center(screen, self.game.font, "A D / Arrows: move   SPACE: shoot   P: pause", TEXT_COLOR, 420)
        draw_center(screen, self.game.font, "Press SPACE to start", BULLET_COLOR, 480)
        draw_center(screen, self.game.font, "Q to quit", TEXT_COLOR, 520)

    def _draw_column(self, screen, title, color, items, x):
        screen.blit(self.game.font.render(title, True, color), (x, 190))
        y = 262
        for image_name, text in items:
            icon = sprites.get_image(image_name)
            scale = min(56 / icon.get_width(), 36 / icon.get_height(), 1)
            icon = pygame.transform.smoothscale(icon, (round(icon.get_width() * scale),
                                                       round(icon.get_height() * scale)))
            screen.blit(icon, icon.get_rect(midright=(x - 8, y)))          # ไอคอนอยู่ซ้ายของแนวหัวข้อ
            label = self.game.font.render(text, True, TEXT_COLOR)
            screen.blit(label, label.get_rect(midleft=(x, y)))             # ชื่อเริ่มตรงกับหัวข้อพอดี
            y += 48


class PlayState(GameState):
    """หน้าเล่นเกม"""

    def __init__(self, game):
        super().__init__(game)
        self._player = Player(WIDTH / 2 - 24, HEIGHT - 90)
        self._bullets = []
        self._enemies = []
        self._enemy_bullets = []
        self._powerups = []
        self._score_manager = ScoreManager()
        self._observers = [self._score_manager]       # เพิ่ม observer ใหม่ได้ด้วยการ append
        self._spawn_timer = 0.0
        self._boss_timer = 0.0
        self._powerup_timer = 0.0
        self._paper_scroll = 0.0
        self._elapsed = 0.0                           # เวลาที่เล่นมาแล้ว (วินาที)

    def enter(self):
        pygame.event.clear([ENEMY_KILLED, PLAYER_HIT])   # ล้างอีเวนต์ค้างจากรอบก่อน

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_ESCAPE):
            self.game.push_state(PauseState(self.game))
        for observer in self._observers:
            observer.handle_event(event)

    def _all_objects(self):
        return ([self._player] + self._bullets + self._enemies
                + self._enemy_bullets + self._powerups)

    @property
    def week(self):
        """ทุก 20 วินาที = 1 สัปดาห์ของเทอม ยิ่งสัปดาห์สูงยิ่งยาก"""
        return 1 + int(self._elapsed // 20)

    @property
    def spawn_interval(self):
        return max(0.3, 1.0 - 0.06 * (self.week - 1))       # ศัตรูเกิดถี่ขึ้นทุกสัปดาห์

    @property
    def boss_interval(self):
        return max(6.0, 15.0 - 0.75 * (self.week - 1))      # บอสมาบ่อยขึ้น

    def _spawn_enemy(self):
        enemy_class = random.choice([Homework, Homework, Quiz])
        self._enemies.append(enemy_class(random.randint(0, WIDTH - 50), -40))

    def _spawn(self, dt):
        self._spawn_timer += dt
        if self._spawn_timer >= self.spawn_interval:
            self._spawn_timer = 0.0
            self._spawn_enemy()
            double_chance = min(0.8, 0.05 * (self.week - 5))  # ตั้งแต่ Week 6 บางทีมาทีละ 2 ตัว
            if random.random() < double_chance:
                self._spawn_enemy()
        self._boss_timer += dt
        if self._boss_timer >= self.boss_interval:
            self._boss_timer = 0.0
            self._enemies.append(MidtermBoss(WIDTH / 2 - 80, -70, self._player))
        self._powerup_timer += dt
        if self._powerup_timer >= 8.0:
            self._powerup_timer = 0.0
            item_class = random.choice([Coffee, Sleep])
            self._powerups.append(item_class(random.randint(0, WIDTH - 28), -28))

    def _check_collisions(self):
        for bullet in self._bullets:
            for enemy in self._enemies:
                if bullet.active and enemy.active and bullet.rect.colliderect(enemy.rect):
                    bullet.kill()
                    enemy.take_hit(1)
                    if not enemy.active:
                        pygame.event.post(pygame.event.Event(ENEMY_KILLED, {"points": enemy.points}))
        for enemy in self._enemies:
            if enemy.active and enemy.rect.colliderect(self._player.rect):
                enemy.kill()
                if self._player.hit(20):
                    pygame.event.post(pygame.event.Event(PLAYER_HIT, {"damage": 20}))
        for shot in self._enemy_bullets:
            if shot.active and shot.rect.colliderect(self._player.rect):
                shot.kill()
                if self._player.hit(10):
                    pygame.event.post(pygame.event.Event(PLAYER_HIT, {"damage": 10}))
        for item in self._powerups:
            if item.active and item.rect.colliderect(self._player.rect):
                item.apply(self._player)              # polymorphism: ไม่ต้องรู้ว่าเป็นกาแฟหรือการนอน
                item.kill()

    def update(self, dt):
        self._elapsed += dt
        self._paper_scroll = (self._paper_scroll + 40 * dt) % 40
        self._spawn(dt)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            bullet = self._player.try_shoot()
            if bullet is not None:
                self._bullets.append(bullet)

        for enemy in self._enemies:
            shot = enemy.try_shoot()                  # มีแค่บอสที่คืนกระสุน ตัวอื่นคืน None
            if shot is not None:
                self._enemy_bullets.append(shot)

        for obj in self._all_objects():
            obj.update(dt)

        self._check_collisions()

        self._bullets = [b for b in self._bullets if b.active]
        self._enemies = [e for e in self._enemies if e.active]
        self._enemy_bullets = [s for s in self._enemy_bullets if s.active]
        self._powerups = [p for p in self._powerups if p.active]

        if not self._player.health.is_alive:
            sm = self._score_manager
            self.game.change_state(GameOverState(self.game, sm.score, sm.grade))

    def _draw_paper(self, screen):
        y = self._paper_scroll
        while y < HEIGHT:
            pygame.draw.line(screen, PAPER_LINE_COLOR, (0, round(y)), (WIDTH, round(y)))
            y += 40
        pygame.draw.line(screen, MARGIN_LINE_COLOR, (60, 0), (60, HEIGHT), 2)

    def _draw_hud(self, screen):
        health = self._player.health
        ratio = health.hp / health.max_hp
        if ratio > 0.5:
            color = HP_GOOD_COLOR
        elif ratio > 0.25:
            color = HP_WARN_COLOR
        else:
            color = HP_BAD_COLOR
        font = self.game.font
        bar = pygame.Rect(118, 20, 200, 20)                       # อยู่ขวาของเส้นขอบกระดาษ
        label = font.render("HP", True, TEXT_COLOR)
        screen.blit(label, label.get_rect(midright=(bar.left - 10, bar.centery)))
        pygame.draw.rect(screen, BAR_BG_COLOR, bar, border_radius=4)
        pygame.draw.rect(screen, color, (bar.left, bar.top, round(bar.width * ratio), bar.height), border_radius=4)
        score = font.render(f"Score: {self._score_manager.score}", True, TEXT_COLOR)
        screen.blit(score, score.get_rect(midright=(WIDTH - 20, bar.centery)))

    def draw(self, screen):
        self._draw_paper(screen)
        for obj in self._all_objects():
            obj.draw(screen)
        self._draw_hud(screen)

class PauseState(GameState):
    """หน้าหยุดเกม: วางทับ PlayState ที่ถูกแช่แข็งไว้"""

    def __init__(self, game):
        super().__init__(game)
        self._overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self._overlay.fill(PAUSE_OVERLAY_COLOR)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_ESCAPE):
            self.game.pop_state()          # เอา Pause ออก → กลับไปเล่นต่อ

    def update(self, dt):
        pass                               # ว่างไว้ = เกมด้านล่างหยุดนิ่ง

    def draw(self, screen):
        screen.blit(self._overlay, (0, 0))
        draw_center(screen, self.game.big_font, "PAUSED", TEXT_COLOR, 240)
        draw_center(screen, self.game.font, "P or ESC to resume", TEXT_COLOR, 320)


class GameOverState(GameState):
    """หน้าจบเกม: R เล่นใหม่, M กลับเมนู"""

    def __init__(self, game, final_score, grade):
        super().__init__(game)
        self._final_score = final_score
        self._grade = grade

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.game.change_state(PlayState(self.game))
            elif event.key in (pygame.K_m, pygame.K_ESCAPE):
                self.game.change_state(MenuState(self.game))

    def update(self, dt):
        pass

    def draw(self, screen):
        draw_center(screen, self.game.big_font, "GAME OVER", BOSS_COLOR, 60)
        draw_center(screen, self.game.font, f"Score: {self._final_score}", TEXT_COLOR, 150)
        draw_center(screen, self.game.font, "Your grade", TEXT_COLOR, 198)
        stamp = sprites.get_image(sprites.grade_image_name(self._grade))
        screen.blit(stamp, stamp.get_rect(center=(WIDTH // 2, 340)))
        draw_center(screen, self.game.font, "R to restart  |  M for menu", TEXT_COLOR, 480)