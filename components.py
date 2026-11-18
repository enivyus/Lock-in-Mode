class Health:
    
    def __init__(self, max_hp):
        if max_hp <= 0:
            raise ValueError("max_hp must be positive")
        self._max_hp = max_hp
        self._hp = max_hp
        
    @property
    def hp(self):
        return self._hp
    
    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, self._max_hp))
        
    @property 
    def max_hp(self):
        return self._max_hp
    
    @property
    def is_alive(self):
        return self._hp > 0
    
    def take_damage(self,amount):
        if amount < 0:
            raise ValueError("damage cannot be negative")
        self.hp -= amount
        
    def heal(self, amount):
        if amount < 0:
            raise ValueError("heal amount cannot be negative")
        self.hp += amount
         

class Weapon:
    
    def __init__(self, cooldown=0.25):
        self._cooldown = cooldown
        self._timer = 0.0
        
    def update(self, dt):
        self._timer = max(0.0, self._timer - dt)
        
    def try_fire(self):
        if self._timer > 0:
            return False
        self._timer = self._cooldown
        return True
        

        
        
        