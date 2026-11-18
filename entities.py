import math
from abc import ABC, abstractmethod

import pygame
from settings import (WIDTH, HEIGHT, PLAYER_COLOR, BULLET_COLOR,HOMEWORK_COLOR, QUIZ_COLOR, BOSS_COLOR,COFFEE_COLOR, SLEEP_COLOR, ENEMY_BULLET_COLOR,
                      BAR_BG_COLOR)
from components import Health, Weapon
import sprites


class GameObject(ABC):
    

    def __init__(self, x, y, width, height):
        self._x = float(x)
        self._y = float(y)
        self._width = width
        self._height = height
        self._active = True

    @property
    def active(self):
        return self._active

    @property
    def rect(self):
        return pygame.Rect(round(self._x), round(self._y), self._width, self._height)

    def kill(self):
        self._active = False

    def blit_image(self, screen, image):
        """แปะรูปให้กึ่งกลางตรงกับ hitbox (rect)"""
        screen.blit(image, image.get_rect(center=self.rect.center))

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass


class Bullet(GameObject):
    

    def __init__(self, x, y, speed=600.0):
        super().__init__(x, y, 10, 30)
        self._speed = speed

    def update(self, dt):
        self._y -= self._speed * dt
        if self._y + self._height < 0:
            self.kill()

    def draw(self, screen):
        self.blit_image(screen, sprites.get_image("pencil"))


class EnemyBullet(GameObject):
    """กระสุนของบอส: พุ่งลงด้านล่าง"""

    def __init__(self, x, y, speed=300.0):
        super().__init__(x, y, 22, 22)
        self._speed = speed

    def update(self, dt):
        self._y += self._speed * dt
        if self._y > HEIGHT:
            self.kill()

    def draw(self, screen):
        self.blit_image(screen, sprites.get_image("grade_f"))


class Player(GameObject):
    """นักศึกษาที่ผู้เล่นควบคุม"""

    def __init__(self, x, y, speed=300.0):
        super().__init__(x, y, 48, 58)
        self.speed = speed
        self._base_speed = self._speed
        self._boost_timer = 0.0
        self._invincible_timer = 0.0
        self._health = Health(100)
        self._weapon = Weapon(cooldown=0.25)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if not (100 <= value <= 600):
            raise ValueError("speed must be between 100 and 600")
        self._speed = float(value)

    @property
    def health(self):
        return self._health

    @property
    def center_x(self):
        return self._x + self._width / 2

    @property
    def is_boosted(self):
        return self._boost_timer > 0

    @property
    def is_invincible(self):
        return self._invincible_timer > 0

    def hit(self, damage):
        """รับความเสียหาย คืน True ถ้าโดนจริง (ไม่โดนซ้ำระหว่างอมตะชั่วคราว 1 วินาที)"""
        if self.is_invincible:
            return False
        self._health.take_damage(damage)
        self._invincible_timer = 1.0
        return True

    def boost_speed(self, multiplier, duration):
        self.speed = self._base_speed * multiplier     # ผ่าน setter → ตรวจช่วง 100–600
        self._boost_timer = duration

    def update(self, dt):
        keys = pygame.key.get_pressed()
        dx = 0                                         # เดินได้แค่ซ้าย-ขวา
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -1

        self._x += dx * self._speed * dt
        self._x = max(0, min(self._x, WIDTH - self._width))

        self._weapon.update(dt)
        self._invincible_timer = max(0.0, self._invincible_timer - dt)

        if self._boost_timer > 0:
            self._boost_timer -= dt
            if self._boost_timer <= 0:
                self.speed = self._base_speed          # หมดฤทธิ์กาแฟ กลับความเร็วปกติ

    def try_shoot(self):
        if not self._weapon.try_fire():
            return None
        return Bullet(self.center_x - 5, self._y - 10)

    def draw(self, screen):
        if self.is_invincible and int(self._invincible_timer * 10) % 2 == 0:
            return                                     # กะพริบ: เว้นวาดบางเฟรมระหว่างอมตะ
        self.blit_image(screen, sprites.get_image("player"))
        if self.is_boosted:                            # เส้นความเร็วตอนกินกาแฟ
            for dx in (-10, 0, 10):
                x = self.rect.centerx + dx
                pygame.draw.line(screen, COFFEE_COLOR, (x, self.rect.bottom + 3), (x, self.rect.bottom + 11), 2)


