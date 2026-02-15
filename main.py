"""
ASMR GUI 应用入口
基于 Flet 框架，跨平台运行（桌面 + Android）。
"""

import flet as ft
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.detail_page import DetailPage
from components.audio_player import AudioPlayer
from components.nav_bar import NavBar


async def main(page: ft.Page):
    # ── 页面配置 ──────────────────────────────────────
    page.title = "ASMR Player"
    page.bgcolor = "#0d0d1a"
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.DEEP_PURPLE,
        visual_density=ft.VisualDensity.COMPACT,
    )

    # 响应式：移动端自适应
    page.window.min_width = 360
    page.window.width = 420
    page.window.height = 800

    # ── 全局组件 ──────────────────────────────────────
    try:
        audio_player = AudioPlayer()
    except Exception as e:
        print(f"AudioPlayer init failed: {e}")
        import traceback
        traceback.print_exc()
        audio_player = ft.Container() # Fallback

    # ── 页面实例 ──────────────────────────────────────
    def open_detail(work: dict):
        """打开作品详情页"""
        detail = DetailPage(
            work=work,
            audio_player=audio_player,
            on_back=show_main,
        )
        content_area.controls.clear()
        content_area.controls.append(detail)
        nav_bar.visible = False
        page.update()
        page.run_task(detail.load_tracks, page)

    def show_main():
        """返回主页面"""
        content_area.controls.clear()
        if current_tab[0] == 0:
            content_area.controls.append(home_page)
        else:
            content_area.controls.append(search_page)
        nav_bar.visible = True
        page.update()

    home_page = HomePage(on_work_click=open_detail)
    search_page = SearchPage(on_work_click=open_detail)

    current_tab = [0]

    # ── 导航切换 ──────────────────────────────────────
    async def on_nav_change(e):
        idx = e.control.selected_index
        current_tab[0] = idx
        content_area.controls.clear()
        if idx == 0:
            content_area.controls.append(home_page)
        else:
            content_area.controls.append(search_page)
        page.update()

    try:
        nav_bar = NavBar(on_change=on_nav_change)
    except Exception as e:
        print(f"NavBar init failed: {e}")
        import traceback
        traceback.print_exc()
        nav_bar = ft.NavigationBar() # Fallback

    # ── 主内容区 ──────────────────────────────────────
    content_area = ft.Column(
        controls=[home_page],
        expand=True,
        spacing=0,
    )

    # ── 整体布局 ──────────────────────────────────────
    try:
        page.add(
            ft.Stack(
                controls=[
                    # 主内容
                    content_area,
                    # 底部播放器（浮在 nav_bar 上方）
                    ft.Container(
                        content=audio_player,
                        bottom=80,
                        left=0,
                        right=0,
                    ),
                ],
                expand=True,
            ),
        )
        page.navigation_bar = nav_bar

        # ── 初始加载 ──────────────────────────────────────
        await home_page.load_data()
    except Exception as e:
        page.clean()
        page.add(
            ft.Column(
                controls=[
                    ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED, size=50),
                    ft.Text("启动出错", size=24, color=ft.Colors.RED),
                    ft.Text(f"Error: {e}", size=16),
                    ft.Text(f"Type: {type(e)}", size=14, color=ft.Colors.GREY),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()


# ── 启动 ──────────────────────────────────────────────
if __name__ == "__main__":
    ft.app(target=main)
