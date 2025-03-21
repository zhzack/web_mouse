from typing import List, Dict, Any
import math

class GestureRecognizer:
    def __init__(self):
        self.recognizers = []

    def add_recognizer(self, recognizer):
        self.recognizers.append(recognizer)

    def recognize(self, points_sequence: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
        results = {}
        for recognizer in self.recognizers:
            result = recognizer.recognize(points_sequence)
            if result is not None:
                results.update(result)
        return results


def calculate_angle(p1, p2):
    dx = p2['x'] - p1['x']
    dy = p2['y'] - p1['y']
    return math.atan2(dy, dx)


def calculate_distance(p1, p2):
    dx = p2['x'] - p1['x']
    dy = p2['y'] - p1['y']
    return math.sqrt(dx ** 2 + dy ** 2)


class SwipeRecognizer:
    def recognize(self, points_sequence: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
        if len(points_sequence) < 2:
            return None

        prev_points = points_sequence[-2]
        curr_points = points_sequence[-1]

        if len(curr_points) == 1:  # 单指滑动
            p1 = prev_points[0]
            p2 = curr_points[0]
            angle = math.degrees(calculate_angle(p1, p2))

            if calculate_distance(p1, p2) > 50:  # 判断为滑动
                return {"swipe": angle}
        return None


class RotateRecognizer:
    def recognize(self, points_sequence: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
        if len(points_sequence) < 2:
            return None

        prev_points = points_sequence[-2]
        curr_points = points_sequence[-1]

        if len(curr_points) > 1:  # 多指旋转
            angles = []
            for i in range(len(curr_points)):
                p1 = prev_points[i]
                p2 = curr_points[i]
                angles.append(calculate_angle(p1, p2))

            if len(angles) == 2:  # 双指旋转检测
                angle_diff = math.degrees(angles[1] - angles[0])
                if abs(angle_diff) > 10:  # 判断为旋转
                    return {"rotate": angle_diff}
        return None


gesture_recognizer = GestureRecognizer()
gesture_recognizer.add_recognizer(SwipeRecognizer())
gesture_recognizer.add_recognizer(RotateRecognizer())

def process_gesture(points_sequence: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
    return gesture_recognizer.recognize(points_sequence)
