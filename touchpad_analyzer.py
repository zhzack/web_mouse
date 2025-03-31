import json
from gesture_recognition import multi_touch_gesture_recognition  # 导入手势识别模块

class TouchPadAnalyzer:
    def __init__(self):
        self.touch_points = []  # 存储所有触摸点的历史记录
        self.current_touch_points = []  # 当前触摸点
        self.num_finger = 0  # 当前的手指数量
        self.click_threshold = 8  # 少于这个数量的触摸点视为点击
        self.double_click_threshold = 500  # 双击的最大间隔时间（毫秒）
        self.last_click_num = 0  # 上一次点击的手指数量
        self.last_click_time = 0  # 上一次点击的时间戳
        self.last_te_time = 0  # 最近一次 te 事件的时间戳

    def process_data(self, data: str):
        """处理接收到的数据"""
        print('收到的数据:', data)
        try:
            # 尝试解析JSON数据
            event_data = json.loads(data)
            event_type = event_data.get('t')
            timestamp = event_data.get('ts')
            touch_points = event_data.get('pts', [])

            # 验证数据完整性
            if event_type not in ['ts', 'tm', 'te'] or timestamp is None:
                print("数据格式错误或缺失关键字段")
                return

            # 根据事件类型处理
            if event_type == 'ts':  # 触摸开始
                self._handle_touch_start(touch_points)

            elif event_type == 'tm':  # 触摸移动
                # 如果是单指移动，直接返回
                if len(touch_points) == 1:
                    return
                self._handle_touch_move(touch_points)

            elif event_type == 'te':  # 触摸结束
                self._handle_touch_end(touch_points, timestamp)

        except json.JSONDecodeError:
            print("JSON解析错误")
        except Exception as e:
            print(f"数据处理错误: {e}")
            raise  # 重新抛出异常以便进一步调试

    def _handle_touch_start(self, touch_points):
        """处理触摸开始事件"""
        self.current_touch_points = touch_points  # 更新当前触摸点
        self.num_finger = len(touch_points)  # 更新当前手指数量
        print(f"触摸开始: {self.num_finger} 指触摸")

    def _handle_touch_move(self, touch_points):
        """处理触摸移动事件"""
        try:
            self.current_touch_points = touch_points  # 更新当前触摸点
            self.num_finger = len(touch_points)  # 更新当前手指数量
            print(f"触摸移动: {self.num_finger} 指触摸")

            self.touch_points.append(touch_points)  # 记录触摸点历史

            if len(self.touch_points) > self.click_threshold:
                # 识别手势
                gesture = multi_touch_gesture_recognition(self.touch_points)
                print(f"识别出的手势: {gesture}")
        except Exception as e:
            print(f"_handle_touch_move 错误: {e}")
            raise  # 重新抛出异常以便进一步调试

    def _handle_touch_end(self, touch_points, timestamp):
        """处理触摸结束事件"""
        if len(touch_points) > 0:
            # 如果 pts 非空，表示部分抬起，更新记录但不进行点击检测
            self.current_touch_points = touch_points
            self.num_finger = len(touch_points)  # 更新当前手指数量
            print(f"部分手指抬起: {self.num_finger} 指剩余")
            self.last_te_time = timestamp
            return

        # 检查是否是一个完整的点击（所有手指抬起）
        if len(self.current_touch_points) <= self.click_threshold:
            if self.last_click_num == self.num_finger:
                print(f"{self.num_finger} 指点击")

            # 更新点击记录
            self.last_click_num = self.num_finger
            self.last_click_time = timestamp

        # 重置触摸点记录
        self.current_touch_points = []
        self.num_finger = 0
        print("所有手指抬起，触摸结束")
