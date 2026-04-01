# factories/pokemon_factory.py
import random
from typing import List
from models.pokemon import Pokemon, ElementType


class PokemonFactory:
    """精灵工厂类 - 负责创建精灵实例"""

    _instance = None
    _pokemon_templates = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_templates()
        return cls._instance

    def _initialize_templates(self):
        """初始化精灵模板"""
        self._pokemon_templates = {
            "皮卡丘": Pokemon(
                1, "皮卡丘", 50, 15, 0.4, "⚡",
                "电系精灵，可爱的电气老鼠", ElementType.ELECTRIC, "mouse", "#FFD700"
            ),
            "小火龙": Pokemon(
                2, "小火龙", 60, 18, 0.35, "🔥",
                "火系精灵，尾巴上的火焰代表生命力", ElementType.FIRE, "dragon", "#FF6B6B"
            ),
            "杰尼龟": Pokemon(
                3, "杰尼龟", 70, 12, 0.45, "💧",
                "水系精灵，性格温和的小乌龟", ElementType.WATER, "turtle", "#4ECDC4"
            ),
            "妙蛙种子": Pokemon(
                4, "妙蛙种子", 65, 14, 0.4, "🌿",
                "草系精灵，背上有神奇的种子", ElementType.GRASS, "frog", "#6B8E23"
            ),
            "波波": Pokemon(
                5, "波波", 40, 10, 0.6, "🕊️",
                "飞行系精灵，常见的小鸟", ElementType.FLYING, "bird", "#D2691E"
            ),
            "可达鸭": Pokemon(
                6, "可达鸭", 55, 13, 0.5, "🦆",
                "水系精灵，总是头疼的样子", ElementType.WATER, "duck", "#FFE4B5"
            ),
            "卡比兽": Pokemon(
                7, "卡比兽", 100, 20, 0.2, "😴",
                "一般系精灵，超级贪吃嗜睡", ElementType.NORMAL, "default", "#8B4513"
            ),
            "伊布": Pokemon(
                8, "伊布", 45, 12, 0.5, "🦊",
                "一般系精灵，可以进化成多种形态", ElementType.NORMAL, "mouse", "#D2B48C"
            ),
        }

    def create_pokemon(self, name: str) -> Pokemon:
        """根据名称创建精灵"""
        if name in self._pokemon_templates:
            template = self._pokemon_templates[name]
            return Pokemon(
                template.id, template.name, template.max_hp, template.attack,
                template.catch_rate, template.emoji, template.description,
                template.element, template.image_type, template.color
            )
        return None

    def create_random_pokemon(self) -> Pokemon:
        """创建随机精灵"""
        name = random.choice(list(self._pokemon_templates.keys()))
        return self.create_pokemon(name)

    def get_all_pokemon_names(self) -> List[str]:
        """获取所有精灵名称"""
        return list(self._pokemon_templates.keys())

    def get_pokemon_by_id(self, pokemon_id: int) -> Pokemon:
        """根据ID获取精灵"""
        for pokemon in self._pokemon_templates.values():
            if pokemon.id == pokemon_id:
                return self.create_pokemon(pokemon.name)
        return None