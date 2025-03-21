import math

# 计算两个点之间的距离


def calculate_distance(p1, p2):
    return math.sqrt((p2['x'] - p1['x'])**2 + (p2['y'] - p1['y'])**2)

# 计算两个点之间的方向角


def calculate_angle(p1, p2):
    return math.atan2(p2['y'] - p1['y'], p2['x'] - p1['x'])

# 计算位移方向，返回角度（度数）


def calculate_move_direction(p1, p2):
    angle = math.atan2(p2['y'] - p1['y'], p2['x'] - p1['x'])
    return math.degrees(angle)  # 转换为度数

# 检测是否为捏合（Pinch）手势


def detect_pinch(p1, p2, prev_p1, prev_p2):
    current_distance = calculate_distance(p1, p2)
    previous_distance = calculate_distance(prev_p1, prev_p2)

    if abs(current_distance - previous_distance) > 10:  # 捏合变化的阈值
        if current_distance < previous_distance:
            return "Pinch in"
        elif current_distance > previous_distance:
            return "Pinch out"
    return None

# 检测是否为旋转（Rotate）手势


def detect_rotation(p1, p2, prev_p1, prev_p2):
    current_angle = calculate_angle(p1, p2)
    previous_angle = calculate_angle(prev_p1, prev_p2)

    angle_diff = math.degrees(current_angle - previous_angle)

    if abs(angle_diff) > 5:  # 旋转变化的阈值
        if angle_diff > 0:
            return "Rotate clockwise"
        else:
            return "Rotate counterclockwise"
    return None

# 检测是否为整体移动（Move）手势，并返回方向


def detect_move(p1, p2, prev_p1, prev_p2):
    move_distance_p1 = calculate_distance(p1, prev_p1)
    move_distance_p2 = calculate_distance(p2, prev_p2)

    if move_distance_p1 > 5 or move_distance_p2 > 5:  # 移动的阈值
        direction = calculate_move_direction(prev_p1, p1)
        return f"Move with direction: {direction}°"
    return None

# 多指手势识别函数


def multi_touch_gesture_recognition(data_array):
    if len(data_array) < 2:
        return "Insufficient data for recognition."

    # 获取最后两个数据
    prev_points, points = data_array[-2], data_array[-1]

    if len(points) != len(prev_points):
        return "Error: The number of points must match."

    gestures = []

    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]

        prev_p1 = prev_points[i]
        prev_p2 = prev_points[(i + 1) % len(prev_points)]

        # 检测捏合手势
        pinch = detect_pinch(p1, p2, prev_p1, prev_p2)
        if pinch:
            gestures.append(pinch)

        # 检测旋转手势
        rotation = detect_rotation(p1, p2, prev_p1, prev_p2)
        if rotation:
            gestures.append(rotation)

        # 检测移动手势
        move = detect_move(p1, p2, prev_p1, prev_p2)
        if move:
            gestures.append(move)

    return gestures


if __name__ == '__main__':
    data_array = [[{'id': 0, 'x': 191.132, 'y': 697.75}, {'id': 1, 'x': 250.573, 'y': 530.609}], [{'id': 0, 'x': 191.132, 'y': 697.75}, {'id': 1, 'x': 251.445, 'y': 530.847}], [{'id': 0, 'x': 194.78, 'y': 698.98}, {'id': 1, 'x': 256.918, 'y': 532.592}], [{'id': 0, 'x': 198.666, 'y': 700.368}, {'id': 1, 'x': 261.041, 'y': 533.9}], [{'id': 0, 'x': 203.345, 'y': 702.311}, {'id': 1, 'x': 265.483, 'y': 535.408}], [{'id': 0, 'x': 210.84, 'y': 707.069}, {'id': 1, 'x': 272.462, 'y': 539.254}], [{'id': 0, 'x': 214.329, 'y': 709.687}, {'id': 1, 'x': 275.872, 'y': 541.593}], [{'id': 0, 'x': 220.753, 'y': 714.326}, {'id': 1, 'x': 283.842, 'y': 546.907}], [{'id': 0, 'x': 224.044, 'y': 716.467}, {'id': 1, 'x': 287.53, 'y': 549.564}], [{'id': 0, 'x': 231.023, 'y': 720.909}, {'id': 1, 'x': 296.611, 'y': 554.838}], [{'id': 0, 'x': 235.346, 'y': 723.169}, {'id': 1, 'x': 300.616, 'y': 557.296}], [
        {'id': 0, 'x': 239.47, 'y': 725.23}, {'id': 1, 'x': 304.304, 'y': 559.597}], [{'id': 0, 'x': 246.488, 'y': 728.205}, {'id': 1, 'x': 311.68, 'y': 563.562}], [{'id': 0, 'x': 249.978, 'y': 729.315}, {'id': 1, 'x': 315.645, 'y': 564.513}], [{'id': 0, 'x': 258.385, 'y': 731.1}, {'id': 1, 'x': 325.677, 'y': 566.02}], [{'id': 0, 'x': 262.786, 'y': 731.694}, {'id': 1, 'x': 330.356, 'y': 566.377}], [{'id': 0, 'x': 270.757, 'y': 732.21}, {'id': 1, 'x': 338.724, 'y': 566.893}], [{'id': 0, 'x': 274.365, 'y': 732.289}, {'id': 1, 'x': 343.046, 'y': 567.011}], [{'id': 0, 'x': 277.657, 'y': 732.448}, {'id': 1, 'x': 347.923, 'y': 567.091}], [{'id': 0, 'x': 285.429, 'y': 733.875}, {'id': 1, 'x': 356.766, 'y': 567.369}], [{'id': 0, 'x': 289.434, 'y': 734.946}, {'id': 1, 'x': 360.374, 'y': 567.765}], [{'id': 0, 'x': 292.923, 'y': 735.779}, {'id': 1, 'x': 366.164, 'y': 569.113}]]

    gestures = multi_touch_gesture_recognition(data_array)
    print(gestures)
