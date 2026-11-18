from events import ENEMY_KILLED, PLAYER_HIT


class ScoreManager:
    """Observer: ฟังอีเวนต์แล้วเก็บคะแนน จำนวนศัตรูที่ยิงได้ และจำนวนครั้งที่โดนชน"""

    GRADE_CUTOFFS = [(1500, "A"), (1200, "B+"), (900, "B"), (700, "C+"),
                     (500, "C"), (350, "D+"), (200, "D")]

    def __init__(self):
        self._score = 0
        self._kills = 0
        self._hits_taken = 0

    @property
    def score(self):
        return self._score

    @property
    def kills(self):
        return self._kills

    @property
    def hits_taken(self):
        return self._hits_taken

    @property
    def grade(self):
        for cutoff, letter in self.GRADE_CUTOFFS:
            if self._score >= cutoff:
                return letter
        return "F"

    def handle_event(self, event):
        if event.type == ENEMY_KILLED:
            self._score += event.points
            self._kills += 1
        elif event.type == PLAYER_HIT:
            self._hits_taken += 1