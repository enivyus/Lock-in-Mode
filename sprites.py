"""วาดรูปตัวละครทั้งหมดด้วยคำสั่งของ Pygame (ไม่ใช้ไฟล์รูป)

ทุกฟังก์ชัน make_... วาดลง Surface โปร่งใสแล้วคืนรูปนั้นออกไป
get_image() สร้างรูปครั้งแรกที่ถูกขอ แล้วเก็บไว้ใช้ซ้ำทุกเฟรม
"""
import os

import pygame
from settings import (PLAYER_COLOR, HOMEWORK_COLOR, QUIZ_COLOR, BOSS_COLOR,
                      COFFEE_COLOR, SLEEP_COLOR, BULLET_COLOR, ENEMY_BULLET_COLOR,
                      OUTLINE_COLOR, SKIN_COLOR, HAIR_COLOR, PAPER_COLOR)


def new_surface(width, height):
    return pygame.Surface((width, height), pygame.SRCALPHA)   # พื้นหลังโปร่งใส


def draw_text(surface, text, size, color, center):
    font = pygame.font.Font(None, size)
    image = font.render(text, True, color)
    surface.blit(image, image.get_rect(center=center))


def draw_paper(surface, rect, border_color, fill=PAPER_COLOR):
    """กระดาษพับมุมขวาบน ใช้ร่วมกันทั้งการบ้าน ควิซ และบอส"""
    x, y, w, h = rect
    fold = min(w, h) // 4
    outline = [(x, y), (x + w - fold, y), (x + w, y + fold), (x + w, y + h), (x, y + h)]
    pygame.draw.polygon(surface, fill, outline)
    pygame.draw.polygon(surface, border_color, outline, 2)
    corner = [(x + w - fold, y), (x + w - fold, y + fold), (x + w, y + fold)]
    pygame.draw.polygon(surface, border_color, corner)


def draw_face(surface, center, color, angry=False, scale=1):
    cx, cy = center
    eye_gap, eye_size = 6 * scale, 2 * scale
    pygame.draw.circle(surface, color, (cx - eye_gap, cy), eye_size)            # ตา
    pygame.draw.circle(surface, color, (cx + eye_gap, cy), eye_size)
    slope = (4 if angry else 2) * scale                                          # คิ้วขมวด
    brow_y = cy - 5 * scale
    pygame.draw.line(surface, color, (cx - 9 * scale, brow_y - slope), (cx - 3 * scale, brow_y), 2 * scale)
    pygame.draw.line(surface, color, (cx + 9 * scale, brow_y - slope), (cx + 3 * scale, brow_y), 2 * scale)
    mouth = (cx - 5 * scale, cy + 5 * scale, 10 * scale, 8 * scale)
    pygame.draw.arc(surface, color, mouth, 0.4, 2.74, 2 * scale)                 # ปากบึ้ง


def make_player():
    img = new_surface(40, 40)
    pygame.draw.rect(img, OUTLINE_COLOR, (5, 22, 30, 16), border_radius=6)        # เป้
    pygame.draw.rect(img, PLAYER_COLOR, (9, 20, 22, 20), border_radius=7)         # เสื้อ
    pygame.draw.circle(img, HAIR_COLOR, (20, 11), 10)                              # ผม
    pygame.draw.ellipse(img, SKIN_COLOR, (11, 6, 18, 15))                          # หน้า
    pygame.draw.circle(img, OUTLINE_COLOR, (16, 13), 2)                            # ตา
    pygame.draw.circle(img, OUTLINE_COLOR, (24, 13), 2)
    pygame.draw.arc(img, OUTLINE_COLOR, (16, 13, 8, 5), 3.5, 5.9, 1)               # ยิ้ม
    return img


def make_homework():
    img = new_surface(50, 36)
    draw_paper(img, (1, 1, 48, 34), HOMEWORK_COLOR)
    draw_text(img, "HW", 18, HOMEWORK_COLOR, (13, 10))
    for y in (18, 24, 30):
        pygame.draw.line(img, HOMEWORK_COLOR, (5, y), (20, y), 1)                  # บรรทัดตัวหนังสือ
    draw_face(img, (35, 18), OUTLINE_COLOR)
    return img


def make_quiz():
    img = new_surface(40, 40)
    draw_paper(img, (1, 1, 38, 38), QUIZ_COLOR)
    draw_text(img, "?", 46, QUIZ_COLOR, (19, 22))
    return img


def make_boss(angry=False):
    img = new_surface(160, 70)
    fill = (255, 225, 225) if angry else PAPER_COLOR                             # โกรธจนหน้าแดง
    draw_paper(img, (1, 1, 158, 68), BOSS_COLOR, fill)
    draw_text(img, "MIDTERM", 22, BOSS_COLOR, (42, 13))
    draw_face(img, (68, 38), BOSS_COLOR, angry=angry, scale=2)
    pygame.draw.circle(img, BOSS_COLOR, (128, 40), 20, 3)                          # วงกลมเกรด
    draw_text(img, "F", 40, BOSS_COLOR, (128, 42))
    return img


def make_coffee():
    img = new_surface(32, 32)
    for x in (11, 18):                                                             # ไอร้อน
        pygame.draw.arc(img, (170, 170, 180), (x - 3, 1, 6, 6), 1.6, 4.7, 2)
        pygame.draw.arc(img, (170, 170, 180), (x - 3, 6, 6, 6), -1.6, 1.6, 2)
    pygame.draw.circle(img, COFFEE_COLOR, (25, 21), 5, 2)                          # หูแก้ว
    pygame.draw.rect(img, COFFEE_COLOR, (5, 13, 20, 17), border_radius=4)          # แก้ว
    pygame.draw.rect(img, PAPER_COLOR, (8, 18, 14, 4), border_radius=2)            # ลายแก้ว
    return img


