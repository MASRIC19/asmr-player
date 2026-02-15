"""
搜索页面
关键词搜索 ASMR 作品，支持排序和分页。
"""

import flet as ft
from asmr_api import AsmrApi
from components.work_card import WorkCard


class SearchPage(ft.Column):
    """搜索页面"""

    def __init__(self, on_work_click=None):
        super().__init__(expand=True, spacing=0)
        self._on_work_click = on_work_click
        self._page_num = 1
        self._keyword = ""
        self._loading = False

        # 搜索框
        self.search_field = ft.TextField(
            hint_text="搜索作品、标签、声优...",
            prefix_icon=ft.Icons.SEARCH_ROUNDED,
            border_radius=25,
            height=48,
            text_size=14,
            border_color=ft.Colors.WHITE24,
            focused_border_color=ft.Colors.DEEP_PURPLE_ACCENT_100,
            color=ft.Colors.WHITE,
            hint_style=ft.TextStyle(color=ft.Colors.WHITE38),
            on_submit=self._on_search,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=8),
        )

        # 结果网格
        self.grid = ft.GridView(
            runs_count=2,
            max_extent=220,
            child_aspect_ratio=0.62,
            spacing=12,
            run_spacing=12,
            expand=True,
            padding=ft.padding.symmetric(horizontal=16, vertical=8),
        )

        # 空状态提示
        self.empty_hint = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.Icons.HEADPHONES_ROUNDED,
                        size=64,
                        color=ft.Colors.WHITE12,
                    ),
                    ft.Text(
                        "搜索你喜欢的 ASMR 作品",
                        size=16,
                        color=ft.Colors.WHITE24,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
            alignment=ft.Alignment(0, 0),
            expand=True,
        )

        # 加载更多
        self.load_more_btn = ft.Container(
            content=ft.TextButton(
                text="加载更多",
                icon=ft.Icons.EXPAND_MORE_ROUNDED,
                on_click=self._load_more,
                style=ft.ButtonStyle(color=ft.Colors.DEEP_PURPLE_ACCENT_100),
            ),
            alignment=ft.Alignment(0, 0),
            padding=ft.padding.only(bottom=80),
            visible=False,
        )

        self.loading_ring = ft.Container(
            content=ft.ProgressRing(
                width=30, height=30,
                color=ft.Colors.DEEP_PURPLE_ACCENT_100,
            ),
            alignment=ft.Alignment(0, 0),
            padding=20,
            visible=False,
        )

        # 顶部搜索栏
        header = ft.Container(
            content=self.search_field,
            padding=ft.padding.only(left=16, right=16, top=12, bottom=8),
        )

        self.controls = [header, self.empty_hint, self.grid, self.loading_ring, self.load_more_btn]

    async def _on_search(self, e):
        keyword = self.search_field.value.strip()
        if not keyword:
            return
        self._keyword = keyword
        self._page_num = 1
        self.grid.controls.clear()
        self.empty_hint.visible = False
        self.load_more_btn.visible = False
        await self._do_search()

    async def _load_more(self, e):
        self._page_num += 1
        await self._do_search()

    async def _do_search(self):
        if self._loading:
            return
        self._loading = True
        self.loading_ring.visible = True
        self.update()

        try:
            async with AsmrApi() as api:
                data = await api.search(self._keyword, page=self._page_num)

            works = data.get("works", [])
            if works:
                for w in works:
                    card = WorkCard(w, on_click=self._on_work_click)
                    self.grid.controls.append(card)
                self.load_more_btn.visible = True
            else:
                self.load_more_btn.visible = False
                if self._page_num == 1:
                    self.grid.controls.append(
                        ft.Container(
                            content=ft.Text(
                                "没有找到相关作品",
                                color=ft.Colors.WHITE38,
                                size=14,
                            ),
                            padding=20,
                        )
                    )
        except Exception as e:
            self.grid.controls.append(
                ft.Container(
                    content=ft.Text(f"搜索失败: {e}", color=ft.Colors.RED_300),
                    padding=20,
                )
            )
        finally:
            self._loading = False
            self.loading_ring.visible = False
            self.update()
