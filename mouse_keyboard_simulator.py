from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key
import time

# 初始化鼠标和键盘控制器
mouse = MouseController()
keyboard = KeyboardController()

def simulate_mouse_and_keyboard():
    # 模拟鼠标操作
    mouse.position = (500, 500)  # 移动鼠标到屏幕坐标 (500, 500)
    time.sleep(1)
    mouse.click(Button.left, 1)  # 左键单击

    # 模拟键盘操作
    keys_to_press = ['a', 'b', 'c', 'd', Key.enter]  # 定义要按下的按键
    for key in keys_to_press:
        keyboard.press(key)  # 按下按键
        keyboard.release(key)  # 释放按键
        time.sleep(0.5)  # 每次按键之间等待 0.5 秒

if __name__ == "__main__":
    simulate_mouse_and_keyboard()
