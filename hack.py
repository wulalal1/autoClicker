# autoclicker.py
import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import threading
import time
import sys
import os
from PIL import Image, ImageDraw


# ----------------------
# 资源路径处理
# ----------------------
def resource_path(relative_path):
    """ 处理PyInstaller打包后的资源路径 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ----------------------
# 自动生成图标
# ----------------------
def generate_icon(output_path="autoclicker.ico"):
    """ 如果图标不存在则自动生成 """
    if not os.path.exists(output_path):
        try:
            img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            # 绘制红色圆形图标
            draw.ellipse((50, 50, 206, 206), fill=(220, 20, 60))
            draw.ellipse((60, 60, 196, 196), fill=(255, 255, 255))
            img.save(resource_path(output_path), format='ICO', sizes=[(256, 256), (128, 128), (64, 64)])
        except Exception as e:
            print(f"图标生成失败: {str(e)}")


# ----------------------
# 主应用程序类
# ----------------------
class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("自动连点器 v2.2")
        self.stop_event = threading.Event()
        self.click_thread = None
        self.hotkey = "<F6>"
        self.recording = False

        # 初始化界面
        self.setup_ui()
        self.setup_icon()
        self.bind_hotkeys()

    # ----------------------
    # 界面初始化
    # ----------------------
    def setup_ui(self):
        """ 创建图形用户界面 """
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill='both', expand=True)

        # 热键设置区域
        hotkey_frame = ttk.LabelFrame(main_frame, text="控制设置", padding=10)
        hotkey_frame.pack(fill='x', pady=5)

        self.hotkey_btn = ttk.Button(
            hotkey_frame,
            text="设置快捷键",
            command=self.start_hotkey_recording
        )
        self.hotkey_btn.pack(side='left')

        self.hotkey_label = ttk.Label(
            hotkey_frame,
            text=f"当前快捷键：{self.hotkey}",
            width=20
        )
        self.hotkey_label.pack(side='left', padx=10)

        # 参数设置区域
        setting_frame = ttk.Frame(main_frame)
        setting_frame.pack(fill='x', pady=5)

        ttk.Label(setting_frame, text="点击间隔（秒）:").pack(side='left')
        self.interval = tk.DoubleVar(value=0.1)
        ttk.Entry(setting_frame, textvariable=self.interval, width=8).pack(side='left', padx=5)

        ttk.Label(setting_frame, text="鼠标按钮:").pack(side='left', padx=(10, 0))
        self.mouse_button = tk.StringVar(value='left')
        ttk.Combobox(
            setting_frame,
            textvariable=self.mouse_button,
            values=['left', 'right', 'middle'],
            state='readonly',
            width=8
        ).pack(side='left')

        # 控制按钮区域
        ctrl_frame = ttk.Frame(main_frame)
        ctrl_frame.pack(fill='x', pady=10)

        self.start_btn = ttk.Button(
            ctrl_frame,
            text="开始 (F6)",
            command=self.toggle_click
        )
        self.start_btn.pack(side='left')

        self.stop_btn = ttk.Button(
            ctrl_frame,
            text="强制停止",
            command=self.force_stop,
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=5)

        ttk.Button(
            ctrl_frame,
            text="退出",
            command=self.root.quit
        ).pack(side='right')

        # 状态栏
        self.status = ttk.Label(
            self.root,
            text="状态: 就绪",
            relief='sunken',
            padding=(5, 2)
        )
        self.status.pack(fill='x', padx=10, pady=5)

    # ----------------------
    # 图标处理
    # ----------------------
    def setup_icon(self):
        """ 初始化程序图标 """
        generate_icon()
        try:
            self.root.iconbitmap(resource_path("autoclicker.ico"))
        except Exception as e:
            print(f"图标加载失败: {str(e)}")

    # ----------------------
    # 热键功能
    # ----------------------
    def bind_hotkeys(self):
        """ 绑定热键事件 """
        self.root.unbind(self.hotkey)
        self.root.bind(self.hotkey, self.toggle_click)

    def start_hotkey_recording(self):
        """ 开始录制新快捷键 """
        import keyboard
        self.recording = True
        self.hotkey_btn.config(text="按下新快捷键...")
        self.status.config(text="状态: 正在录制快捷键...")
        keyboard.hook(self.process_hotkey)

    def process_hotkey(self, event):
        """ 处理键盘事件 """
        if self.recording and event.event_type == 'down':
            import keyboard
            key = keyboard.normalize_name(event.name)
            modifiers = event.modifiers

            # 过滤无效按键
            if key in ['esc', 'tab', 'enter']:
                messagebox.showerror("错误", "不能使用系统保留按键")
                return

            # 构建组合键
            combo = []
            if modifiers:
                combo += modifiers
            combo.append(key)
            self.hotkey = f"<{'+'.join(combo).lower()}>"

            # 更新界面
            self.hotkey_label.config(text=f"当前快捷键：{self.hotkey}")
            self.bind_hotkeys()

            # 重置状态
            self.recording = False
            keyboard.unhook_all()
            self.hotkey_btn.config(text="设置快捷键")
            self.status.config(text="快捷键已更新")

    # ----------------------
    # 点击控制逻辑
    # ----------------------
    def toggle_click(self, event=None):
        """ 切换点击状态 """
        if not self.stop_event.is_set():
            self.start_click()
        else:
            self.stop_click()

    def start_click(self):
        """ 启动点击线程 """
        try:
            interval = float(self.interval.get())
            if interval <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("输入错误", "间隔时间必须为大于0的数字")
            return

        # 清理旧线程
        if self.click_thread and self.click_thread.is_alive():
            self.click_thread.join()

        self.stop_event.clear()
        self.update_ui_state(running=True)
        self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
        self.click_thread.start()

    def force_stop(self):
        """ 强制停止点击 """
        self.stop_event.set()
        if self.click_thread.is_alive():
            self.click_thread.join(timeout=0.5)
        self.update_ui_state(running=False)

    def stop_click(self):
        """ 正常停止点击 """
        self.stop_event.set()
        self.update_ui_state(running=False)

    def update_ui_state(self, running):
        """ 更新界面状态 """
        state = 'disabled' if running else 'enabled'
        self.root.after(0, lambda: [
            self.start_btn.config(
                state=state,
                text=f"停止 ({self.hotkey})" if running else f"开始 ({self.hotkey})"
            ),
            self.stop_btn.config(state='disabled' if not running else 'enabled'),
            self.status.config(
                text=f"状态: 运行中 - {self.interval.get()}秒/次" if running
                else "状态: 已停止"
            )
        ])

    def click_loop(self):
        """ 点击循环核心逻辑 """
        try:
            while not self.stop_event.is_set():
                pyautogui.click(button=self.mouse_button.get())

                # 拆分等待以便快速响应停止
                wait_time = self.interval.get()
                for _ in range(10):
                    if self.stop_event.is_set():
                        return
                    time.sleep(wait_time / 10)
        except Exception as e:
            self.stop_event.set()
            self.root.after(0, lambda: messagebox.showerror("运行时错误", str(e)))


# ----------------------
# 程序入口
# ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-topmost', True)

    # 窗口居中
    window_width = 400
    window_height = 220
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{window_width}x{window_height}+"
                  f"{(screen_width // 2 - window_width // 2)}+"
                  f"{(screen_height // 2 - window_height // 2)}")

    app = AutoClickerApp(root)
    root.mainloop()