# 🎓 Lock-in Mode

เกมยิงแนวตั้ง 2D สร้างด้วย Pygame-ce 

ผู้เล่นคือนักศึกษาที่ต้อง "lock in" ยิงงานที่พุ่งเข้ามาก่อนจะชนตัวเอง ตั้งแต่การบ้าน ควิซ ไปจนถึงบอสมิดเทอม เก็บกาแฟและการนอนเพื่อเอาตัวรอด แล้วดูว่าจบเกมได้เกรดอะไร

## ⚙️ ความต้องการของระบบ

- Python 3.12 ขึ้นไป
- pygame-ce

## 🚀 การติดตั้งและรันเกม

```bash
# 1. สร้างและเปิดใช้ virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 2. ติดตั้ง pygame-ce
python -m pip install --upgrade pip
python -m pip install pygame-ce

# 3. รันเกม
python main.py
```

## 🎮 การควบคุม

| หน้าจอ | ปุ่ม | การทำงาน |
|---|---|---|
| เมนู | `SPACE` | เริ่มเกม |
| เมนู | `Q` | ออกจากเกม |
| ระหว่างเล่น | `A` `D` หรือ ลูกศรซ้าย-ขวา | เดินซ้าย-ขวา |
| ระหว่างเล่น | `SPACE` (กดค้างได้) | ยิง (คูลดาวน์ 0.25 วินาที) |
| ระหว่างเล่น | `P` หรือ `ESC` | หยุดเกมชั่วคราว |
| หยุดเกม | `P` หรือ `ESC` | เล่นต่อ |
| จบเกม | `R` | เริ่มเล่นใหม่ |
| จบเกม | `M` หรือ `ESC` | กลับเมนู |

## 🕹️ วิธีเล่น

ผู้เล่นเริ่มด้วยพลังชีวิต 100 เดินได้เฉพาะซ้าย-ขวาที่ด้านล่างของจอ ศัตรูที่ชนตัวผู้เล่นทำให้เสียพลังชีวิต 20 และหายไป

**ความยากเพิ่มขึ้นตามเวลา:** ทุก 20 วินาทีนับเป็น 1 สัปดาห์ของเทอม ยิ่งเล่นนาน ศัตรูยิ่งเกิดถี่ขึ้น (ต่ำสุดทุก 0.3 วินาที) บอสมาบ่อยขึ้น (ต่ำสุดทุก 6 วินาที) และตั้งแต่ Week 6 ศัตรูอาจมาทีละ 2 ตัว เกมจึงจบเสมอไม่ว่าผู้เล่นจะเก่งแค่ไหน

| ศัตรู | พฤติกรรม | ยิงกี่นัดถึงตาย | คะแนน |
|---|---|---|---|
| 📄 Homework (สีส้ม) | ตกลงมาตรงๆ ช้าๆ | 1 | 10 |
| ❓ Quiz (สีม่วง) | ส่ายซ้าย-ขวาแบบซิกแซกขณะตกลงมา | 1 | 15 |
| 💀 Midterm Boss (สีแดง) | โผล่ทุก 15 วินาที ลงมาด้านบน ไล่ตามผู้เล่นซ้าย-ขวา และยิงเกรด F ในวงกลมแดงลงมาทุก 1.2 วินาที (โดนแล้วเสียพลังชีวิต 10) | 20 | 200 |

**ไอเทม** (วงกลมที่ตกลงมาทุก 8 วินาที เดินไปชนเพื่อเก็บ)

| ไอเทม | ผล |
|---|---|
| ☕ Coffee (สีน้ำตาล) | เดินเร็วขึ้น 1.5 เท่า นาน 5 วินาที (มีกรอบสีน้ำตาลล้อมตัวระหว่างมีผล) |
| 😴 Sleep (สีเขียว) | ฟื้นพลังชีวิต 30 (ไม่เกิน 100) |

**จบเกม:** เมื่อพลังชีวิตเหลือ 0 เกมจะแสดงคะแนนและ "เกรด" แบบลายมือวงแดงเหมือนครูให้คะแนน ตามเกณฑ์นี้ แล้วกด `R` เพื่อเล่นใหม่

| คะแนน | ≥ 1500 | ≥ 1200 | ≥ 900 | ≥ 700 | ≥ 500 | ≥ 350 | ≥ 200 | ต่ำกว่า 200 |
|---|---|---|---|---|---|---|---|---|
| เกรด | A | B+ | B | C+ | C | D+ | D | F |

## 📁 โครงสร้างโปรเจกต์