def make_sleep():
    img = new_surface(32, 32)
    pygame.draw.rect(img, SLEEP_COLOR, (2, 14, 28, 16), border_radius=8)           # หมอน
    pygame.draw.rect(img, PAPER_COLOR, (6, 18, 20, 3), border_radius=2)
    draw_text(img, "Z", 18, SLEEP_COLOR, (20, 7))
    draw_text(img, "z", 14, SLEEP_COLOR, (27, 3))
    return img


def make_pencil():
    img = new_surface(6, 14)
    pygame.draw.polygon(img, SKIN_COLOR, [(0, 4), (3, 0), (5, 4)])                 # ปลายไม้
    pygame.draw.line(img, OUTLINE_COLOR, (3, 0), (3, 1))                           # ไส้ดินสอ
    pygame.draw.rect(img, BULLET_COLOR, (0, 4, 6, 8))                              # ตัวดินสอ
    pygame.draw.rect(img, (240, 140, 160), (0, 12, 6, 2))                          # ยางลบ
    return img


def make_grade_f():
    """กระสุนบอส: ตัว F ในวงกลมแดง"""
    img = new_surface(26, 26)
    pygame.draw.circle(img, ENEMY_BULLET_COLOR, (13, 13), 12, 3)
    draw_text(img, "F", 24, ENEMY_BULLET_COLOR, (13, 14))
    return img


def make_grade_stamp(grade):
    """เกรดตอนจบเกม: ตัวอักษรในวงรีแดง เหมือนครูวงคะแนน"""
    img = new_surface(200, 160)
    pygame.draw.ellipse(img, BOSS_COLOR, (6, 6, 188, 148), 6)
    draw_text(img, grade, 110, BOSS_COLOR, (100, 84))
    return img


def make_red_pen():
    img = new_surface(10, 16)
    pygame.draw.rect(img, ENEMY_BULLET_COLOR, (2, 0, 6, 11), border_radius=2)     # ด้ามปากกา
    pygame.draw.polygon(img, ENEMY_BULLET_COLOR, [(2, 11), (8, 11), (5, 16)])     # ปลายปากกา
    pygame.draw.line(img, PAPER_COLOR, (4, 2), (4, 8), 1)                          # แสงสะท้อน
    return img


_MAKERS = {
    "player": make_player,
    "homework": make_homework,
    "quiz": make_quiz,
    "boss": make_boss,
    "boss_angry": lambda: make_boss(angry=True),
    "coffee": make_coffee,
    "sleep": make_sleep,
    "pencil": make_pencil,
    "red_pen": make_red_pen,
    "grade_f": make_grade_f,
}
GRADE_FILES = {"A": "a", "B+": "b_plus", "B": "b", "C+": "c_plus",
               "C": "c", "D+": "d_plus", "D": "d", "F": "f"}
for _grade, _key in GRADE_FILES.items():
    _MAKERS["result_" + _key] = (lambda g=_grade: make_grade_stamp(g))
# ขนาดสูงสุดของรูปวาดมือในเกม (กว้าง, สูง) ใกล้เคียง hitbox ของแต่ละตัว
DRAWING_SIZES = {
    "player": (60, 72),
    "homework": (64, 46),
    "quiz": (52, 50),
    "boss": (180, 92),
    "boss_angry": (180, 92),
    "coffee": (46, 46),
    "sleep": (48, 44),
    "pencil": (14, 36),
    "grade_f": (28, 28),
}
for _key in GRADE_FILES.values():
    DRAWING_SIZES["result_" + _key] = (200, 160)
ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
_cache = {}


def remove_white_background(image):
    """ทำพื้นขาวให้โปร่งใส (สำหรับรูปที่ไม่ได้บันทึกแบบพื้นโปร่งใส)"""
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            color = image.get_at((x, y))
            if min(color.r, color.g, color.b) >= 230:
                image.set_at((x, y), (255, 255, 255, 0))
    return image


def load_drawing(name):
    """โหลดรูปวาดมือจาก assets/<name>.png ถ้าไม่มีไฟล์หรือเปิดไม่ได้ คืน None"""
    path = os.path.join(ASSET_DIR, name + ".png")
    if name not in DRAWING_SIZES or not os.path.exists(path):
        return None
    try:
        image = pygame.image.load(path)
    except pygame.error:
        return None
    has_transparency = bool(image.get_flags() & pygame.SRCALPHA)    # ไฟล์บันทึกแบบพื้นโปร่งใสมาไหม
    max_w, max_h = DRAWING_SIZES[name]
    scale = min(max_w / image.get_width(), max_h / image.get_height())
    size = (max(1, round(image.get_width() * scale)), max(1, round(image.get_height() * scale)))
    image = pygame.transform.smoothscale(image.convert_alpha(), size)   # ย่อให้พอดีตัวละคร
    if not has_transparency:
        image = remove_white_background(image)
    return image


def grade_image_name(grade):
    """แปลงเกรด เช่น "B+" เป็นชื่อรูป "result_b_plus" """
    return "result_" + GRADE_FILES[grade]


def get_image(name):
    """ใช้รูปวาดมือถ้ามี ถ้าไม่มีใช้รูปที่วาดด้วยโค้ด สร้างครั้งแรกแล้วเก็บไว้ใช้ซ้ำ"""
    if name not in _cache:
        drawing = load_drawing(name)
        if drawing is None:
            drawing = _MAKERS[name]()
        _cache[name] = drawing
    return _cache[name]
