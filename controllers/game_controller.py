# controllers/game_controller.py
from typing import Optional
import random
from models.player import Player
from models.battle import Battle
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
        self.display_strategy: DisplayStrategy = GraphicDisplayStrategy()  # 默认图像模式
        self.game_view = None

    def start_game(self, player_name: str):
        """开始新游戏"""
        self.player = Player(player_name)
        self.player.poke_balls = 15
        self.player.score = 0

    def set_display_mode(self, mode: str):
        """设置显示模式"""
        if mode == "text":
            self.display_strategy = TextDisplayStrategy()
        elif mode == "graphic":
            self.display_strategy = GraphicDisplayStrategy()

    def enter_grass(self):
        """进入草丛"""
        if self.current_battle:
            return None

        wild_pokemon = self.pokemon_factory.create_random_pokemon()
        self.current_battle = Battle(self.player, wild_pokemon)
        return wild_pokemon

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
        return {
            "player_name": self.player.name if self.player else "",
            "score": self.player.score if self.player else 0,
            "poke_balls": self.player.poke_balls if self.player else 0,
            "pokemon_count": self.player.get_pokemon_count() if self.player else 0,
            "in_battle": self.current_battle is not None,
            "wild_pokemon": self.current_battle.wild_pokemon if self.current_battle else None
        }