# factories/pokemon_factory.py
import random
from typing import List, Dict
from models.pokemon import Pokemon, ElementType
from models.map import Location, TerrainType


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
            "超梦": Pokemon(
                9, "超梦", 120, 25, 0.05, "🧬",
                "传说精灵，拥有强大的超能力", ElementType.NORMAL, "default", "#A569BD"
            ),
            "快龙": Pokemon(
                10, "快龙", 110, 22, 0.08, "🐉",
                "龙系精灵，非常稀有", ElementType.FLYING, "dragon", "#5DADE2"
            )
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

    def create_random_pokemon(self, location_name: str = None) -> Pokemon:
        """创建随机精灵（根据地点）"""
        if location_name:
            # 根据地点返回特定精灵
            location_pokemon = self._get_location_pokemon(location_name)
            if location_pokemon:
                name = random.choice(location_pokemon)
                return self.create_pokemon(name)

        # 随机选择
        name = random.choice(list(self._pokemon_templates.keys()))
        return self.create_pokemon(name)

    def _get_location_pokemon(self, location_name: str) -> List[str]:
        """获取特定地点可能出现的精灵"""
        location_spawns = {
            "初始小镇": ["波波", "伊布"],
            "森林入口": ["妙蛙种子", "皮卡丘", "波波"],
            "幽暗洞穴": ["可达鸭", "皮卡丘"],
            "火焰山脉": ["小火龙"],
            "湖泊": ["杰尼龟", "可达鸭"],
            "古代遗迹": ["卡比兽", "超梦"],
            "冰霜雪原": ["伊布"],
            "天空之塔": ["快龙"],
            "精灵之森": ["皮卡丘", "妙蛙种子", "伊布"],
            "神秘洞窟": ["卡比兽", "超梦"]
        }
        return location_spawns.get(location_name, list(self._pokemon_templates.keys()))

    def get_all_pokemon_names(self) -> List[str]:
        """获取所有精灵名称"""
        return list(self._pokemon_templates.keys())

    def get_pokemon_by_id(self, pokemon_id: int) -> Pokemon:
        """根据ID获取精灵"""
        for pokemon in self._pokemon_templates.values():
            if pokemon.id == pokemon_id:
                return self.create_pokemon(pokemon.name)
        return None

    def get_location_pokemon_list(self, location_name: str) -> List[str]:
        """获取地点可遇到的精灵列表"""
        return self._get_location_pokemon(location_name)