```
lock_in_mode/
├── main.py              # จุดเริ่มโปรแกรม: สร้าง Game แล้วเริ่มที่ MenuState
├── settings.py          # ค่าคงที่: ขนาดจอ, FPS, สี
├── game.py              # Game: เกมลูป และ state stack (change/push/pop)
├── states.py            # GameState(ABC) และ MenuState / PlayState / PauseState / GameOverState
├── entities.py          # GameObject(ABC), Player, Bullet, EnemyBullet, Enemy, Homework, Quiz, MidtermBoss, PowerUp, Coffee, Sleep
├── sprites.py           # รูปตัวละคร: โหลดรูปจาก assets/ ถ้าไม่มีใช้รูปที่วาดด้วยโค้ด
├── components.py        # Health, Weapon (ใช้แบบ composition)
├── events.py            # อีเวนต์ของเกม: ENEMY_KILLED, PLAYER_HIT
├── observers.py         # ScoreManager (Observer)
├── test_game.py         # ชุดทดสอบอัตโนมัติ 27 ข้อ (unittest)
├── check_components.py  # ทดสอบ Health และ Weapon แบบไม่เปิดหน้าต่าง
├── assets/              # รูปตัวละครสไตล์ doodle (.png)
│   └── fonts/           # ฟอนต์ลายมือ + ไฟล์สัญญาอนุญาต
├── docs/
│   └── class-diagram.png
├── README.md
└── AI_LOG.md
```

## 🧱 สถาปัตยกรรม OOP

| แนวคิด | อยู่ตรงไหนในเกม |
|---|---|
| Encapsulation | แอตทริบิวต์ขึ้นต้นด้วย `_` อ่านผ่าน `@property` เช่น `Player.speed` มี setter ที่ยก `ValueError` ถ้าค่าไม่อยู่ในช่วง 100–600 (แม้แต่ตอนกาแฟเร่งความเร็วก็ต้องผ่าน setter) และ `Health.hp` ถูกล็อกให้อยู่ระหว่าง 0 ถึง `max_hp` เสมอ |
| Composition | `Player` มี `Health` และ `Weapon` / `Enemy` มี `Health` / `MidtermBoss` ใช้ `Weapon` คลาสเดียวกับผู้เล่น (คูลดาวน์ 1.2 วินาที) แล้วส่งต่องาน (delegation) ให้คอมโพเนนต์จัดการ |
| Inheritance | `Player`, `Bullet`, `EnemyBullet`, `Enemy`, `PowerUp` สืบทอดจาก `GameObject` / `Homework`, `Quiz`, `MidtermBoss` สืบทอดจาก `Enemy` / `Coffee`, `Sleep` สืบทอดจาก `PowerUp` ทุกคลาสเรียก `super().__init__()` เป็นบรรทัดแรก |
| Method Overriding | `MidtermBoss` แทนที่ `image_name()` ให้เปลี่ยนเป็นหน้าโกรธเมื่อเลือดต่ำกว่าครึ่ง / `Homework`, `Quiz`, `MidtermBoss` แทนที่ `update()` ด้วยการเคลื่อนที่ของตัวเอง แล้วเรียก `super().update()` ให้ `Enemy` ตรวจการตกขอบจอ และ `MidtermBoss` แทนที่ `try_shoot()` (ค่าเริ่มต้นของ `Enemy` คืน `None`) ให้ยิงกระสุนได้ |
| Polymorphism | `PlayState` เก็บผู้เล่น กระสุน ศัตรู และไอเทมทุกชนิดไว้รวมกัน แล้วเรียก `update()` / `draw()` ในลูปเดียวโดยไม่ตรวจชนิด (ไม่มี `isinstance`) เก็บไอเทมด้วย `item.apply(player)` บรรทัดเดียวไม่ว่าจะเป็นไอเทมชนิดไหน และเรียก `enemy.try_shoot()` กับศัตรูทุกตัวโดยไม่ต้องเช็กว่าตัวไหนเป็นบอส |
| Abstract Base Class | `GameObject(ABC)` บังคับสัญญา `update(dt)` / `draw(screen)`, `PowerUp` เพิ่มสัญญา `apply(player)` และ `GameState(ABC)` บังคับ `handle_event` / `update` / `draw` |
| Events + Observer | `PlayState._check_collisions()` ส่งอีเวนต์ `ENEMY_KILLED`, `PLAYER_HIT` ผ่าน `pygame.event.post()` แล้ว `ScoreManager.handle_event()` เป็นผู้รับ เพิ่ม observer ใหม่ได้โดยไม่ต้องแก้โค้ดการชน |
| State Pattern | `Game` ถือ `state_stack`: `change_state()` สลับหน้าจอ, `push_state()` วาง Pause ทับ Play, `pop_state()` กลับไปเล่นต่อ |

แผนภาพคลาส UML ทั้งหมดอยู่ที่ [`docs/class-diagram.png`](docs/class-diagram.png)

