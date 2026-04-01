# main.py
import tkinter as tk
from controllers.game_controller import GameController
from views.login_view import LoginView
from views.game_view import GameView


class PokemonGame:
    """游戏主类"""

    def __init__(self):
        self.root = tk.Tk()
        self.controller = GameController()
        self.current_view = None

        self.setup_root()
        self.show_login()

    def setup_root(self):
        """设置主窗口"""
        self.root.title("精灵捕捉大师")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2ecc71')

    def show_login(self):
        """显示登录界面"""
        if self.current_view:
            self.current_view.destroy()

        self.current_view = LoginView(self.root, self.controller, self.show_game)
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def show_game(self):
        """显示游戏界面"""
        if self.current_view:
            self.current_view.destroy()

        self.current_view = GameView(self.root, self.controller)
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def run(self):
        """运行游戏"""
        self.root.mainloop()


if __name__ == "__main__":
    game = PokemonGame()
    game.run()