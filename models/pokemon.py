# models/pokemon.py
from enum import Enum


class ElementType(Enum):
    """精灵属性类型"""
    NORMAL = "一般"
    FIRE = "火"
    WATER = "水"
    GRASS = "草"
    ELECTRIC = "电"
    FLYING = "飞行"


class Pokemon:
    """精灵类 - 核心数据模型"""

    def __init__(self, id, name, hp, attack, catch_rate, emoji,
                 description, element, image_type, color):
        self.id = id
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.catch_rate = catch_rate
        self.emoji = emoji
        self.description = description
        self.element = element if isinstance(element, ElementType) else ElementType(element)
        self.image_type = image_type
        self.color = color

    def is_alive(self):
        """判断是否存活"""
        return self.hp > 0

    def take_damage(self, damage):
        """受到伤害"""
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return damage

    def heal(self, amount=None):
        """治疗"""
        if amount is None:
            self.hp = self.max_hp
        else:
            self.hp = min(self.max_hp, self.hp + amount)

    def get_hp_percentage(self):
        """获取血量百分比"""
        return self.hp / self.max_hp if self.max_hp > 0 else 0

    def clone(self):
        """克隆一个新的精灵实例"""
        return Pokemon(
            self.id, self.name, self.max_hp, self.attack,
            self.catch_rate, self.emoji, self.description,
            self.element, self.image_type, self.color
        )

    def __str__(self):
        return f"{self.emoji} {self.name} (HP: {self.hp}/{self.max_hp})"

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "attack": self.attack,
            "catch_rate": self.catch_rate,
            "emoji": self.emoji,
            "description": self.description,
            "element": self.element.value,
            "image_type": self.image_type,
            "color": self.color
        }