# test_graphic.py
import tkinter as tk
from models.pokemon import Pokemon, ElementType
from strategies.graphic_strategy import GraphicDisplayStrategy


def test_graphic():
    root = tk.Tk()
    root.title("图形显示测试")
    root.geometry("400x500")
    root.configure(bg='#2ecc71')

    # 创建测试精灵
    pikachu = Pokemon(
        1, "皮卡丘", 50, 15, 0.4, "⚡",
        "电系精灵，可爱的电气老鼠", ElementType.ELECTRIC, "mouse", "#FFD700"
    )

    # 创建显示策略
    strategy = GraphicDisplayStrategy()

    # 创建容器
    container = tk.Frame(root, bg='#27ae60')
    container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    # 创建显示
    widgets = strategy.create_wild_display(container, pikachu)

    # 添加按钮测试更新
    def update_hp():
        pikachu.hp = max(0, pikachu.hp - 10)
        strategy.update_wild_display(widgets, pikachu)
        print(f"HP更新为: {pikachu.hp}")

    btn = tk.Button(root, text="减少HP", command=update_hp)
    btn.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    test_graphic()