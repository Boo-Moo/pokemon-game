# controllers/game_controller.py
from typing import Optional
from models.player import Player
from models.battle import Battle
from models.map import GameMap, Location, TerrainType
from factories.pokemon_factory import PokemonFactory
from strategies.display_strategy import DisplayStrategy
from strategies.text_strategy import TextDisplayStrategy
from strategies.graphic_strategy import GraphicDisplayStrategy


class GameController:
    """游戏主控制器"""

    def __init__(self):
        self.player: Optional[Player] = None
        self.current_battle: Optional[Battle] = None
        self.pokemon_factory = PokemonFactory()
        self.display_strategy: DisplayStrategy = GraphicDisplayStrategy()
        self.game_map = GameMap()
        self.game_view = None
        self._initialize_map()

    def _initialize_map(self):
        """初始化地图"""
        # 创建地点
        locations = [
            Location("初始小镇", TerrainType.TOWN,
                     "一个宁静的小镇，是训练家旅程的起点。这里有商店和休息的地方。", 0.05),
            Location("森林入口", TerrainType.FOREST,
                     "茂密的森林入口，常见草系和电系精灵。", 0.1),
            Location("幽暗洞穴", TerrainType.CAVE,
                     "光线昏暗的洞穴，据说有神秘的精灵出没。", 0.15),
            Location("火焰山脉", TerrainType.MOUNTAIN,
                     "活跃的火山地带，火系精灵的栖息地。", 0.2),
            Location("湖泊", TerrainType.WATER,
                     "清澈的湖泊，水系精灵的天堂。", 0.1),
            Location("古代遗迹", TerrainType.ROAD,
                     "古老的遗迹，传说中隐藏着强大的精灵。", 0.25),
            Location("冰霜雪原", TerrainType.MOUNTAIN,
                     "常年积雪的雪原，环境极其寒冷。", 0.15),
            Location("天空之塔", TerrainType.ROAD,
                     "高耸入云的高塔，龙系精灵的栖息地。", 0.3),
            Location("精灵之森", TerrainType.FOREST,
                     "精灵们居住的森林，充满神秘气息。", 0.12),
            Location("神秘洞窟", TerrainType.CAVE,
                     "隐藏着传说精灵的洞窟，极其危险。", 0.35)
        ]

        # 添加地点到地图
        for loc in locations:
            self.game_map.add_location(loc)

        # 添加精灵出现率
        self._add_pokemon_spawns()

        # 创建地图连接
        connections = [
            ("初始小镇", "森林入口"),
            ("森林入口", "幽暗洞穴"),
            ("森林入口", "精灵之森"),
            ("幽暗洞穴", "火焰山脉"),
            ("幽暗洞穴", "古代遗迹"),
            ("火焰山脉", "天空之塔"),
            ("湖泊", "森林入口"),
            ("湖泊", "古代遗迹"),
            ("古代遗迹", "冰霜雪原"),
            ("冰霜雪原", "天空之塔"),
            ("精灵之森", "神秘洞窟")
        ]

        for from_loc, to_loc in connections:
            self.game_map.add_connection(from_loc, to_loc)

        # 设置起始地点
        self.game_map.move_to("初始小镇")

    def _add_pokemon_spawns(self):
        """添加各地点精灵出现率"""
        spawns = {
            "初始小镇": [("波波", 0.6), ("伊布", 0.4)],
            "森林入口": [("妙蛙种子", 0.4), ("皮卡丘", 0.35), ("波波", 0.25)],
            "幽暗洞穴": [("可达鸭", 0.5), ("皮卡丘", 0.3), ("卡比兽", 0.2)],
            "火焰山脉": [("小火龙", 0.7), ("卡比兽", 0.3)],
            "湖泊": [("杰尼龟", 0.5), ("可达鸭", 0.5)],
            "古代遗迹": [("卡比兽", 0.5), ("超梦", 0.05), ("伊布", 0.45)],
            "冰霜雪原": [("伊布", 0.7), ("皮卡丘", 0.3)],
            "天空之塔": [("快龙", 0.3), ("小火龙", 0.4), ("波波", 0.3)],
            "精灵之森": [("皮卡丘", 0.35), ("妙蛙种子", 0.35), ("伊布", 0.3)],
            "神秘洞窟": [("卡比兽", 0.5), ("超梦", 0.1), ("快龙", 0.4)]
        }

        for loc_name, pokemon_list in spawns.items():
            location = self.game_map.locations.get(loc_name)
            if location:
                for pokemon_name, rate in pokemon_list:
                    location.add_pokemon_spawn(pokemon_name, rate)

    def start_game(self, player_name: str):
        """开始新游戏"""
        self.player = Player(player_name)
        self.player.poke_balls = 15
        self.player.score = 0
        self.game_map.move_to("初始小镇")

    def set_display_mode(self, mode: str):
        """设置显示模式"""
        if mode == "text":
            self.display_strategy = TextDisplayStrategy()
        elif mode == "graphic":
            self.display_strategy = GraphicDisplayStrategy()

    def enter_grass(self):
        """进入草丛（在当前地点遭遇精灵）"""
        if self.current_battle:
            return None

        # 根据当前地点获取精灵
        current_loc = self.game_map.get_current_location()
        if current_loc:
            pokemon_name = self.game_map.get_pokemon_at_location(self.pokemon_factory)
            if pokemon_name:
                wild_pokemon = self.pokemon_factory.create_pokemon(pokemon_name)
                self.current_battle = Battle(self.player, wild_pokemon)
                return wild_pokemon

        # 默认随机
        wild_pokemon = self.pokemon_factory.create_random_pokemon()
        self.current_battle = Battle(self.player, wild_pokemon)
        return wild_pokemon

    def move_to_location(self, location_name: str) -> bool:
        """移动到新地点"""
        if self.game_map.move_to(location_name):
            # 移动后自动保存
            if self.player:
                self.player.save()
            return True
        return False

    def get_available_locations(self) -> list:
        """获取可前往的地点"""
        current = self.game_map.current_location
        if current:
            return self.game_map.get_available_locations(current)
        return []

    def get_current_location(self):
        """获取当前位置"""
        return self.game_map.get_current_location()

    def attack_pokemon(self):
        """攻击精灵"""
        if not self.current_battle:
            return None

        damage = self.current_battle.player_attack()
        result = {
            "action": "attack",
            "damage": damage,
            "wild_hp": self.current_battle.wild_pokemon.hp,
            "wild_max_hp": self.current_battle.wild_pokemon.max_hp,
            "is_alive": self.current_battle.is_wild_alive()
        }

        # 野生精灵反击
        if self.current_battle.is_wild_alive():
            counter_damage = self.current_battle.wild_attack()
            result["counter_damage"] = counter_damage

        return result

    def catch_pokemon(self):
        """捕捉精灵"""
        if not self.current_battle:
            return None

        success = self.current_battle.try_catch()
        result = {
            "action": "catch",
            "success": success,
            "pokemon": self.current_battle.wild_pokemon if success else None,
            "score_gained": 10 if success else 0
        }

        if success:
            self.end_battle()

        return result

    def run_away(self):
        """逃跑"""
        if not self.current_battle:
            return None

        success = self.current_battle.try_escape()
        result = {
            "action": "run",
            "success": success
        }

        if success:
            self.end_battle()

        return result

    def end_battle(self):
        """结束战斗"""
        self.current_battle = None

    def buy_poke_balls(self, amount: int) -> bool:
        """购买精灵球"""
        return self.player.buy_poke_balls(amount)

    def get_game_state(self):
        """获取游戏状态"""
        current_loc = self.game_map.get_current_location()
        return {
            "player_name": self.player.name if self.player else "",
            "score": self.player.score if self.player else 0,
            "poke_balls": self.player.poke_balls if self.player else 0,
            "pokemon_count": self.player.get_pokemon_count() if self.player else 0,
            "in_battle": self.current_battle is not None,
            "wild_pokemon": self.current_battle.wild_pokemon if self.current_battle else None,
            "current_location": current_loc.name if current_loc else "未知",
            "location_description": current_loc.description if current_loc else ""
        }