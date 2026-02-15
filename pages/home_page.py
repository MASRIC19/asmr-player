"""
首页 — 发现
展示最新/热门 ASMR 作品的网格列表，支持排序切换和分页加载。
"""

import flet as ft
from asmr_api import AsmrApi
from components.work_card import WorkCard


class HomePage(ft.Column):
    """首页 — 作品发现"""

    ORDER_OPTIONS = {
        "最新上传": "create_date",
        "最新发售": "release",
        "下载最多": "dl_count",
        "评分最高": "rate_average_2dp",
        "评论最多": "review_count",
        "随机推荐": "random",
    }

    def __init__(self, on_work_click=None):
        super().__init__(expand=True, spacing=0)
        self._on_work_click = on_work_click
        self._page_num = 1
        self._order = "create_date"
        self._loading = False

        # 排序下拉
        self.order_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(key=v, text=k) for k, v in self.ORDER_OPTIONS.items()],
            value="create_date",
            width=160,
            height=42,
            text_size=13,
            border_color=ft.Colors.WHITE24,
            color=ft.Colors.WHITE,
            on_change=self._on_order_change,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=4),
        )

        # 作品网格容器
        self.grid = ft.GridView(
            runs_count=2,
            max_extent=220,
            child_aspect_ratio=0.62,
            spacing=12,
            run_spacing=12,
            expand=True,
            padding=ft.padding.symmetric(horizontal=16, vertical=8),
        )

        # 加载更多按钮
        self.load_more_btn = ft.Container(
            content=ft.TextButton(
                text="加载更多",
                icon=ft.Icons.EXPAND_MORE_ROUNDED,
                on_click=self._load_more,
                style=ft.ButtonStyle(color=ft.Colors.DEEP_PURPLE_ACCENT_100),
            ),
            alignment=ft.Alignment(0, 0),
            padding=ft.padding.only(bottom=80),
        )

        # 加载指示器
        self.loading_ring = ft.Container(
            content=ft.ProgressRing(
                width=30, height=30,
                color=ft.Colors.DEEP_PURPLE_ACCENT_100,
            ),
            alignment=ft.Alignment(0, 0),
            padding=20,
            visible=False,
        )

        # 顶部栏
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        "🎧 发现",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Container(expand=True),
                    self.order_dropdown,
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(left=20, right=16, top=12, bottom=4),
        )

        self.controls = [header, self.grid, self.loading_ring, self.load_more_btn]

    async def load_data(self):
        """加载作品数据"""
        if self._loading:
            return
        self._loading = True
        self.loading_ring.visible = True
        self.update()

        try:
            async with AsmrApi() as api:
                data = await api.get_works(page=self._page_num, order=self._order)

            works = data.get("works", [])
            if works:
                for w in works:
                    card = WorkCard(w, on_click=self._on_work_click)
                    self.grid.controls.append(card)
                self.load_more_btn.visible = True
            else:
                self.load_more_btn.visible = False
        except Exception as e:
            self.grid.controls.append(
                ft.Container(
                    content=ft.Text(f"加载失败: {e}", color=ft.Colors.RED_300),
                    padding=20,
                )
            )
        finally:
            self._loading = False
            self.loading_ring.visible = False
            self.update()

    async def _on_order_change(self, e):
        self._order = e.control.value
        self._page_num = 1
        self.grid.controls.clear()
        await self.load_data()

    async def _load_more(self, e):
        self._page_num += 1
        await self.load_data()
