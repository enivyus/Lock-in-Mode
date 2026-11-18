from components import Health, Weapon

h = Health(100)
h.take_damage(30)
print("hp หลังโดน 30:", h.hp)            # ควรได้ 70
h.take_damage(999)
print("hp หลังโดน 999:", h.hp)           # ควรได้ 0 (ไม่ติดลบ)
print("ยังมีชีวิตไหม:", h.is_alive)       # ควรได้ False
h.heal(50)
print("hp หลังฮีล 50:", h.hp)            # ควรได้ 50

w = Weapon(cooldown=0.25)
print("ยิงนัดแรก:", w.try_fire())         # True
print("ยิงซ้ำทันที:", w.try_fire())       # False (ยังคูลดาวน์)
w.update(0.3)                             # ผ่านไป 0.3 วินาที
print("ยิงหลัง 0.3 วิ:", w.try_fire())    # True