import cv2


class PoseDetector:

    def get_keypoints(self, result):

        if result.keypoints is None:
            return None

        return result.keypoints.xy

    def draw_keypoints(self, frame, keypoints):

        if keypoints is None:
            return frame

        for person in keypoints:

            for point in person:

                x = int(point[0])
                y = int(point[1])

                cv2.circle(
                    frame,
                    (x, y),
                    4,
                    (0, 255, 255),
                    -1
                )

        return frame

    def draw_skeleton(self, frame, keypoints):

        if keypoints is None:
            return frame

        skeleton = [
            (5, 7), (7, 9),
            (6, 8), (8, 10),
            (5, 6),
            (5, 11), (6, 12),
            (11, 12),
            (11, 13), (13, 15),
            (12, 14), (14, 16)
        ]

        for person in keypoints:

            for start, end in skeleton:

                x1, y1 = person[start]
                x2, y2 = person[end]

                cv2.line(
                    frame,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (0, 255, 0),
                    2
                )

        return frame

    def get_body_points(self, person):

        # Left Shoulder
        ls = person[5]

        # Right Shoulder
        rs = person[6]

        # Left Hip
        lh = person[11]

        # Right Hip
        rh = person[12]

        # Shoulder Center
        shoulder_x = int((ls[0] + rs[0]) / 2)
        shoulder_y = int((ls[1] + rs[1]) / 2)

        # Hip Center
        hip_x = int((lh[0] + rh[0]) / 2)
        hip_y = int((lh[1] + rh[1]) / 2)

        return shoulder_x, shoulder_y, hip_x, hip_y
    
    def get_pose_center(self, person):

        sx, sy, hx, hy = self.get_body_points(person)

        center_x = (sx + hx) // 2
        center_y = (sy + hy) // 2

        return center_x, center_y
        
