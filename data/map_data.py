# data/map_data.py
from models.map import Location, TerrainType

# 地图配置数据
MAP_CONFIG = {
    "locations": {
        "初始小镇": {
            "terrain": TerrainType.TOWN,
            "description": "一个宁静的小镇，是训练家旅程的起点。这里有商店和休息的地方。",
            "rare_rate": 0.05,
            "spawns": [("波波", 0.6), ("伊布", 0.4)]
        },
        "森林入口": {
            "terrain": TerrainType.FOREST,
            "description": "茂密的森林入口，常见草系和电系精灵。",
            "rare_rate": 0.1,
            "spawns": [("妙蛙种子", 0.4), ("皮卡丘", 0.35), ("波波", 0.25)]
        },
        # ... 更多地点配置
    },
    "connections": [
        ("初始小镇", "森林入口"),
        ("森林入口", "幽暗洞穴"),
        # ... 更多连接
    ]
}