import os

import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE, BG_COLOR


FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "fonts")


def load_font(filename, size):
    """โหลดฟอนต์ doodle จาก assets/fonts ถ้าไม่เจอไฟล์ใช้ฟอนต์เริ่มต้นของ pygame"""
    path = os.path.join(FONT_DIR, filename)
    if os.path.exists(path):
        return pygame.font.Font(path, size)
    return pygame.font.Font(None, size)


class Game:
    """เจ้าของหน้าต่างและ state stack ส่งต่องานให้ state บนสุด"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = load_font("IndieFlower-Regular.ttf", 32)          # ข้อความทั่วไป ลายมือ
        self.big_font = load_font("Gaegu-Bold.ttf", 84)              # หัวข้อใหญ่ ลายมือเด็ก
        self.running = True
        self.state_stack = []

    def change_state(self, new_state):
        if self.state_stack:
            self.state_stack.pop().exit()
        self.state_stack.append(new_state)
        new_state.enter()

    def push_state(self, new_state):
        self.state_stack.append(new_state)
        new_state.enter()

    def pop_state(self):
        if not self.state_stack:
            return None
        popped = self.state_stack.pop()
        popped.exit()
        return popped

    def quit(self):
        self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if self.state_stack:
                self.state_stack[-1].handle_event(event)    # รับอินพุตเฉพาะ state บนสุด

    def update(self, dt):
        if self.state_stack:
            self.state_stack[-1].update(dt)                 # อัปเดตเฉพาะ state บนสุด

    def draw(self):
        self.screen.fill(BG_COLOR)
        for state in self.state_stack:                      # วาดทุกชั้น (Play แล้วทับด้วย Pause)
            state.draw(self.screen)
        pygame.display.flip()

    def run(self, start_state):
        self.change_state(start_state)
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()