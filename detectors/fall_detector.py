import time

class FallDetector:

    def __init__(self):

        # standing | falling | fallen
        self.state = {}

        # Fall start time
        self.start_time = {}

    def check_fall(self, person_id, angle, speed):

        # New Person
        if person_id not in self.state:
            self.state[person_id] = "standing"

        state = self.state[person_id]

        # ==========================
        # STATE : STANDING
        # ==========================
        if state == "standing":

            print(f"ID:{person_id}  State: STANDING")

            # Sudden fall starts
            if angle >= 60 and abs(speed) >= 15:

                self.state[person_id] = "falling"
                self.start_time[person_id] = time.time()

                print(f"ID:{person_id}  >>> FALLING <<<")

            return False

        # ==========================
        # STATE : FALLING
        # ==========================
        elif state == "falling":

            # Person still horizontal
            if angle >= 60:

                elapsed = time.time() - self.start_time[person_id]

                print(
                    f"ID:{person_id}  "
                    f"Ground:{elapsed:.1f}s"
                )

                # Stayed on ground
                if elapsed >= 2:

                    self.state[person_id] = "fallen"

                    print(f"ID:{person_id}  >>> FALLEN <<<")

                    return True

            else:

                # False alarm
                print(f"ID:{person_id}  Recovered")

                self.state[person_id] = "standing"

                self.start_time.pop(person_id, None)

            return False

        # ==========================
        # STATE : FALLEN
        # ==========================
        elif state == "fallen":

            # Person stood up
            if angle < 45:

                print(f"ID:{person_id}  Back To Standing")

                self.state[person_id] = "standing"

                self.start_time.pop(person_id, None)

                return False

            return True
