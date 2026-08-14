import math


def body_angle(shoulder_x, shoulder_y, hip_x, hip_y):

    dx = hip_x - shoulder_x
    dy = hip_y - shoulder_y

    angle = abs(math.degrees(math.atan2(dx, dy)))

    return angle
