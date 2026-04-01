# views/shop_view.py
import tkinter as tk
from tkinter import messagebox


class ShopView(tk.Toplevel):
    """商店界面"""

    def __init__(self, parent, controller, on_update):
        super().__init__(parent)
        self.controller = controller
        self.on_update = on_update
        self.setup_ui()

    def setup_ui(self):
        """设置界面"""
        self.title("精灵商店")
        self.geometry("400x300")
        self.configure(bg='#2ecc71')

        tk.Label(self, text="🛒 精灵商店", font=("微软雅黑", 20, "bold"),
                 bg='#2ecc71', fg='#fff').pack(pady=20)

        state = self.controller.get_game_state()
        tk.Label(self, text=f"当前分数：{state['score']}",
                 font=("微软雅黑", 14), bg='#2ecc71', fg='#ffd700').pack(pady=10)

        tk.Label(self, text="1个精灵球 = 10分",
                 font=("微软雅黑", 12), bg='#2ecc71', fg='#fff').pack(pady=5)

        # 购买数量选择
        buy_frame = tk.Frame(self, bg='#2ecc71')
        buy_frame.pack(pady=20)

        tk.Label(buy_frame, text="购买数量：", font=("微软雅黑", 12),
                 bg='#2ecc71', fg='#fff').pack(side=tk.LEFT, padx=10)

        self.num_entry = tk.Entry(buy_frame, font=("微软雅黑", 12), width=10)
        self.num_entry.pack(side=tk.LEFT, padx=10)
        self.num_entry.insert(0, "1")

        # 预设按钮
        preset_frame = tk.Frame(self, bg='#2ecc71')
        preset_frame.pack(pady=10)

        for num in [1, 5, 10, 20]:
            btn = tk.Button(preset_frame, text=f"{num}个", font=("微软雅黑", 10),
                            bg='#3498db', fg='#fff', padx=10, pady=5,
                            command=lambda x=num: self.set_quantity(x))
            btn.pack(side=tk.LEFT, padx=5)

        buy_btn = tk.Button(self, text="购买", font=("微软雅黑", 12),
                            bg='#f39c12', fg='#fff', padx=30, pady=10,
                            command=self.buy_balls)
        buy_btn.pack(pady=20)

    def set_quantity(self, num):
        """设置数量"""
        self.num_entry.delete(0, tk.END)
        self.num_entry.insert(0, str(num))

    def buy_balls(self):
        """购买精灵球"""
        try:
            num = int(self.num_entry.get())
            if num <= 0:
                messagebox.showwarning("提示", "请输入正数！")
                return

            if self.controller.buy_poke_balls(num):
                self.on_update()
                messagebox.showinfo("成功", f"成功购买 {num} 个精灵球！")
                self.destroy()
            else:
                messagebox.showwarning("提示", "分数不足！")
        except ValueError:
            messagebox.showwarning("提示", "请输入有效数字！")