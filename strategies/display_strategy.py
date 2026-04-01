# strategies/display_strategy.py
from abc import ABC, abstractmethod
from typing import Any, Dict


class DisplayStrategy(ABC):
    """显示策略抽象基类"""

    @abstractmethod
    def create_wild_display(self, parent, pokemon) -> Dict[str, Any]:
        """创建野生精灵显示"""
        pass

    @abstractmethod
    def update_wild_display(self, display_widgets: Dict[str, Any], pokemon):
        """更新野生精灵显示"""
        pass

    @abstractmethod
    def create_pokemon_list_item(self, parent, pokemon, index) -> Any:
        """创建精灵列表项"""
        pass

    @abstractmethod
    def destroy_display(self, display_widgets: Dict[str, Any]):
        """销毁显示"""
        pass