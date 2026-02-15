"""
底部导航栏组件
Material 风格底部导航，支持首页和搜索切换。
"""

import flet as ft


class NavBar(ft.NavigationBar):
    """底部导航栏"""

    def __init__(self, on_change=None):
        super().__init__(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.EXPLORE_OUTLINED,
                    selected_icon=ft.Icons.EXPLORE_ROUNDED,
                    label="发现",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SEARCH_OUTLINED,
                    selected_icon=ft.Icons.SEARCH_ROUNDED,
                    label="搜索",
                ),
            ],
            selected_index=0,
            # on_change=on_change, # Removed from init arg
            bgcolor=ft.Colors.with_opacity(0.85, "#1a1a2e"),
            indicator_color=ft.Colors.DEEP_PURPLE_ACCENT_100,
            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
            shadow_color=ft.Colors.BLACK,
            overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.DEEP_PURPLE),
        )
        self.on_change = on_change
