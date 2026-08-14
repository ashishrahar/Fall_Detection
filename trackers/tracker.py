from collections import defaultdict, deque

class PersonTracker:
    def __init__(self):
        # Har person ki last 30 positions store hongi
        self.history = defaultdict(lambda: deque(maxlen=30))

    def update(self, person_id, center):
        self.history[person_id].append(center)

    def get_history(self, person_id):
        return list(self.history[person_id])

    def clear_missing(self, active_ids):
        old_ids = list(self.history.keys())

        for pid in old_ids:
            if pid not in active_ids:
                del self.history[pid]
