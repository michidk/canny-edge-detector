# calculates the direction a certain angle is facing as need in the canny edge detector
def angle_to_direction(angle):
    if angle < -22.5: # mirror angle
        angle = angle + 180
    if angle > 157.5:
        angle = angle - 180

    if angle >= -22.5 and angle <= 22.5:
        return 0.0 # round to 0
    elif angle >= 22.5 and angle <= 67.5:
        return 1.0 # round to 45
    elif angle >= 67.5 and angle <= 112.5:
        return 2.0 # round to 90
    elif angle >= 112.5 and angle <= 157.5:
        return 3.0 # round to 135
    else:
        print(angle)
