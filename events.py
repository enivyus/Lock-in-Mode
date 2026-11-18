import pygame

# อีเวนต์ของเกมเรา (เลขต่ำกว่า USEREVENT pygame จองไว้ใช้เอง)
ENEMY_KILLED = pygame.USEREVENT + 1     # แนบข้อมูล: points
PLAYER_HIT = pygame.USEREVENT + 2       # แนบข้อมูล: damage