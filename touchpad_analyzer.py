
import json
import math


class TouchPadAnalyzer:
    def __init__(self):
        # 初始化任何你需要的变量
        self.touch_points = []
        self.move_num = 3  # 小于这个数的move定义为点击
        self.double_click_delta_time = 1741983463489-1741983463258  # 双击间隔时间
        self.last_click_num = 0  # 上一次点击是几指
        self.last_click_time = 0

    def process_data(self, data):
        try:
            # 解析接收到的数据
            event_data = json.loads(data)
            event_type = event_data.get('t')  # 获取事件类型
            timestamp = event_data.get('ts')  # 获取时间戳
            touch_points = event_data.get('pts', [])  # 获取触摸点信息
            num_finger = len(touch_points)
            
            # 处理触摸点
            if event_type == 'ts':
                self.touch_points = []
                self.move_num = num_finger
                self.touch_points.append(touch_points)
            elif event_type == 'tm':
                if self.move_num != num_finger:
                    self.touch_points = []
                    self.move_num = num_finger
                self.touch_points.append(touch_points)
                # 识别手势
                gestures = multi_touch_gesture_recognition(self.touch_points)
                print(gestures)
            elif event_type == 'te':

                if len(self.touch_points) < self.move_num:
                    
                    diff_time = timestamp-self.last_click_time
                    if diff_time < self.double_click_delta_time and self.last_click_num == num_finger:
                        print(num_finger, "双击")
                    elif diff_time > self.double_click_delta_time:
                        print(num_finger, "点击")
                    self.last_click_num = num_finger
                    self.last_click_time = timestamp

        except Exception as e:
            print(f"数据处理错误: {e}")


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

# 多指手势识别函数，使用整个数据数组


def multi_touch_gesture_recognition(data_array):
    if len(data_array) < 2:
        return "Insufficient data for recognition."

    # 使用整个数组的数据来判断
    prev_points = data_array[-2]
    points = data_array[-1]

    if len(points) != len(prev_points):
        return "Error: The number of points must match."

    gestures = []

    # 遍历每个时间点的触摸点
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

    # 扩展使用整个数据数组来判断趋势，防止漏掉快速小幅度移动
    return gestures

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

# 多指手势识别函数，使用整个数据数组


def multi_touch_gesture_recognition(data_array):
    if len(data_array) < 2:
        return "Insufficient data for recognition."

    # 使用整个数组的数据来判断
    prev_points = data_array[0]
    points = data_array[-1]

    if len(points) != len(prev_points):
        return "Error: The number of points must match."

    gestures = []

    # 遍历每个时间点的触摸点
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

    # 扩展使用整个数据数组来判断趋势，防止漏掉快速小幅度移动
    return gestures
