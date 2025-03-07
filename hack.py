import multiprocessing

from PIL import Image, ImageDraw  # 新增导入
import os

# 新增图标生成函数（可放在 resource_path 下方）
def check_and_generate_icon():
    icon_path = resource_path("icon.ico")
    if not os.path.exists(icon_path):
        try:
            img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.ellipse((0, 0, 63, 63), fill=(220, 20, 60))  # 生成红色备用图标
            img.save(icon_path, format='ICO')
        except Exception as e:
            print(f"自动生成图标失败: {str(e)}")

# 在 __init__ 方法最开始调用
class AutoClickerApp:
    def __init__(self, root):
        check_and_generate_icon()  # 新增此行
        # 其他原有代码...
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import threading
import time
import keyboard  # 新增键盘监听库


# PyInstaller 资源路径处理
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("自动连点器 v3.0")
        self.running = False
        self.click_thread = None
        self.hotkey = "<F6>"  # 默认热键
        self.recording = False  # 热键录制状态

        # 加载图标
        try:
            self.root.iconbitmap(resource_path('icon.ico'))
        except:
            pass

        self.create_widgets()
        self.setup_hotkey()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill='both', expand=True)

        # 热键设置区域
        hotkey_frame = ttk.LabelFrame(main_frame, text="快捷键设置", padding=10)
        hotkey_frame.pack(fill='x', pady=5)

        self.hotkey_btn = ttk.Button(
            hotkey_frame,
            text="点击设置快捷键",
            command=self.start_hotkey_recording
        )
        self.hotkey_btn.pack(side='left')

        self.hotkey_label = ttk.Label(
            hotkey_frame,
            text=f"当前快捷键：{self.hotkey}",
            width=20
        )
        self.hotkey_label.pack(side='left', padx=10)

        # 点击设置区域
        settings_frame = ttk.Frame(main_frame)
        settings_frame.pack(fill='x', pady=5)

        # 间隔时间
        ttk.Label(settings_frame, text="点击间隔（秒）:").pack(side='left')
        self.interval = tk.DoubleVar(value=0.1)
        ttk.Entry(settings_frame, textvariable=self.interval, width=8).pack(side='left', padx=5)

        # 鼠标按钮
        ttk.Label(settings_frame, text="鼠标按钮:").pack(side='left', padx=(10, 0))
        self.mouse_button = tk.StringVar(value='left')
        ttk.Combobox(
            settings_frame,
            textvariable=self.mouse_button,
            values=['left', 'right', 'middle'],
            state='readonly',
            width=8
        ).pack(side='left')

        # 控制按钮
        ctrl_frame = ttk.Frame(main_frame)
        ctrl_frame.pack(fill='x', pady=10)

        self.start_btn = ttk.Button(
            ctrl_frame,
            text=f"开始 ({self.hotkey})",
            command=self.toggle_click
        )
        self.start_btn.pack(side='left')

        ttk.Button(
            ctrl_frame,
            text="退出",
            command=self.root.quit
        ).pack(side='right')

        # 状态栏
        self.status = ttk.Label(
            self.root,
            text="状态: 等待中",
            relief='sunken',
            padding=(5, 2)
        )
        self.status.pack(fill='x', padx=10, pady=5)

    def setup_hotkey(self):
        """绑定热键事件"""
        try:
            self.root.unbind(self.hotkey)
        except tk.TclError:
            pass
        self.root.bind(self.hotkey, lambda e: self.toggle_click())

    def start_hotkey_recording(self):
        """开始录制快捷键"""
        self.recording = True
        self.hotkey_btn.config(text="按下新快捷键...")
        self.status.config(text="状态: 正在录制快捷键...")

        # 开启键盘监听
        keyboard.hook(self.process_hotkey)

    def process_hotkey(self, event):
        """处理键盘事件"""
        if self.recording and event.event_type == keyboard.KEY_DOWN:
            key = event.name
            modifiers = []

            if event.modifiers:
                modifiers = list(event.modifiers)
                if 'windows' in modifiers:
                    modifiers.remove('windows')

            # 组合键处理
            if modifiers:
                key_str = "+".join(modifiers + [key.upper()])
                formatted_key = f"<{key_str}>"
            else:
                formatted_key = f"<{key.upper()}>"

            # 过滤无效按键
            if key.lower() in ['esc', 'tab', 'enter']:
                messagebox.showerror("错误", "不能使用系统保留按键")
                return

            # 更新热键
            self.hotkey = formatted_key
            self.hotkey_label.config(text=f"当前快捷键：{self.hotkey}")
            self.start_btn.config(text=f"开始 ({self.hotkey})")
            self.setup_hotkey()

            # 重置状态
            self.recording = False
            keyboard.unhook_all()
            self.hotkey_btn.config(text="点击设置快捷键")
            self.status.config(text="快捷键已更新")

    def toggle_click(self, event=None):
        if not self.running:
            self.start_click()
        else:
            self.stop_click()

    def start_click(self):
        try:
            interval = float(self.interval.get())
            if interval <= 0:
                raise ValueError
        except ValueError:
            self.status.config(text="错误: 间隔时间必须为数字且大于0")
            return

        self.running = True
        self.start_btn.config(text=f"停止 ({self.hotkey})")
        self.status.config(text=f"状态: 运行中 - 每隔 {interval} 秒点击一次")

        self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
        self.click_thread.start()

    def stop_click(self):
        self.running = False
        self.start_btn.config(text=f"开始 ({self.hotkey})")
        self.status.config(text="状态: 已停止")

    def click_loop(self):
        while self.running:
            try:
                pyautogui.click(button=self.mouse_button.get())
                time.sleep(self.interval.get())
            except Exception as e:
                self.status.config(text=f"错误: {str(e)}")
                self.stop_click()


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-topmost', True)

    # 窗口居中
    window_width = 400
    window_height = 220
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    app = AutoClickerApp(root)
    root.mainloop()