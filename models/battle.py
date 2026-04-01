# models/battle.py
import random
from enum import Enum
from .pokemon import Pokemon
from .player import Player


class BattleResult(Enum):
    """战斗结果"""
    CAPTURED = "captured"
    ESCAPED = "escaped"
    DEFEATED = "defeated"
    RUN_AWAY = "run_away"


class Battle:
    """战斗类 - 处理战斗逻辑"""

    def __init__(self, player: Player, wild_pokemon: Pokemon):
        self.player = player
        self.wild_pokemon = wild_pokemon
        self.turn_count = 0
        self.damage_dealt = 0

    def player_attack(self) -> int:
        """玩家攻击"""
        damage = random.randint(10, 25)
        self.wild_pokemon.take_damage(damage)
        self.damage_dealt += damage
        self.turn_count += 1
        return damage

    def wild_attack(self) -> int:
        """野生精灵攻击"""
        if not self.wild_pokemon.is_alive():
            return 0
        damage = random.randint(5, self.wild_pokemon.attack)
        self.turn_count += 1
        return damage

    def calculate_catch_chance(self) -> float:
        """计算捕捉成功率"""
        if not self.wild_pokemon.is_alive():
            return 0.0

        hp_rate = self.wild_pokemon.hp / self.wild_pokemon.max_hp
        catch_chance = self.wild_pokemon.catch_rate * (1 - hp_rate * 0.5)
        catch_chance = min(catch_chance, 0.85)
        return catch_chance

    def try_catch(self) -> bool:
        """尝试捕捉"""
        if not self.player.use_poke_ball():
            return False

        catch_chance = self.calculate_catch_chance()
        success = random.random() < catch_chance

        if success:
            self.player.add_pokemon(self.wild_pokemon)
            self.player.add_score(10)

        return success

    def try_escape(self) -> bool:
        """尝试逃跑"""
        escape_chance = 0.7
        success = random.random() < escape_chance
        return success

    def is_wild_alive(self) -> bool:
        """野生精灵是否存活"""
        return self.wild_pokemon.is_alive()

    def get_battle_info(self) -> dict:
        """获取战斗信息"""
        return {
            "turn": self.turn_count,
            "wild_hp": f"{self.wild_pokemon.hp}/{self.wild_pokemon.max_hp}",
            "wild_hp_percent": self.wild_pokemon.get_hp_percentage(),
            "damage_dealt": self.damage_dealt,
            "catch_chance": self.calculate_catch_chance()
        }