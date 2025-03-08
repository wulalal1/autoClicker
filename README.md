# AutoClicker - 智能鼠标连点器

## 🚀 功能特性

### 核心功能
- **精准点击控制**
  - 毫秒级点击间隔 (0.1秒 ~ 60秒)
  - 支持左键/右键/中键三键操作
  - 智能位置追踪 (跟随鼠标实时位置)

- **热键管理系统**
  - 默认热键：<kbd>F6</kbd> 启动/停止
  - 支持组合键绑定 (Ctrl/Alt/Shift + 任意键)
  - 热键冲突实时检测

### 用户界面
- 📊 可视化状态面板
  - 实时运行状态指示灯
  - 点击次数统计 (需代码扩展)
  - 异常错误弹窗提示
  - 窗口置顶显示模式

- 🎨 主题定制
  - 自动图标生成系统
  - 支持自定义 `.ico` 文件
  - 高DPI显示适配

### 跨平台支持
- **Windows**: 提供预编译的便携版 exe
- **macOS/Linux**: 支持源码直接运行
- **兼容性**: Windows 10/11 全版本支持

## 📥 下载与安装

### 普通用户
1. 访问 [Releases 页面](https://github.com/wulalal1/autoClicker/releases)
2. 在 Assets 中下载最新版 "autoClicker.exe"
3. 右键文件 → 属性 → 勾选"解除锁定"
4. 双击运行即可使用

### 开发者
```bash
# 克隆仓库
git clone https://github.com/wulalal1/autoClicker.git

# 安装依赖
# 在PyCharm Terminal中安装依赖
pip install pyinstaller pyautogui pillow keyboard

# 运行程序
python hack.py

# 打包可执行文件
pyinstaller --onefile --noconsole --icon=assets/icon.ico src/hack.py
