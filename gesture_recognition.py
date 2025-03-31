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

# 检测滑动手势的方向（支持两指到五指以上）。
# 返回八个方向之一：上、下、左、右、左上、右上、左下、右下。


def detect_swipe(trajectories):
    """
    检测滑动手势的方向（支持两指到五指以上）。
    返回八个方向之一：上、下、左、右、左上、右上、左下、右下。
    """
    avg_dx, avg_dy = _calculate_average_movement(trajectories)

    if abs(avg_dx) < 10 and abs(avg_dy) < 10:
        return None  # 移动距离太小，忽略

    angle = math.degrees(math.atan2(-avg_dy, avg_dx))  # 修正上下方向
    if -22.5 <= angle < 22.5:
        return "右滑"
    elif 22.5 <= angle < 67.5:
        return "右上滑"
    elif 67.5 <= angle < 112.5:
        return "上滑"
    elif 112.5 <= angle < 157.5:
        return "左上滑"
    elif 157.5 <= angle or angle < -157.5:
        return "左滑"
    elif -157.5 <= angle < -112.5:
        return "左下滑"
    elif -112.5 <= angle < -67.5:
        return "下滑"
    elif -67.5 <= angle < -22.5:
        return "右下滑"
    return None

# 检测旋转手势（顺时针或逆时针）。


def detect_rotation(trajectories):
    if len(trajectories) < 2:
        return None  # 至少需要两指进行旋转检测

    # 计算两指的初始和最终角度
    finger_1 = trajectories[0]
    finger_2 = trajectories[1]

    start_angle = math.atan2(finger_2[0][1] - finger_1[0][1], finger_2[0][0] - finger_1[0][0])
    end_angle = math.atan2(finger_2[-1][1] - finger_1[-1][1], finger_2[-1][0] - finger_1[-1][0])

    angle_diff = math.degrees(end_angle - start_angle)

    if abs(angle_diff) > 15:  # 旋转角度阈值
        if angle_diff > 0:
            return "顺时针旋转"
        else:
            return "逆时针旋转"
    return None

# 多指手势识别函数


def multi_touch_gesture_recognition(touch_points):
    """
    根据多指触摸点的集合综合判断输入的动作。
    支持两指到五指以上的八个方向滑动，以及顺时针和逆时针旋转。
    """
    try:
        if not touch_points or len(touch_points[0]) < 1:  # 修正手指数量判断
            return "未知手势"

        # 计算每帧的触摸点数量
        num_fingers = len(touch_points[0])  # 假设每帧的触摸点数量一致
        print(f"手势识别: 当前帧手指数量: {num_fingers}")

        # 提取所有触摸点的轨迹
        trajectories = {i: [] for i in range(num_fingers)}
        for frame in touch_points:
            for i, point in enumerate(frame):
                trajectories[i].append((point['x'], point['y']))

        # 检测滑动手势
        swipe_result = detect_swipe(trajectories)
        if swipe_result:
            return f"{num_fingers}指{swipe_result}"

        # 检测旋转手势
        rotation_result = detect_rotation(trajectories)
        if rotation_result:
            return rotation_result

        return "未知手势"
    except Exception as e:
        print(f"multi_touch_gesture_recognition 错误: {e}")
        raise  # 重新抛出异常以便进一步调试


def _calculate_distance(point1, point2):
    """计算两点之间的欧几里得距离"""
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


def _calculate_average_movement(trajectories):
    """
    计算所有触摸点的平均移动向量。
    
    参数:
        trajectories (dict): 每个触摸点的轨迹字典。
    
    返回:
        tuple: 平均移动向量 (dx, dy)。
    """
    total_dx, total_dy = 0, 0
    num_points = 0

    for trajectory in trajectories.values():
        start_x, start_y = trajectory[0]
        end_x, end_y = trajectory[-1]
        total_dx += end_x - start_x
        total_dy += end_y - start_y
        num_points += 1

    return total_dx / num_points, total_dy / num_points


if __name__ == '__main__':
    data_array = [
        [{'id': 0, 'x': 100, 'y': 100}, {'id': 1, 'x': 200, 'y': 100}],
        [{'id': 0, 'x': 110, 'y': 110}, {'id': 1, 'x': 210, 'y': 110}],
        [{'id': 0, 'x': 120, 'y': 120}, {'id': 1, 'x': 220, 'y': 120}],
        [{'id': 0, 'x': 130, 'y': 130}, {'id': 1, 'x': 230, 'y': 130}],
    ]

    gestures = multi_touch_gesture_recognition(data_array)
    print(gestures)
