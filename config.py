# config.py
import os


class GameConfig:
    """游戏配置类"""

    # 窗口配置
    WINDOW_TITLE = "精灵捕捉大师"
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700
    WINDOW_BG = "#2ecc71"

    # 游戏配置
    INIT_POKE_BALLS = 15
    CATCH_SCORE = 10
    BALL_PRICE = 10

    # 战斗配置
    MIN_DAMAGE = 10
    MAX_DAMAGE = 25
    ESCAPE_RATE = 0.7
    COUNTER_ATTACK_RATE = 0.3

    # 颜色配置
    COLOR_BG_MAIN = "#2ecc71"
    COLOR_BG_SECONDARY = "#27ae60"
    COLOR_BG_DARK = "#2c3e50"
    COLOR_TEXT_LIGHT = "#ffffff"
    COLOR_TEXT_GOLD = "#ffd700"
    COLOR_HP_BAR = "#e74c3c"
    COLOR_HP_BG = "#2c3e50"
    COLOR_BUTTON_ACTION = "#f39c12"
    COLOR_BUTTON_ATTACK = "#e74c3c"
    COLOR_BUTTON_CATCH = "#3498db"
    COLOR_BUTTON_RUN = "#95a5a6"
    COLOR_BUTTON_SHOP = "#1abc9c"
    COLOR_BUTTON_RESET = "#e67e22"
    COLOR_BUTTON_EXIT = "#c0392b"

    # 字体配置
    FONT_TITLE = ("微软雅黑", 36, "bold")
    FONT_SUBTITLE = ("微软雅黑", 14)
    FONT_NORMAL = ("微软雅黑", 12)
    FONT_SMALL = ("微软雅黑", 10)
    FONT_BOLD = ("微软雅黑", 12, "bold")

    # 路径配置
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    @classmethod
    def ensure_dirs(cls):
        """确保必要的目录存在"""
        if not os.path.exists(cls.DATA_DIR):
            os.makedirs(cls.DATA_DIR)