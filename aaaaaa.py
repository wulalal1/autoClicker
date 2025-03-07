from PIL import Image, ImageDraw
import os


def generate_icon(output_path="icon.ico"):
    # 创建 256x256 的透明背景图像
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 绘制圆形按钮样式
    draw.ellipse((50, 50, 206, 206), fill=(66, 133, 244))  # Google蓝色
    draw.ellipse((60, 60, 196, 196), fill=(255, 255, 255))

    # 保存为多尺寸ICO文件
    img.save(output_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])


if __name__ == "__main__":
    if not os.path.exists("icon.ico"):
        generate_icon()
        print("图标文件已生成：icon.ico")
    else:
        print("图标文件已存在")