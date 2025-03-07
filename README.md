# autoClicker
鼠标连点器
基于 Python 的自动化鼠标点击工具，支持：
- 自定义点击间隔
- 多线程处理
- 全局热键控制
- 实时状态显示
## 功能特性

### 基础功能
- 🕹 **精准点击控制**
  - 可调节点击间隔 (0.1秒~60秒)
  - 支持左键/右键/中键选择
  - 点击位置跟随当前鼠标指针

### 快捷键功能
- ⌨ **自定义热键绑定**
  - 默认启动/停止快捷键：F6
  - 支持组合键设置 (Ctrl/Alt/Shift + 任意键)
  - 实时热键冲突检测

### 可视化界面
- 📊 **实时状态监控**
  - 运行状态指示灯
  - 点击次数统计 (需代码扩展)
  - 错误提示弹窗
  - 窗口置顶显示

### 高级功能
- 🖼 **自动图标生成**
  - 缺少图标时自动创建
  - 支持自定义ICO文件
- 🌐 **多平台兼容**
  - Windows打包exe
  - macOS/Linux可源码运行

### 如何运行
-打开dist->运行hack.exe
##操作步骤
    -基本设置
    -操作	说明
    -输入框	输入点击间隔（建议≥0.1秒）
    -下拉菜单	选择鼠标按键

### 开发者操作
-git clone https://github.com/wulalal1/autoClicker.git
### 安装依赖
-pip install pyautogui tkinter keyboard
### 运行
-python hack.py
### 图标显示异常
手动指定图标路径
-python hack.py --icon custom_icon.ico
