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
data_array = [
    [{'id': 0, 'x': 803.553, 'y': 1112.208}], [{'id': 0, 'x': 802.97, 'y': 1125.519}], [{'id': 0, 'x': 797.238, 'y': 1163.797}], [{'id': 0, 'x': 792.187, 'y': 1189.348}], [{'id': 0, 'x': 779.071, 'y': 1236.37}], [{'id': 0, 'x': 772.076, 'y': 1255.704}], [{'id': 0, 'x': 765.566, 'y': 1275.231}], [{'id': 0, 'x': 754.685, 'y': 1309.915}], [{'id': 0, 'x': 750.313, 'y': 1324.293}], [{'id': 0, 'x': 743.512, 'y': 1350.039}], [{'id': 0, 'x': 739.821, 'y': 1362.183}], [{'id': 0, 'x': 736.031, 'y': 1384.723}], [{'id': 0, 'x': 733.992, 'y': 1394.633}], [{'id': 0, 'x': 731.757, 'y': 1405.708}], [{'id': 0, 'x': 727.191, 'y': 1425.041}], [{'id': 0, 'x': 725.053, 'y': 1433.591}], [{'id': 0, 'x': 719.224, 'y': 1448.164}], [{'id': 0, 'x': 716.504, 'y': 1453.993}], [{'id': 0, 'x': 711.355, 'y': 1464.486}], [{'id': 0, 'x': 708.829, 'y': 1468.76}], [{'id': 0, 'x': 706.303, 'y': 1472.646}], [{'id': 0, 'x': 701.542, 'y': 1482.459}] 
]

gestures = multi_touch_gesture_recognition(data_array)
print(gestures)
