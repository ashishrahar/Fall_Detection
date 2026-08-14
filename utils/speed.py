from collections import defaultdict

class SpeedTracker:

    def __init__(self):
        self.prev_hip = defaultdict(lambda: None)

    def get_speed(self, person_id, hip_y):

        if self.prev_hip[person_id] is None:
            self.prev_hip[person_id] = hip_y
            return 0

        speed = hip_y - self.prev_hip[person_id]

        self.prev_hip[person_id] = hip_y

        return speed
