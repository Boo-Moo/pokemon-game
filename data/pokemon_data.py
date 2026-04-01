# data/pokemon_data.py
from models.pokemon import Pokemon, ElementType

# 精灵数据库
POKEMON_DATABASE = {
    "皮卡丘": {
        "id": 1,
        "name": "皮卡丘",
        "hp": 50,
        "attack": 15,
        "catch_rate": 0.4,
        "emoji": "⚡",
        "description": "电系精灵，可爱的电气老鼠，脸颊两边的电气袋能释放电流",
        "element": ElementType.ELECTRIC,
        "image_type": "mouse",
        "color": "#FFD700"
    },
    "小火龙": {
        "id": 2,
        "name": "小火龙",
        "hp": 60,
        "attack": 18,
        "catch_rate": 0.35,
        "emoji": "🔥",
        "description": "火系精灵，尾巴上的火焰代表生命力，火焰越旺盛说明越健康",
        "element": ElementType.FIRE,
        "image_type": "dragon",
        "color": "#FF6B6B"
    },
    # ... 更多精灵数据
}

def get_pokemon_data(name):
    """获取精灵数据"""
    return POKEMON_DATABASE.get(name)