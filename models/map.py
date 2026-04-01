# models/map.py
from enum import Enum
from typing import List, Dict, Optional


class TerrainType(Enum):
    """地形类型"""
    GRASS = "🌿"  # 草丛
    FOREST = "🌲"  # 森林
    MOUNTAIN = "⛰️"  # 山脉
    WATER = "💧"  # 水域
    CAVE = "🕳️"  # 洞穴
    TOWN = "🏘️"  # 城镇
    ROAD = "🛤️"  # 道路


class Location:
    """地点类"""

    def __init__(self, name: str, terrain: TerrainType, description: str,
                 rare_pokemon_rate: float = 0.1):
        self.name = name
        self.terrain = terrain
        self.description = description
        self.rare_pokemon_rate = rare_pokemon_rate  # 稀有精灵出现率
        self.visited = False
        self.pokemon_spawns = []  # 该地点可能出现的精灵列表

    def add_pokemon_spawn(self, pokemon_name: str, spawn_rate: float):
        """添加可出现的精灵"""
        self.pokemon_spawns.append({
            "name": pokemon_name,
            "rate": spawn_rate
        })

    def __str__(self):
        return f"{self.terrain.value} {self.name}"


class GameMap:
    """游戏地图类"""

    def __init__(self):
        self.locations: Dict[str, Location] = {}
        self.current_location: Optional[str] = None
        self.connections: Dict[str, List[str]] = {}  # 地点连接关系

    def add_location(self, location: Location):
        """添加地点"""
        self.locations[location.name] = location

    def add_connection(self, from_loc: str, to_loc: str):
        """添加地点连接"""
        if from_loc not in self.connections:
            self.connections[from_loc] = []
        if to_loc not in self.connections:
            self.connections[to_loc] = []

        if to_loc not in self.connections[from_loc]:
            self.connections[from_loc].append(to_loc)
        if from_loc not in self.connections[to_loc]:
            self.connections[to_loc].append(from_loc)

    def get_available_locations(self, location_name: str) -> List[str]:
        """获取可前往的地点"""
        return self.connections.get(location_name, [])

    def move_to(self, location_name: str) -> bool:
        """移动到新地点"""
        if location_name in self.locations:
            self.current_location = location_name
            self.locations[location_name].visited = True
            return True
        return False

    def get_current_location(self) -> Optional[Location]:
        """获取当前位置"""
        if self.current_location:
            return self.locations[self.current_location]
        return None

    def get_pokemon_at_location(self, factory) -> Optional[str]:
        """根据当前位置获取遇到的精灵"""
        location = self.get_current_location()
        if not location or not location.pokemon_spawns:
            return None

        # 根据出现率随机选择精灵
        import random
        total_rate = sum(spawn["rate"] for spawn in location.pokemon_spawns)
        rand = random.random() * total_rate

        cumulative = 0
        for spawn in location.pokemon_spawns:
            cumulative += spawn["rate"]
            if rand <= cumulative:
                return spawn["name"]

        return location.pokemon_spawns[0]["name"] if location.pokemon_spawns else None