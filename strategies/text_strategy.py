# strategies/text_strategy.py
import tkinter as tk
from typing import Dict, Any
from .display_strategy import DisplayStrategy
from models.pokemon import Pokemon


class TextDisplayStrategy(DisplayStrategy):
    """文字显示策略实现"""

    def create_wild_display(self, parent, pokemon: Pokemon) -> Dict[str, Any]:
        """创建野生精灵文字显示"""
        frame = tk.Frame(parent, bg='#27ae60')

        # 精灵名字和表情
        name_label = tk.Label(frame, text=f"{pokemon.emoji} {pokemon.name}",
                              font=("微软雅黑", 16, "bold"),
                              bg='#27ae60', fg='#fff')
        name_label.pack(pady=10)

        # 精灵信息
        info_text = f"""
HP: {pokemon.hp}/{pokemon.max_hp}
属性: {pokemon.element.value}
描述: {pokemon.description}
        """
        info_label = tk.Label(frame, text=info_text,
                              font=("微软雅黑", 11),
                              bg='#27ae60', fg='#fff',
                              justify=tk.LEFT)
        info_label.pack(pady=10)

        return {
            "frame": frame,
            "name_label": name_label,
            "info_label": info_label,
            "pokemon": pokemon
        }

    def update_wild_display(self, display_widgets: Dict[str, Any], pokemon: Pokemon):
        """更新野生精灵显示"""
        if "info_label" in display_widgets:
            info_text = f"""
HP: {pokemon.hp}/{pokemon.max_hp}
属性: {pokemon.element.value}
描述: {pokemon.description}
            """
            display_widgets["info_label"].config(text=info_text)

    def create_pokemon_list_item(self, parent, pokemon: Pokemon, index: int) -> Any:
        """创建精灵列表项"""
        frame = tk.Frame(parent, bg='#34495e')
        frame.pack(fill=tk.X, pady=2)

        label = tk.Label(frame,
                         text=f"{index}. {pokemon.emoji} {pokemon.name} (HP: {pokemon.hp}/{pokemon.max_hp})",
                         font=("微软雅黑", 10),
                         bg='#34495e', fg='#fff',
                         anchor=tk.W)
        label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        return frame

    def destroy_display(self, display_widgets: Dict[str, Any]):
        """销毁显示"""
        if "frame" in display_widgets:
            display_widgets["frame"].destroy()