class Enemy(GameObject):
    IMAGE = "homework"                     # คลาสลูกเลือกรูปของตัวเอง
    

    def __init__(self, x, y, width, height, color, speed, hp, points):
        super().__init__(x, y, width, height)
        self._color = color
        self._speed = speed
        self._health = Health(hp)
        self._points = points

    @property
    def points(self):
        return self._points

    def try_shoot(self):
        return None                    # ศัตรูทั่วไปไม่ยิง

    def take_hit(self, damage=1):
        self._health.take_damage(damage)
        if not self._health.is_alive:
            self.kill()

    def update(self, dt):
        if self._y > HEIGHT:
            self.kill()

    def image_name(self):
        return self.IMAGE

    def draw(self, screen):
        self.blit_image(screen, sprites.get_image(self.image_name()))


class Homework(Enemy):
    IMAGE = "homework"
    

    def __init__(self, x, y):
        super().__init__(x, y, 50, 36, HOMEWORK_COLOR, speed=120, hp=1, points=10)

    def update(self, dt):
        self._y += self._speed * dt
        super().update(dt)


class Quiz(Enemy):
    IMAGE = "quiz"
    

    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, QUIZ_COLOR, speed=160, hp=1, points=15)
        self._time = 0.0

    def update(self, dt):
        self._time += dt
        self._y += self._speed * dt
        self._x += math.sin(self._time * 5) * 200 * dt
        self._x = max(0, min(self._x, WIDTH - self._width))
        super().update(dt)


class MidtermBoss(Enemy):
    IMAGE = "boss"
    

    def __init__(self, x, y, target):
        super().__init__(x, y, 160, 70, BOSS_COLOR, speed=90, hp=20, points=200)
        self._target = target
        self._weapon = Weapon(cooldown=1.2)

    def update(self, dt):
        if self._y < 60:
            self._y += self._speed * dt
        my_center = self._x + self._width / 2
        if self._target.center_x > my_center + 5:
            self._x += self._speed * dt
        elif self._target.center_x < my_center - 5:
            self._x -= self._speed * dt
        self._weapon.update(dt)
        super().update(dt)

    def image_name(self):
        if self._health.hp < self._health.max_hp / 2:
            return "boss_angry"                # เลือดต่ำกว่าครึ่ง เปลี่ยนเป็นหน้าโกรธจัด
        return self.IMAGE

    def draw(self, screen):
        super().draw(screen)
        image_top = self.rect.centery - sprites.get_image(self.image_name()).get_height() // 2
        bar = pygame.Rect(self.rect.left, image_top - 10, self.rect.width, 6)     # เหนือรูปบอส
        ratio = self._health.hp / self._health.max_hp
        pygame.draw.rect(screen, BAR_BG_COLOR, bar)
        pygame.draw.rect(screen, BOSS_COLOR, (bar.left, bar.top, round(bar.width * ratio), bar.height))

    def try_shoot(self):
        if self._y < 60 or not self._weapon.try_fire():
            return None                # ยังลงมาไม่ถึงตำแหน่ง หรือยังคูลดาวน์
        return EnemyBullet(self._x + self._width / 2 - 11, self._y + self._height)
        
class PowerUp(GameObject):
    """ไอเทมที่ตกลงมาให้เก็บ: คลาสลูกต้องกำหนดว่าเก็บแล้วเกิดอะไรใน apply()"""
    IMAGE = ""                             # คลาสลูกเลือกรูปของตัวเอง

    def __init__(self, x, y, color):
        super().__init__(x, y, 28, 28)
        self._color = color
        self._speed = 140

    def update(self, dt):
        self._y += self._speed * dt
        if self._y > HEIGHT:
            self.kill()

    def draw(self, screen):
        self.blit_image(screen, sprites.get_image(self.IMAGE))

    @abstractmethod
    def apply(self, player):
        pass


class Coffee(PowerUp):
    """กาแฟ: เดินเร็วขึ้น 1.5 เท่า นาน 5 วินาที"""
    IMAGE = "coffee"

    def __init__(self, x, y):
        super().__init__(x, y, COFFEE_COLOR)

    def apply(self, player):
        player.boost_speed(1.5, 5.0)


class Sleep(PowerUp):
    """การนอน: ฟื้นพลังชีวิต 30"""
    IMAGE = "sleep"

    def __init__(self, x, y):
        super().__init__(x, y, SLEEP_COLOR)

    def apply(self, player):
        player.health.heal(30)