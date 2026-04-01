# strategies/graphic_strategy.py
import tkinter as tk
from typing import Dict, Any
from .display_strategy import DisplayStrategy
from models.pokemon import Pokemon


class GraphicDisplayStrategy(DisplayStrategy):
    """图像显示策略实现"""

    def create_wild_display(self, parent, pokemon: Pokemon) -> Dict[str, Any]:
        """创建野生精灵图像显示"""
        # 先清除父容器中的所有子控件
        for widget in parent.winfo_children():
            widget.destroy()

        frame = tk.Frame(parent, bg='#27ae60')
        frame.pack(expand=True, fill=tk.BOTH)

        # 精灵名字
        name_label = tk.Label(frame, text=f"{pokemon.emoji} {pokemon.name}",
                              font=("微软雅黑", 18, "bold"),
                              bg='#27ae60', fg='#fff')
        name_label.pack(pady=10)

        # Canvas画布绘制精灵
        canvas = tk.Canvas(frame, width=250, height=250, bg='#27ae60',
                           highlightthickness=2, highlightbackground='#fff')
        canvas.pack(pady=10)

        # 绘制精灵图像
        self._draw_pokemon(canvas, pokemon)

        # 信息标签
        info_label = tk.Label(frame, text="",
                              font=("微软雅黑", 11),
                              bg='#27ae60', fg='#fff', justify=tk.LEFT)
        info_label.pack(pady=5)

        # 血量条框架
        hp_frame = tk.Frame(frame, bg='#27ae60')
        hp_frame.pack(pady=10)

        tk.Label(hp_frame, text="HP:", font=("微软雅黑", 12, "bold"),
                 bg='#27ae60', fg='#fff').pack(side=tk.LEFT, padx=5)

        # 血量条画布
        hp_bar_canvas = tk.Canvas(hp_frame, width=200, height=25, bg='#2c3e50',
                                  highlightthickness=1, highlightbackground='#fff')
        hp_bar_canvas.pack(side=tk.LEFT, padx=5)

        # 创建血量矩形
        hp_width = int(200 * (pokemon.hp / pokemon.max_hp))
        hp_rect = hp_bar_canvas.create_rectangle(0, 0, hp_width, 25, fill='#e74c3c')

        hp_text = tk.Label(hp_frame, text=f"{pokemon.hp}/{pokemon.max_hp}",
                           font=("微软雅黑", 10, "bold"), bg='#27ae60', fg='#fff')
        hp_text.pack(side=tk.LEFT, padx=5)

        # 更新信息
        self._update_info(info_label, pokemon)

        return {
            "frame": frame,
            "canvas": canvas,
            "info_label": info_label,
            "hp_bar_canvas": hp_bar_canvas,
            "hp_rect": hp_rect,
            "hp_text": hp_text,
            "pokemon": pokemon
        }

    def update_wild_display(self, display_widgets: Dict[str, Any], pokemon: Pokemon):
        """更新野生精灵显示"""
        if "info_label" in display_widgets:
            self._update_info(display_widgets["info_label"], pokemon)

        if "hp_bar_canvas" in display_widgets and "hp_rect" in display_widgets:
            # 更新血量条
            hp_bar_canvas = display_widgets["hp_bar_canvas"]
            hp_rect = display_widgets["hp_rect"]
            max_width = 200
            hp_width = int(max_width * (pokemon.hp / pokemon.max_hp))
            hp_bar_canvas.coords(hp_rect, 0, 0, hp_width, 25)

            # 根据血量改变颜色
            percentage = pokemon.get_hp_percentage()
            if percentage > 0.5:
                color = '#e74c3c'
            elif percentage > 0.2:
                color = '#f39c12'
            else:
                color = '#c0392b'
            hp_bar_canvas.itemconfig(hp_rect, fill=color)

        if "hp_text" in display_widgets:
            display_widgets["hp_text"].config(text=f"{pokemon.hp}/{pokemon.max_hp}")

        # 更新画布中的精灵（显示受伤效果）
        if "canvas" in display_widgets:
            canvas = display_widgets["canvas"]
            # 重新绘制，显示受伤效果
            self._draw_pokemon(canvas, pokemon)

    def create_pokemon_list_item(self, parent, pokemon: Pokemon, index: int) -> Any:
        """创建精灵列表项"""
        frame = tk.Frame(parent, bg='#34495e')
        frame.pack(fill=tk.X, pady=2)

        # 迷你Canvas显示小图标
        mini_canvas = tk.Canvas(frame, width=30, height=30, bg='#34495e',
                                highlightthickness=0)
        mini_canvas.pack(side=tk.LEFT, padx=5, pady=2)
        self._draw_mini_pokemon(mini_canvas, pokemon)

        # 精灵信息
        hp_percent = int(pokemon.get_hp_percentage() * 100)
        info_label = tk.Label(frame,
                              text=f"{index}. {pokemon.name}  HP: {pokemon.hp}/{pokemon.max_hp} ({hp_percent}%)",
                              font=("微软雅黑", 10),
                              bg='#34495e', fg='#fff',
                              anchor=tk.W)
        info_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        return frame

    def destroy_display(self, display_widgets: Dict[str, Any]):
        """销毁显示"""
        if "frame" in display_widgets:
            display_widgets["frame"].destroy()

    def _draw_pokemon(self, canvas, pokemon):
        """绘制精灵图像"""
        canvas.delete("all")

        # 根据血量调整亮度
        hp_percentage = pokemon.get_hp_percentage()
        if hp_percentage < 0.3:
            # 受伤时添加暗色效果
            color = self._darken_color(pokemon.color, 0.5)
        else:
            color = pokemon.color

        # 根据精灵类型绘制不同图像
        if pokemon.image_type == "mouse":  # 皮卡丘风格
            self._draw_mouse(canvas, color, hp_percentage)
        elif pokemon.image_type == "dragon":  # 小火龙风格
            self._draw_dragon(canvas, color, hp_percentage)
        elif pokemon.image_type == "turtle":  # 杰尼龟风格
            self._draw_turtle(canvas, color, hp_percentage)
        elif pokemon.image_type == "frog":  # 妙蛙种子风格
            self._draw_frog(canvas, color, hp_percentage)
        elif pokemon.image_type == "bird":  # 波波风格
            self._draw_bird(canvas, color, hp_percentage)
        elif pokemon.image_type == "duck":  # 可达鸭风格
            self._draw_duck(canvas, color, hp_percentage)
        else:  # 默认圆形
            self._draw_default(canvas, color, hp_percentage)

        # 如果血量低，显示受伤效果
        if hp_percentage < 0.3:
            # 添加红色闪烁效果
            canvas.create_rectangle(0, 0, 250, 250,
                                    fill='#ff0000', stipple='gray50',
                                    outline='', tags="damage")

    def _draw_mouse(self, canvas, color, hp_percentage):
        """绘制老鼠风格"""
        # 身体
        canvas.create_oval(75, 75, 175, 175, fill=color, outline='#b8860b', width=3)

        # 耳朵
        canvas.create_polygon(85, 55, 105, 35, 125, 55, fill='#000000', outline='#b8860b', width=2)
        canvas.create_polygon(125, 55, 145, 35, 165, 55, fill='#000000', outline='#b8860b', width=2)

        # 眼睛
        canvas.create_oval(100, 105, 120, 125, fill='#ffffff', outline='#000000', width=2)
        canvas.create_oval(130, 105, 150, 125, fill='#ffffff', outline='#000000', width=2)
        canvas.create_oval(108, 112, 115, 119, fill='#000000')
        canvas.create_oval(138, 112, 145, 119, fill='#000000')

        # 腮红（根据血量改变）
        if hp_percentage > 0.5:
            canvas.create_oval(90, 130, 100, 140, fill='#ff9999', outline='')
            canvas.create_oval(150, 130, 160, 140, fill='#ff9999', outline='')

        # 嘴巴
        if hp_percentage > 0.5:
            canvas.create_arc(115, 130, 135, 150, start=0, extent=-180, fill='#000000')
        else:
            canvas.create_line(125, 135, 125, 145, fill='#000000', width=2)

    def _draw_dragon(self, canvas, color, hp_percentage):
        """绘制龙风格"""
        # 身体
        canvas.create_oval(70, 80, 180, 170, fill=color, outline='#8B4513', width=3)

        # 头部装饰
        canvas.create_polygon(125, 55, 110, 70, 140, 70, fill='#ff6b6b')

        # 眼睛
        canvas.create_oval(95, 110, 115, 130, fill='#ffffff', outline='#000000', width=2)
        canvas.create_oval(135, 110, 155, 130, fill='#ffffff', outline='#000000', width=2)
        canvas.create_oval(103, 118, 110, 125, fill='#000000')
        canvas.create_oval(143, 118, 150, 125, fill='#000000')

        # 火焰尾巴（根据血量改变大小）
        flame_size = int(15 * (1 - hp_percentage) + 5)
        for i in range(3):
            canvas.create_polygon(160, 150 + i * 8, 180, 155 + i * 8, 160, 160 + i * 8,
                                  fill='#ff6600', outline='')

    def _draw_turtle(self, canvas, color, hp_percentage):
        """绘制乌龟风格"""
        # 龟壳
        canvas.create_oval(60, 65, 190, 165, fill=color, outline='#2c5e2e', width=4)

        # 龟壳花纹
        canvas.create_line(125, 65, 125, 165, fill='#2c5e2e', width=2)
        canvas.create_line(60, 115, 190, 115, fill='#2c5e2e', width=2)

        # 头部
        canvas.create_oval(155, 80, 185, 110, fill=color)

        # 眼睛
        canvas.create_oval(170, 88, 178, 96, fill='#000000')

        # 脚
        canvas.create_oval(70, 130, 90, 150, fill=color)
        canvas.create_oval(160, 130, 180, 150, fill=color)

    def _draw_frog(self, canvas, color, hp_percentage):
        """绘制青蛙风格"""
        # 身体
        canvas.create_oval(80, 85, 170, 160, fill=color, outline='#2c5e2e', width=3)

        # 大眼睛
        canvas.create_oval(85, 70, 110, 95, fill='#ffffff')
        canvas.create_oval(140, 70, 165, 95, fill='#ffffff')
        canvas.create_oval(95, 78, 103, 86, fill='#000000')
        canvas.create_oval(150, 78, 158, 86, fill='#000000')

        # 种子/植物（根据血量改变大小）
        seed_size = int(15 * (1 - hp_percentage) + 10)
        canvas.create_oval(120, 130, 130 + seed_size, 140 + seed_size,
                           fill='#6b8e23', outline='#2c5e2e')

    def _draw_bird(self, canvas, color, hp_percentage):
        """绘制鸟风格"""
        # 身体
        canvas.create_oval(80, 85, 170, 145, fill=color, outline='#8B4513', width=3)

        # 翅膀
        canvas.create_polygon(125, 105, 85, 95, 100, 115, fill=color)

        # 眼睛
        canvas.create_oval(140, 100, 155, 115, fill='#ffffff')
        canvas.create_oval(146, 106, 151, 111, fill='#000000')

        # 喙
        canvas.create_polygon(155, 108, 170, 108, 162, 115, fill='#ff9900')

    def _draw_duck(self, canvas, color, hp_percentage):
        """绘制鸭子风格"""
        # 身体
        canvas.create_oval(75, 85, 175, 160, fill=color, outline='#8B4513', width=3)

        # 头
        canvas.create_oval(150, 65, 180, 95, fill=color)

        # 眼睛
        canvas.create_oval(165, 75, 172, 82, fill='#000000')

        # 嘴巴
        canvas.create_polygon(175, 80, 190, 78, 183, 84, fill='#ff9900')

        # 眉毛（根据血量改变）
        if hp_percentage < 0.5:
            canvas.create_line(160, 73, 168, 71, fill='#000000', width=2)

    def _draw_default(self, canvas, color, hp_percentage):
        """默认圆形"""
        canvas.create_oval(60, 60, 190, 190, fill=color, outline='#000000', width=4)

        # 眼睛
        canvas.create_oval(95, 105, 115, 125, fill='#ffffff', outline='#000000', width=2)
        canvas.create_oval(135, 105, 155, 125, fill='#ffffff', outline='#000000', width=2)
        canvas.create_oval(102, 112, 109, 119, fill='#000000')
        canvas.create_oval(142, 112, 149, 119, fill='#000000')

        # 嘴巴
        if hp_percentage > 0.5:
            canvas.create_arc(115, 130, 135, 150, start=0, extent=-180, fill='#000000')
        else:
            canvas.create_line(125, 140, 125, 150, fill='#000000', width=2)

    def _draw_mini_pokemon(self, canvas, pokemon):
        """绘制迷你精灵"""
        canvas.delete("all")
        canvas.create_oval(5, 5, 25, 25, fill=pokemon.color, outline='#000000', width=1)
        canvas.create_text(15, 15, text=pokemon.emoji, font=("微软雅黑", 12))

    def _update_info(self, info_label, pokemon):
        """更新信息标签"""
        hp_percent = int(pokemon.get_hp_percentage() * 100)
        info_text = f"属性: {pokemon.element.value}\nHP: {hp_percent}%\n{pokemon.description}"
        info_label.config(text=info_text)

    def _darken_color(self, color, factor):
        """使颜色变暗"""
        # 简单的颜色变暗处理
        color_map = {
            '#FFD700': '#B8860B',  # 金色变暗
            '#FF6B6B': '#CD5C5C',  # 红色变暗
            '#4ECDC4': '#2E8B57',  # 青色变暗
            '#6B8E23': '#556B2F',  # 绿色变暗
            '#D2691E': '#8B4513',  # 棕色变暗
            '#FFE4B5': '#DEB887',  # 米色变暗
            '#8B4513': '#5D3A1A',  # 深棕变暗
            '#D2B48C': '#BC9A6C',  # 卡其变暗
        }
        return color_map.get(color, '#888888')

    def draw_pokemon_to_canvas(self, canvas, pokemon):
        """公开的绘制方法，供其他窗口使用"""
        self._draw_pokemon(canvas, pokemon)