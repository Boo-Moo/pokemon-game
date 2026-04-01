# views/map_view.py
import tkinter as tk
from tkinter import messagebox
from typing import Callable
from models.map import GameMap, TerrainType


class MapView(tk.Toplevel):
    """地图界面"""

    def __init__(self, parent, game_map: GameMap, on_location_selected: Callable):
        super().__init__(parent)
        self.parent = parent
        self.game_map = game_map
        self.on_location_selected = on_location_selected
        self.selected_location = None

        self.title("世界地图")
        self.geometry("800x600")
        self.configure(bg='#2ecc71')

        self.setup_ui()
        self.update_map_display()

    def setup_ui(self):
        """设置界面"""
        # 标题
        title_frame = tk.Frame(self, bg='#2ecc71')
        title_frame.pack(fill=tk.X, pady=10)

        tk.Label(title_frame, text="🗺️ 世界地图", font=("微软雅黑", 20, "bold"),
                 bg='#2ecc71', fg='#fff').pack()

        # 当前地点信息
        self.location_info = tk.Label(title_frame, text="", font=("微软雅黑", 12),
                                      bg='#2ecc71', fg='#ffd700')
        self.location_info.pack(pady=5)

        # 主要内容区域
        main_frame = tk.Frame(self, bg='#2ecc71')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 左侧 - 地图显示
        left_frame = tk.Frame(main_frame, bg='#27ae60', relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(left_frame, text="地图区域", font=("微软雅黑", 14, "bold"),
                 bg='#27ae60', fg='#fff').pack(pady=5)

        self.map_canvas = tk.Canvas(left_frame, width=400, height=450,
                                    bg='#2c3e50', highlightthickness=0)
        self.map_canvas.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.map_canvas.bind("<Button-1>", self.on_map_click)

        # 右侧 - 地点信息
        right_frame = tk.Frame(main_frame, bg='#27ae60', relief=tk.RAISED, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(right_frame, text="地点详情", font=("微软雅黑", 14, "bold"),
                 bg='#27ae60', fg='#fff').pack(pady=5)

        # 地点信息文本
        self.info_text = tk.Text(right_frame, height=15, width=30,
                                 font=("微软雅黑", 10), bg='#34495e',
                                 fg='#fff', wrap=tk.WORD, padx=10, pady=10)
        self.info_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # 按钮区域
        button_frame = tk.Frame(right_frame, bg='#27ae60')
        button_frame.pack(pady=10)

        self.move_btn = tk.Button(button_frame, text="🚶 前往此地", font=("微软雅黑", 12),
                                  bg='#3498db', fg='#fff', padx=20, pady=8,
                                  command=self.move_to_location, state=tk.DISABLED)
        self.move_btn.pack(side=tk.LEFT, padx=5)

        close_btn = tk.Button(button_frame, text="关闭", font=("微软雅黑", 12),
                              bg='#e74c3c', fg='#fff', padx=20, pady=8,
                              command=self.destroy)
        close_btn.pack(side=tk.LEFT, padx=5)

        # 底部提示
        tip_label = tk.Label(self, text="💡 点击地图上的地点查看详情，然后选择前往",
                             font=("微软雅黑", 9), bg='#2ecc71', fg='#fff')
        tip_label.pack(pady=5)

    def update_map_display(self):
        """更新地图显示"""
        self.map_canvas.delete("all")

        # 定义地点坐标（固定布局）
        locations_coords = {
            "初始小镇": (100, 80),
            "森林入口": (300, 80),
            "幽暗洞穴": (500, 80),
            "火焰山脉": (700, 80),
            "湖泊": (100, 250),
            "古代遗迹": (300, 250),
            "冰霜雪原": (500, 250),
            "天空之塔": (700, 250),
            "精灵之森": (200, 400),
            "神秘洞窟": (500, 400)
        }

        # 地形颜色映射
        terrain_colors = {
            TerrainType.GRASS: "#6B8E23",
            TerrainType.FOREST: "#228B22",
            TerrainType.MOUNTAIN: "#8B4513",
            TerrainType.WATER: "#4682B4",
            TerrainType.CAVE: "#696969",
            TerrainType.TOWN: "#CD853F",
            TerrainType.ROAD: "#DEB887"
        }

        # 绘制连接线
        for from_loc, to_locs in self.game_map.connections.items():
            if from_loc in locations_coords:
                x1, y1 = locations_coords[from_loc]
                for to_loc in to_locs:
                    if to_loc in locations_coords:
                        x2, y2 = locations_coords[to_loc]
                        self.map_canvas.create_line(x1, y1, x2, y2,
                                                    fill='#95a5a6', width=2,
                                                    dash=(5, 3))

        # 绘制地点
        self.location_buttons = {}
        for loc_name, (x, y) in locations_coords.items():
            location = self.game_map.locations.get(loc_name)
            if location:
                # 获取地形颜色
                color = terrain_colors.get(location.terrain, "#95a5a6")

                # 判断是否已访问
                outline_color = "#FFD700" if location.visited else "#FFFFFF"
                outline_width = 3 if location.visited else 2

                # 绘制地点圆圈
                self.map_canvas.create_oval(x - 20, y - 20, x + 20, y + 20,
                                            fill=color, outline=outline_color,
                                            width=outline_width)

                # 绘制地形图标
                self.map_canvas.create_text(x, y, text=location.terrain.value,
                                            font=("微软雅黑", 16))

                # 绘制地点名称
                self.map_canvas.create_text(x, y + 25, text=loc_name,
                                            font=("微软雅黑", 9),
                                            fill='#fff')

                # 存储位置信息用于点击检测
                self.location_buttons[loc_name] = (x, y)

        # 标记当前位置
        if self.game_map.current_location:
            current = self.game_map.current_location
            if current in locations_coords:
                x, y = locations_coords[current]
                self.map_canvas.create_oval(x - 25, y - 25, x + 25, y + 25,
                                            outline='#FFD700', width=3,
                                            dash=(5, 2))
                self.map_canvas.create_text(x, y - 30, text="📍 当前位置",
                                            font=("微软雅黑", 8),
                                            fill='#FFD700')

        # 更新当前地点信息
        current = self.game_map.get_current_location()
        if current:
            self.location_info.config(text=f"当前位置：{current.terrain.value} {current.name}")
        else:
            self.location_info.config(text="未选择地点")

    def on_map_click(self, event):
        """处理地图点击"""
        # 查找点击的地点
        for loc_name, (x, y) in self.location_buttons.items():
            distance = ((event.x - x) ** 2 + (event.y - y) ** 2) ** 0.5
            if distance <= 30:
                self.selected_location = loc_name
                self.show_location_info(loc_name)
                break

    def show_location_info(self, loc_name: str):
        """显示地点信息"""
        location = self.game_map.locations.get(loc_name)
        if not location:
            return

        # 更新信息文本
        self.info_text.delete(1.0, tk.END)

        info = f"""
【{location.terrain.value} {location.name}】
━━━━━━━━━━━━━━━━━━━━━━

📝 描述：
{location.description}

🌍 地形类型：{location.terrain.value} {location.terrain.name}

✨ 稀有精灵出现率：{int(location.rare_pokemon_rate * 100)}%

📊 访问状态：{"✓ 已探索" if location.visited else "○ 未探索"}

🐾 可遇见的精灵：
"""

        if location.pokemon_spawns:
            for spawn in sorted(location.pokemon_spawns, key=lambda x: x['rate'], reverse=True):
                info += f"  • {spawn['name']} ({int(spawn['rate'] * 100)}%)\n"
        else:
            info += "  • 暂无数据\n"

        info += f"""
🚶 可前往的地点：
"""

        available = self.game_map.get_available_locations(loc_name)
        if available:
            for loc in available:
                loc_obj = self.game_map.locations.get(loc)
                if loc_obj:
                    visited_mark = "✓" if loc_obj.visited else "○"
                    info += f"  • {visited_mark} {loc_obj.terrain.value} {loc}\n"
        else:
            info += "  • 暂无连接\n"

        self.info_text.insert(1.0, info)

        # 检查是否可以前往
        current = self.game_map.current_location
        can_move = (current and loc_name in self.game_map.get_available_locations(current))

        if can_move:
            self.move_btn.config(state=tk.NORMAL, text=f"🚶 前往{location.name}")
        else:
            self.move_btn.config(state=tk.DISABLED, text="🚫 无法前往")

    def move_to_location(self):
        """移动到选定地点"""
        if self.selected_location:
            current = self.game_map.current_location
            if current and self.selected_location in self.game_map.get_available_locations(current):
                self.game_map.move_to(self.selected_location)
                self.on_location_selected(self.selected_location)
                self.update_map_display()
                messagebox.showinfo("移动成功", f"你已到达 {self.selected_location}！")
                self.destroy()
            else:
                messagebox.showwarning("无法移动", "无法直接前往该地点，请选择相邻的地点！")