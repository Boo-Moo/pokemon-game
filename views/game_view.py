# views/game_view.py
import tkinter as tk
from tkinter import messagebox, ttk
import random
from controllers.game_controller import GameController
from strategies.text_strategy import TextDisplayStrategy
from strategies.graphic_strategy import GraphicDisplayStrategy


class GameView(tk.Frame):
    """游戏主界面"""

    def __init__(self, parent, controller: GameController):
        super().__init__(parent)
        self.controller = controller
        self.wild_display_widgets = None
        self.pokedex_detail_window = None  # 图鉴详情窗口
        self.setup_ui()
        self.update_stats()

    def setup_ui(self):
        """设置界面"""
        self.configure(bg='#2ecc71')

        # 顶部状态栏
        self.setup_status_bar()

        # 主要内容区域
        main_frame = tk.Frame(self, bg='#2ecc71')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧 - 野生精灵区域
        self.setup_wild_area(main_frame)

        # 右侧 - 精灵图鉴区域
        self.setup_pokedex_area(main_frame)

        # 底部按钮栏
        self.setup_bottom_buttons()

        # 消息区域
        self.setup_message_area()

    def setup_status_bar(self):
        """设置状态栏"""
        status_frame = tk.Frame(self, bg='#27ae60', height=80)
        status_frame.pack(fill=tk.X, padx=10, pady=5)

        # 第一行：玩家信息
        info_frame = tk.Frame(status_frame, bg='#27ae60')
        info_frame.pack(fill=tk.X, pady=5)

        self.name_label = tk.Label(info_frame, text="",
                                   font=("微软雅黑", 12, "bold"),
                                   bg='#27ae60', fg='#fff')
        self.name_label.pack(side=tk.LEFT, padx=20)

        self.score_label = tk.Label(info_frame, text="分数：0",
                                    font=("微软雅黑", 12, "bold"),
                                    bg='#27ae60', fg='#ffd700')
        self.score_label.pack(side=tk.LEFT, padx=20)

        self.balls_label = tk.Label(info_frame, text="精灵球：0",
                                    font=("微软雅黑", 12, "bold"),
                                    bg='#27ae60', fg='#fff')
        self.balls_label.pack(side=tk.LEFT, padx=20)

        self.pokemon_count_label = tk.Label(info_frame, text="图鉴：0只",
                                            font=("微软雅黑", 12, "bold"),
                                            bg='#27ae60', fg='#fff')
        self.pokemon_count_label.pack(side=tk.LEFT, padx=20)

        # 第二行：地点信息
        location_frame = tk.Frame(status_frame, bg='#27ae60')
        location_frame.pack(fill=tk.X, pady=5)

        self.location_label = tk.Label(location_frame, text="",
                                       font=("微软雅黑", 11),
                                       bg='#27ae60', fg='#ffd700')
        self.location_label.pack(side=tk.LEFT, padx=20)

        self.location_desc_label = tk.Label(location_frame, text="",
                                            font=("微软雅黑", 9),
                                            bg='#27ae60', fg='#bdc3c7')
        self.location_desc_label.pack(side=tk.LEFT, padx=20)

    def setup_wild_area(self, parent):
        """设置野生精灵区域"""
        left_frame = tk.Frame(parent, bg='#27ae60', relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(left_frame, text="🌲 野外区域", font=("微软雅黑", 16, "bold"),
                 bg='#27ae60', fg='#fff').pack(pady=10)

        # 野生精灵显示容器
        self.wild_container = tk.Frame(left_frame, bg='#27ae60')
        self.wild_container.pack(expand=True, pady=20)

        # 初始显示
        self.wild_placeholder = tk.Label(self.wild_container,
                                         text="✨ 点击下方按钮进入草丛 ✨",
                                         font=("微软雅黑", 14),
                                         bg='#27ae60', fg='#f1c40f')
        self.wild_placeholder.pack(expand=True)

        # 战斗按钮区域
        battle_frame = tk.Frame(left_frame, bg='#27ae60')
        battle_frame.pack(pady=20)

        self.attack_btn = tk.Button(battle_frame, text="⚔️ 攻击", font=("微软雅黑", 12),
                                    bg='#e74c3c', fg='#fff', padx=20, pady=10,
                                    command=self.attack_pokemon, state=tk.DISABLED)
        self.attack_btn.pack(side=tk.LEFT, padx=10)

        self.catch_btn = tk.Button(battle_frame, text="🎾 扔精灵球", font=("微软雅黑", 12),
                                   bg='#3498db', fg='#fff', padx=20, pady=10,
                                   command=self.catch_pokemon, state=tk.DISABLED)
        self.catch_btn.pack(side=tk.LEFT, padx=10)

        self.run_btn = tk.Button(battle_frame, text="🏃 逃跑", font=("微软雅黑", 12),
                                 bg='#95a5a6', fg='#fff', padx=20, pady=10,
                                 command=self.run_away, state=tk.DISABLED)
        self.run_btn.pack(side=tk.LEFT, padx=10)

    def setup_pokedex_area(self, parent):
        """设置精灵图鉴区域"""
        right_frame = tk.Frame(parent, bg='#27ae60', relief=tk.RAISED, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 图鉴标题栏
        title_frame = tk.Frame(right_frame, bg='#27ae60')
        title_frame.pack(fill=tk.X, pady=10)

        tk.Label(title_frame, text="📖 精灵图鉴", font=("微软雅黑", 16, "bold"),
                 bg='#27ae60', fg='#fff').pack(side=tk.LEFT)

        # 统计信息
        self.pokedex_stats = tk.Label(title_frame, text="", font=("微软雅黑", 10),
                                      bg='#27ae60', fg='#ffd700')
        self.pokedex_stats.pack(side=tk.RIGHT, padx=10)

        # 图鉴列表框架
        list_frame = tk.Frame(right_frame, bg='#2c3e50')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建带滚动条的列表
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.pokemon_listbox = tk.Listbox(list_frame, font=("微软雅黑", 11),
                                          yscrollcommand=scrollbar.set,
                                          height=12, bg='#34495e', fg='#fff',
                                          selectmode=tk.SINGLE,
                                          selectbackground='#3498db')
        self.pokemon_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.pokemon_listbox.yview)

        # 绑定点击事件
        self.pokemon_listbox.bind('<<ListboxSelect>>', self.on_pokemon_selected)
        self.pokemon_listbox.bind('<Double-Button-1>', self.on_pokemon_double_click)

        # 提示标签
        tip_label = tk.Label(right_frame, text="💡 单击查看详情 | 双击查看完整信息",
                             font=("微软雅黑", 9), bg='#27ae60', fg='#fff')
        tip_label.pack(pady=5)

    def setup_bottom_buttons(self):
        """设置底部按钮"""
        bottom_frame = tk.Frame(self, bg='#27ae60')
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)

        # 添加地图按钮
        map_btn = tk.Button(bottom_frame, text="🗺️ 世界地图", font=("微软雅黑", 12, "bold"),
                            bg='#9b59b6', fg='#fff', padx=30, pady=10,
                            command=self.open_map, cursor="hand2")
        map_btn.pack(side=tk.LEFT, padx=10)

        enter_btn = tk.Button(bottom_frame, text="🌿 进入草丛", font=("微软雅黑", 12, "bold"),
                              bg='#f39c12', fg='#fff', padx=30, pady=10,
                              command=self.enter_grass, cursor="hand2")
        enter_btn.pack(side=tk.LEFT, padx=10)

        shop_btn = tk.Button(bottom_frame, text="🛒 商店 (10分/球)", font=("微软雅黑", 12),
                             bg='#1abc9c', fg='#fff', padx=20, pady=10,
                             command=self.open_shop, cursor="hand2")
        shop_btn.pack(side=tk.LEFT, padx=10)

        # 显示模式切换按钮
        mode_btn = tk.Button(bottom_frame, text="🎨 切换显示模式", font=("微软雅黑", 12),
                             bg='#9b59b6', fg='#fff', padx=20, pady=10,
                             command=self.switch_display_mode, cursor="hand2")
        mode_btn.pack(side=tk.LEFT, padx=10)

        # 图鉴详情按钮
        detail_btn = tk.Button(bottom_frame, text="📊 图鉴统计", font=("微软雅黑", 12),
                               bg='#3498db', fg='#fff', padx=20, pady=10,
                               command=self.show_pokedex_stats, cursor="hand2")
        detail_btn.pack(side=tk.LEFT, padx=10)

        reset_btn = tk.Button(bottom_frame, text="🔄 重新开始", font=("微软雅黑", 12),
                              bg='#e67e22', fg='#fff', padx=20, pady=10,
                              command=self.reset_game, cursor="hand2")
        reset_btn.pack(side=tk.LEFT, padx=10)

        exit_btn = tk.Button(bottom_frame, text="🚪 退出游戏", font=("微软雅黑", 12),
                             bg='#c0392b', fg='#fff', padx=20, pady=10,
                             command=self.exit_game, cursor="hand2")
        exit_btn.pack(side=tk.RIGHT, padx=10)

    def setup_message_area(self):
        """设置消息区域"""
        # 创建消息框架
        message_frame = tk.Frame(self, bg='#2c3e50')
        message_frame.pack(fill=tk.X, padx=10, pady=5)

        # 消息标签
        tk.Label(message_frame, text="📝 消息记录", font=("微软雅黑", 10, "bold"),
                 bg='#2c3e50', fg='#ffd700').pack(anchor=tk.W, padx=5, pady=2)

        # 消息文本框
        self.message_text = tk.Text(message_frame, height=6, font=("微软雅黑", 9),
                                    bg='#34495e', fg='#fff', wrap=tk.WORD,
                                    padx=10, pady=5)
        self.message_text.pack(fill=tk.X, padx=5, pady=5)

        # 添加滚动条
        message_scrollbar = tk.Scrollbar(self.message_text)
        message_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_text.config(yscrollcommand=message_scrollbar.set)
        message_scrollbar.config(command=self.message_text.yview)

    def add_message(self, message):
        """添加消息到消息区域"""
        if hasattr(self, 'message_text'):
            self.message_text.insert(tk.END, f"{message}\n")
            self.message_text.see(tk.END)
            # 自动滚动到底部
            self.message_text.yview_moveto(1)

    def update_stats(self):
        """更新状态栏"""
        state = self.controller.get_game_state()
        self.name_label.config(text=f"训练家：{state['player_name']}")
        self.score_label.config(text=f"分数：{state['score']}")
        self.balls_label.config(text=f"精灵球：{state['poke_balls']}")

        # 更新地点信息
        current_loc = state.get('current_location', '未知')
        loc_desc = state.get('location_description', '')
        self.location_label.config(text=f"📍 当前位置：{current_loc}")
        self.location_desc_label.config(text=f"📝 {loc_desc[:50]}...")

        # 更新图鉴列表
        if self.controller.player:
            pokemon_count = state['pokemon_count']
            self.pokemon_count_label.config(text=f"图鉴：{pokemon_count}只")

            # 更新统计信息
            unique_count = self.controller.player.get_unique_pokemon_count()
            self.pokedex_stats.config(text=f"已收集: {pokemon_count}只 | 种类: {unique_count}种")

            # 更新列表
            self.update_pokedex_list()

    def update_pokedex_list(self):
        """更新图鉴列表"""
        self.pokemon_listbox.delete(0, tk.END)

        if self.controller.player:
            # 按名称排序
            sorted_pokemons = sorted(self.controller.player.pokemons, key=lambda p: p.name)

            for i, pokemon in enumerate(sorted_pokemons, 1):
                hp_percent = int(pokemon.get_hp_percentage() * 100)
                # 根据血量显示不同颜色标记
                if hp_percent > 70:
                    status = "💚"
                elif hp_percent > 30:
                    status = "💛"
                else:
                    status = "❤️"

                display_text = f"{status} {i:2d}. {pokemon.emoji} {pokemon.name}  HP: {pokemon.hp}/{pokemon.max_hp} ({hp_percent}%)"
                self.pokemon_listbox.insert(tk.END, display_text)

                # 根据属性设置不同背景色（可选）
                if pokemon.element.value == "火":
                    self.pokemon_listbox.itemconfig(i - 1, bg='#8B4513')
                elif pokemon.element.value == "水":
                    self.pokemon_listbox.itemconfig(i - 1, bg='#2980B9')
                elif pokemon.element.value == "草":
                    self.pokemon_listbox.itemconfig(i - 1, bg='#27AE60')
                elif pokemon.element.value == "电":
                    self.pokemon_listbox.itemconfig(i - 1, bg='#F39C12')

    def on_pokemon_selected(self, event):
        """图鉴项目被选中"""
        selection = self.pokemon_listbox.curselection()
        if selection and self.controller.player:
            index = selection[0]
            sorted_pokemons = sorted(self.controller.player.pokemons, key=lambda p: p.name)
            if index < len(sorted_pokemons):
                pokemon = sorted_pokemons[index]
                self.show_pokemon_preview(pokemon)

    def on_pokemon_double_click(self, event):
        """双击图鉴项目显示详细信息"""
        selection = self.pokemon_listbox.curselection()
        if selection and self.controller.player:
            index = selection[0]
            sorted_pokemons = sorted(self.controller.player.pokemons, key=lambda p: p.name)
            if index < len(sorted_pokemons):
                pokemon = sorted_pokemons[index]
                self.show_pokemon_detail(pokemon)

    def show_pokemon_preview(self, pokemon):
        """显示精灵预览（在消息区域）"""
        hp_percent = int(pokemon.get_hp_percentage() * 100)
        preview_text = f"""
        📖 精灵预览 - {pokemon.emoji} {pokemon.name}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        属性: {pokemon.element.value}
        HP: {pokemon.hp}/{pokemon.max_hp} ({hp_percent}%)
        攻击力: {pokemon.attack}
        稀有度: {int(pokemon.catch_rate * 100)}%
        描述: {pokemon.description}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        💡 双击查看详细信息
        """
        self.add_message(preview_text)

    def show_pokemon_detail(self, pokemon):
        """显示精灵详细信息的弹出窗口"""
        # 如果已经有详情窗口，先关闭
        if self.pokedex_detail_window and self.pokedex_detail_window.winfo_exists():
            self.pokedex_detail_window.destroy()

        # 创建详情窗口
        self.pokedex_detail_window = tk.Toplevel(self)
        self.pokedex_detail_window.title(f"{pokemon.emoji} {pokemon.name} - 详细资料")
        self.pokedex_detail_window.geometry("500x600")
        self.pokedex_detail_window.configure(bg='#2ecc71')

        # 主框架
        main_frame = tk.Frame(self.pokedex_detail_window, bg='#27ae60', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 精灵名称和表情
        name_frame = tk.Frame(main_frame, bg='#27ae60')
        name_frame.pack(pady=10)

        name_label = tk.Label(name_frame, text=f"{pokemon.emoji} {pokemon.name}",
                              font=("微软雅黑", 24, "bold"),
                              bg='#27ae60', fg='#fff')
        name_label.pack()

        # 精灵图像显示
        image_frame = tk.Frame(main_frame, bg='#27ae60')
        image_frame.pack(pady=10)

        # 创建Canvas绘制精灵大图
        canvas = tk.Canvas(image_frame, width=250, height=250, bg='#27ae60',
                           highlightthickness=2, highlightbackground='#fff')
        canvas.pack()

        # 绘制精灵图像
        self._draw_pokemon_detail(canvas, pokemon)

        # 属性标签
        element_frame = tk.Frame(main_frame, bg='#27ae60')
        element_frame.pack(pady=10)

        element_colors = {
            "火": "#e74c3c",
            "水": "#3498db",
            "草": "#2ecc71",
            "电": "#f1c40f",
            "飞行": "#95a5a6",
            "一般": "#bdc3c7"
        }
        element_color = element_colors.get(pokemon.element.value, "#95a5a6")

        element_label = tk.Label(element_frame, text=f"★ {pokemon.element.value}系 ★",
                                 font=("微软雅黑", 14, "bold"),
                                 bg=element_color, fg='#fff', padx=20, pady=5)
        element_label.pack()

        # 详细信息框架
        info_frame = tk.Frame(main_frame, bg='#2c3e50', padx=20, pady=15)
        info_frame.pack(fill=tk.X, pady=10)

        # 能力值
        stats = [
            ("❤️ 生命值", f"{pokemon.hp}/{pokemon.max_hp}"),
            ("⚔️ 攻击力", str(pokemon.attack)),
            ("🎯 捕捉率", f"{int(pokemon.catch_rate * 100)}%"),
            ("📊 当前HP比例", f"{int(pokemon.get_hp_percentage() * 100)}%")
        ]

        for i, (stat_name, stat_value) in enumerate(stats):
            stat_frame = tk.Frame(info_frame, bg='#2c3e50')
            stat_frame.pack(fill=tk.X, pady=5)

            tk.Label(stat_frame, text=stat_name, font=("微软雅黑", 12, "bold"),
                     bg='#2c3e50', fg='#ffd700', width=12, anchor=tk.W).pack(side=tk.LEFT)

            tk.Label(stat_frame, text=stat_value, font=("微软雅黑", 12),
                     bg='#2c3e50', fg='#fff').pack(side=tk.LEFT, padx=10)

            # 如果是HP，显示血量条
            if "生命值" in stat_name:
                hp_bar_canvas = tk.Canvas(stat_frame, width=150, height=20,
                                          bg='#34495e', highlightthickness=0)
                hp_bar_canvas.pack(side=tk.LEFT, padx=5)
                hp_width = int(150 * pokemon.get_hp_percentage())
                hp_bar_canvas.create_rectangle(0, 0, hp_width, 20, fill='#e74c3c')

        # 描述
        desc_frame = tk.Frame(main_frame, bg='#27ae60')
        desc_frame.pack(fill=tk.X, pady=10)

        tk.Label(desc_frame, text="📝 精灵描述", font=("微软雅黑", 12, "bold"),
                 bg='#27ae60', fg='#fff').pack(anchor=tk.W)

        desc_text = tk.Text(desc_frame, height=5, font=("微软雅黑", 10),
                            bg='#34495e', fg='#fff', wrap=tk.WORD, padx=10, pady=10)
        desc_text.pack(fill=tk.X, pady=5)
        desc_text.insert(tk.END, pokemon.description)
        desc_text.config(state=tk.DISABLED)

        # 按钮框架
        button_frame = tk.Frame(main_frame, bg='#27ae60')
        button_frame.pack(pady=15)

        close_btn = tk.Button(button_frame, text="关闭", font=("微软雅黑", 12),
                              bg='#e74c3c', fg='#fff', padx=30, pady=8,
                              command=self.pokedex_detail_window.destroy)
        close_btn.pack(side=tk.LEFT, padx=10)

        # 如果是战斗中，可以添加治疗按钮
        if self.controller.current_battle and self.controller.current_battle.wild_pokemon:
            if pokemon.name == self.controller.current_battle.wild_pokemon.name:
                heal_btn = tk.Button(button_frame, text="💊 治疗", font=("微软雅黑", 12),
                                     bg='#2ecc71', fg='#fff', padx=20, pady=8,
                                     command=lambda: self.heal_pokemon(pokemon))
                heal_btn.pack(side=tk.LEFT, padx=10)

    def open_map(self):
        """打开世界地图"""
        from views.map_view import MapView

        def on_location_selected(location_name):
            """地点选择回调"""
            if self.controller.move_to_location(location_name):
                self.add_message(f"🗺️ 你来到了 {location_name}！")
                self.update_stats()
            else:
                self.add_message("❌ 无法前往该地点！")

        MapView(self, self.controller.game_map, on_location_selected)
    def _draw_pokemon_detail(self, canvas, pokemon):
        """绘制精灵详情大图"""
        canvas.delete("all")

        # 获取显示策略来绘制
        strategy = self.controller.display_strategy
        if isinstance(strategy, GraphicDisplayStrategy):
            # 使用图形策略的绘制方法
            strategy._draw_pokemon(canvas, pokemon)
        else:
            # 如果是文字模式，绘制一个简单的图形
            self._draw_simple_pokemon(canvas, pokemon)

    def _draw_simple_pokemon(self, canvas, pokemon):
        """绘制简单精灵图形（用于文字模式）"""
        # 绘制圆形身体
        canvas.create_oval(75, 75, 175, 175, fill=pokemon.color, outline='#000000', width=3)

        # 绘制眼睛
        canvas.create_oval(100, 110, 120, 130, fill='#ffffff', outline='#000000')
        canvas.create_oval(130, 110, 150, 130, fill='#ffffff', outline='#000000')
        canvas.create_oval(108, 118, 115, 125, fill='#000000')
        canvas.create_oval(138, 118, 145, 125, fill='#000000')

        # 绘制表情
        hp_percent = pokemon.get_hp_percentage()
        if hp_percent > 0.5:
            canvas.create_arc(115, 135, 135, 155, start=0, extent=-180, fill='#000000')
        elif hp_percent > 0.2:
            canvas.create_line(125, 140, 125, 150, fill='#000000', width=2)
        else:
            canvas.create_line(120, 140, 130, 150, fill='#000000', width=2)
            canvas.create_line(130, 140, 120, 150, fill='#000000', width=2)

        # 添加精灵表情符号
        canvas.create_text(125, 50, text=pokemon.emoji, font=("微软雅黑", 30))

        # 添加名字
        canvas.create_text(125, 210, text=pokemon.name, font=("微软雅黑", 14, "bold"),
                           fill='#fff')

    def show_pokedex_stats(self):
        """显示图鉴统计信息"""
        if not self.controller.player:
            return

        stats_window = tk.Toplevel(self)
        stats_window.title("图鉴统计")
        stats_window.geometry("400x500")
        stats_window.configure(bg='#2ecc71')

        main_frame = tk.Frame(stats_window, bg='#27ae60', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        tk.Label(main_frame, text="📊 图鉴统计", font=("微软雅黑", 20, "bold"),
                 bg='#27ae60', fg='#fff').pack(pady=10)

        # 统计信息
        player = self.controller.player
        total_caught = player.get_pokemon_count()
        unique_count = player.get_unique_pokemon_count()
        total_available = len(self.controller.pokemon_factory.get_all_pokemon_names())

        stats_text = f"""
        总收服数量: {total_caught} 只
        精灵种类: {unique_count} 种
        图鉴完成度: {int(unique_count / total_available * 100)}%

        属性分布:
        """

        stats_label = tk.Label(main_frame, text=stats_text, font=("微软雅黑", 12),
                               bg='#27ae60', fg='#fff', justify=tk.LEFT)
        stats_label.pack(anchor=tk.W, pady=10)

        # 属性统计
        element_count = {}
        for pokemon in player.pokemons:
            element = pokemon.element.value
            element_count[element] = element_count.get(element, 0) + 1

        for element, count in sorted(element_count.items()):
            element_frame = tk.Frame(main_frame, bg='#27ae60')
            element_frame.pack(fill=tk.X, pady=2)

            tk.Label(element_frame, text=f"{element}系:", font=("微软雅黑", 11),
                     bg='#27ae60', fg='#ffd700', width=8, anchor=tk.W).pack(side=tk.LEFT)

            tk.Label(element_frame, text=f"{count}只", font=("微软雅黑", 11),
                     bg='#27ae60', fg='#fff').pack(side=tk.LEFT)

            # 进度条
            bar_canvas = tk.Canvas(element_frame, width=150, height=15,
                                   bg='#34495e', highlightthickness=0)
            bar_canvas.pack(side=tk.LEFT, padx=5)
            bar_width = int(150 * count / max(1, total_caught))
            bar_canvas.create_rectangle(0, 0, bar_width, 15, fill='#3498db')

        # 关闭按钮
        close_btn = tk.Button(main_frame, text="关闭", font=("微软雅黑", 12),
                              bg='#e74c3c', fg='#fff', padx=20, pady=8,
                              command=stats_window.destroy)
        close_btn.pack(pady=20)

    def heal_pokemon(self, pokemon):
        """治疗精灵"""
        if self.controller.current_battle:
            pokemon.heal()
            self.update_stats()
            self.add_message(f"💚 {pokemon.name} 已被完全治愈！")

            # 更新战斗显示
            if self.wild_display_widgets:
                strategy = self.controller.display_strategy
                strategy.update_wild_display(self.wild_display_widgets, pokemon)

            # 刷新图鉴显示
            self.update_pokedex_list()

            if self.pokedex_detail_window and self.pokedex_detail_window.winfo_exists():
                self.pokedex_detail_window.destroy()

    def enter_grass(self):
        """进入草丛"""
        wild_pokemon = self.controller.enter_grass()
        if wild_pokemon:
            # 清除占位符
            if hasattr(self, 'wild_placeholder') and self.wild_placeholder:
                self.wild_placeholder.destroy()
                self.wild_placeholder = None

            # 清除容器中的所有控件
            for widget in self.wild_container.winfo_children():
                widget.destroy()

            # 使用当前显示策略创建野生精灵显示
            strategy = self.controller.display_strategy
            self.wild_display_widgets = strategy.create_wild_display(
                self.wild_container, wild_pokemon
            )

            # 确保显示正确
            self.wild_container.update()

            # 启用战斗按钮
            self.attack_btn.config(state=tk.NORMAL)
            self.catch_btn.config(state=tk.NORMAL)
            self.run_btn.config(state=tk.NORMAL)

            self.add_message(f"🌿 进入草丛，遇到了野生 {wild_pokemon.name}！")
        else:
            self.add_message("已经在战斗中了！")

    def attack_pokemon(self):
        """攻击精灵"""
        result = self.controller.attack_pokemon()
        if result:
            self.add_message(f"⚔️ 你对野生精灵造成了 {result['damage']} 点伤害！")

            # 更新显示
            wild_pokemon = self.controller.current_battle.wild_pokemon
            strategy = self.controller.display_strategy
            strategy.update_wild_display(self.wild_display_widgets, wild_pokemon)

            if not result['is_alive']:
                self.add_message(f"💀 野生精灵倒下了...")
                self.end_battle()
            else:
                self.add_message(f"💥 野生精灵对你造成了 {result['counter_damage']} 点伤害！")

            self.update_stats()

    def catch_pokemon(self):
        """捕捉精灵"""
        result = self.controller.catch_pokemon()
        if result:
            self.add_message(f"🎾 扔出了精灵球！")
            self.update_stats()

            # 延迟显示结果
            self.after(1000, lambda: self.catch_result(result))

    def catch_result(self, result):
        """捕捉结果"""
        if result['success']:
            self.add_message(f"✨ 捕捉成功！恭喜你收服了 {result['pokemon'].name}！")
            self.add_message(f"🎉 获得 {result['score_gained']} 分！")
            self.update_stats()
            self.end_battle()
        else:
            self.add_message(f"😭 精灵球摇晃了几下...野生精灵挣脱了！")
            # 可能逃跑
            if random.random() < 0.3:
                self.add_message(f"🏃 野生精灵逃跑了！")
                self.end_battle()

    def run_away(self):
        """逃跑"""
        result = self.controller.run_away()
        if result:
            if result['success']:
                self.add_message("🏃 成功逃跑！")
                self.end_battle()
            else:
                self.add_message("😰 逃跑失败！")

    def end_battle(self):
        """结束战斗"""
        self.controller.end_battle()

        # 清除野生精灵显示
        if self.wild_display_widgets:
            strategy = self.controller.display_strategy
            strategy.destroy_display(self.wild_display_widgets)
            self.wild_display_widgets = None

        # 显示占位符
        self.wild_placeholder = tk.Label(self.wild_container,
                                         text="✨ 点击下方按钮进入草丛 ✨",
                                         font=("微软雅黑", 14),
                                         bg='#27ae60', fg='#f1c40f')
        self.wild_placeholder.pack(expand=True)

        # 禁用战斗按钮
        self.attack_btn.config(state=tk.DISABLED)
        self.catch_btn.config(state=tk.DISABLED)
        self.run_btn.config(state=tk.DISABLED)

        self.update_stats()

    def switch_display_mode(self):
        """切换显示模式"""
        # 判断当前模式
        current_mode = "text" if isinstance(self.controller.display_strategy,
                                            TextDisplayStrategy) else "graphic"
        new_mode = "graphic" if current_mode == "text" else "text"

        # 切换模式
        self.controller.set_display_mode(new_mode)

        # 如果正在战斗中，重新显示当前精灵
        if self.controller.current_battle and self.wild_display_widgets:
            strategy = self.controller.display_strategy
            wild_pokemon = self.controller.current_battle.wild_pokemon

            # 重新创建显示
            if hasattr(self.controller.display_strategy, 'destroy_display'):
                try:
                    self.controller.display_strategy.destroy_display(self.wild_display_widgets)
                except:
                    pass

            self.wild_display_widgets = strategy.create_wild_display(
                self.wild_container, wild_pokemon
            )

        self.add_message(f"🔄 已切换到{new_mode}模式")

    def open_shop(self):
        """打开商店"""
        from views.shop_view import ShopView
        ShopView(self, self.controller, self.update_stats)

    def reset_game(self):
        """重置游戏"""
        if messagebox.askyesno("确认", "确定要重新开始游戏吗？当前进度将丢失。"):
            if self.controller.player:
                self.controller.start_game(self.controller.player.name)
            else:
                self.controller.start_game("训练家")

            # 保持当前显示模式
            current_mode = "text" if isinstance(self.controller.display_strategy,
                                                TextDisplayStrategy) else "graphic"
            self.controller.set_display_mode(current_mode)

            self.update_stats()
            self.end_battle()
            self.add_message("✨ 游戏已重置！")

    def exit_game(self):
        """退出游戏"""
        if messagebox.askyesno("确认", "确定要退出游戏吗？"):
            self.master.quit()