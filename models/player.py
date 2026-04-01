# models/player.py
import json
import os
from typing import List
from .pokemon import Pokemon


class Player:
    """玩家类 - 核心数据模型"""

    def __init__(self, name):
        self.name = name
        self.pokemons: List[Pokemon] = []
        self.poke_balls = 0
        self.score = 0
        self.total_caught = 0
        self.total_battles = 0

    def add_pokemon(self, pokemon: Pokemon):
        """添加精灵到图鉴"""
        # 克隆一份，避免引用问题
        new_pokemon = pokemon.clone()
        self.pokemons.append(new_pokemon)
        self.total_caught += 1

    def use_poke_ball(self) -> bool:
        """使用精灵球"""
        if self.poke_balls > 0:
            self.poke_balls -= 1
            return True
        return False

    def add_score(self, amount: int):
        """增加分数"""
        self.score += amount

    def add_poke_balls(self, amount: int):
        """增加精灵球"""
        self.poke_balls += amount

    def buy_poke_balls(self, amount: int) -> bool:
        """购买精灵球"""
        cost = amount * 10
        if self.score >= cost:
            self.score -= cost
            self.poke_balls += amount
            return True
        return False

    def get_pokemon_count(self) -> int:
        """获取精灵数量"""
        return len(self.pokemons)

    def get_unique_pokemon_count(self) -> int:
        """获取不同精灵数量"""
        unique_names = set(p.name for p in self.pokemons)
        return len(unique_names)

    def has_pokemon(self, pokemon_name: str) -> bool:
        """判断是否拥有某只精灵"""
        return any(p.name == pokemon_name for p in self.pokemons)

    def get_pokemon_by_name(self, name: str) -> Pokemon:
        """根据名称获取精灵"""
        for pokemon in self.pokemons:
            if pokemon.name == name:
                return pokemon
        return None

    def save(self, filename: str = None):
        """保存玩家数据"""
        if filename is None:
            filename = f"player_{self.name}.json"

        data = {
            "name": self.name,
            "pokemons": [p.to_dict() for p in self.pokemons],
            "poke_balls": self.poke_balls,
            "score": self.score,
            "total_caught": self.total_caught,
            "total_battles": self.total_battles
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, filename: str = None):
        """加载玩家数据"""
        if filename is None:
            filename = f"player_{self.name}.json"

        if not os.path.exists(filename):
            return False

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 这里需要根据实际数据加载
        # 简化实现，实际需要重新创建Pokemon对象
        return True