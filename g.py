import win32api
import win32con
import time

def simulate_touch(x, y):
    # 模拟触摸输入
    win32api.SetCursorPos((x, y))  # 移动光标到 (x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)  # 按下左键
    time.sleep(0.1)  # 持续一段时间
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)  # 松开左键

# 示例：模拟触摸事件
if __name__ == "__main__":
    simulate_touch(400, 400)  # 模拟在屏幕中间的触摸
