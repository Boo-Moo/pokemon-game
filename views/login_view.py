# views/login_view.py
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk


class LoginView(tk.Frame):
    """登录界面"""

    def __init__(self, parent, controller, on_success):
        super().__init__(parent)
        self.controller = controller
        self.on_success = on_success
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        """设置界面"""
        self.configure(bg='#2ecc71')

        # 标题
        title_frame = tk.Frame(self, bg='#2ecc71')
        title_frame.pack(pady=50)

        title_label = tk.Label(title_frame, text="✨ 精灵捕捉大师 ✨",
                               font=("微软雅黑", 36, "bold"),
                               bg='#2ecc71', fg='#fff')
        title_label.pack()

        subtitle_label = tk.Label(title_frame, text="踏上成为精灵大师的旅程！",
                                  font=("微软雅黑", 14),
                                  bg='#2ecc71', fg='#f1c40f')
        subtitle_label.pack(pady=10)

        # 输入框
        input_frame = tk.Frame(self, bg='#2ecc71')
        input_frame.pack(pady=50)

        tk.Label(input_frame, text="训练家名字：", font=("微软雅黑", 14),
                 bg='#2ecc71', fg='#fff').pack(side=tk.LEFT, padx=10)

        self.name_entry = tk.Entry(input_frame, font=("微软雅黑", 14), width=20)
        self.name_entry.pack(side=tk.LEFT, padx=10)
        self.name_entry.bind('<Return>', lambda e: self.start_game())

        # 显示模式选择
        mode_frame = tk.Frame(self, bg='#2ecc71')
        mode_frame.pack(pady=20)

        tk.Label(mode_frame, text="显示模式：", font=("微软雅黑", 12),
                 bg='#2ecc71', fg='#fff').pack(side=tk.LEFT, padx=10)

        self.display_mode = tk.StringVar(value="graphic")
        text_radio = tk.Radiobutton(mode_frame, text="文字模式", variable=self.display_mode,
                                    value="text", bg='#2ecc71', fg='#fff',
                                    selectcolor='#2ecc71')
        text_radio.pack(side=tk.LEFT, padx=10)

        graphic_radio = tk.Radiobutton(mode_frame, text="图像模式", variable=self.display_mode,
                                       value="graphic", bg='#2ecc71', fg='#fff',
                                       selectcolor='#2ecc71')
        graphic_radio.pack(side=tk.LEFT, padx=10)

        # 开始按钮
        start_btn = tk.Button(self, text="开始冒险", font=("微软雅黑", 14, "bold"),
                              bg='#f39c12', fg='#fff', padx=30, pady=10,
                              command=self.start_game, cursor="hand2")
        start_btn.pack(pady=20)

        # 游戏说明
        info_text = """
        🎮 游戏说明：
        • 进入草丛会遇到野生精灵
        • 攻击精灵降低血量，提高捕捉成功率
        • 使用精灵球捕捉精灵
        • 捕捉成功获得分数，可用于购买精灵球
        • 收集更多的精灵，成为精灵大师！
        """

        info_label = tk.Label(self, text=info_text, font=("微软雅黑", 10),
                              bg='#27ae60', fg='#fff', justify=tk.LEFT,
                              padx=20, pady=10)
        info_label.pack(pady=30)

    def start_game(self):
        """开始游戏"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("提示", "请输入训练家名字！")
            return

        self.controller.start_game(name)
        self.controller.set_display_mode(self.display_mode.get())
        self.on_success()