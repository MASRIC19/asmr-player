"""
作品卡片组件
可复用的作品展示卡片，显示封面、标题、评分等信息。
"""

import flet as ft


class WorkCard(ft.Container):
    """作品卡片 — 封面 + 标题 + 评分"""

    def __init__(self, work: dict, on_click=None):
        self.work = work
        self._on_click = on_click

        work_id = work.get("id", 0)
        title = work.get("title", "未知作品")
        circle_name = work.get("circle", {}).get("name", "")
        rate = work.get("rate_average_2dp", 0)
        dl_count = work.get("dl_count", 0)

        # 封面图
        cover_url = f"https://api.asmr-200.com/api/cover/{work_id}.jpg?type=sam"

        # 评分星星颜色
        rate_color = (
            ft.Colors.AMBER if rate >= 4.0
            else ft.Colors.ORANGE if rate >= 3.0
            else ft.Colors.GREY
        )

        super().__init__(
            content=ft.Column(
                controls=[
                    # 封面图区域
                    ft.Container(
                        content=ft.Image(
                            src=cover_url,
                            fit="cover",
                            border_radius=ft.border_radius.only(
                                top_left=12, top_right=12
                            ),
                            error_content=ft.Container(
                                content=ft.Icon(
                                    ft.Icons.IMAGE_NOT_SUPPORTED,
                                    size=40,
                                    color=ft.Colors.GREY_400,
                                ),
                                alignment=ft.Alignment(0, 0),
                            ),
                        ),
                        height=180,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        border_radius=ft.border_radius.only(
                            top_left=12, top_right=12
                        ),
                    ),
                    # 信息区域
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    title,
                                    size=13,
                                    weight=ft.FontWeight.W_600,
                                    max_lines=2,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                    color=ft.Colors.WHITE,
                                ),
                                ft.Text(
                                    circle_name,
                                    size=11,
                                    color=ft.Colors.WHITE54,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.STAR_ROUNDED,
                                            size=14,
                                            color=rate_color,
                                        ),
                                        ft.Text(
                                            f"{rate}",
                                            size=12,
                                            color=rate_color,
                                            weight=ft.FontWeight.W_600,
                                        ),
                                        ft.Container(expand=True),
                                        ft.Icon(
                                            ft.Icons.DOWNLOAD_ROUNDED,
                                            size=12,
                                            color=ft.Colors.WHITE38,
                                        ),
                                        ft.Text(
                                            f"{dl_count}",
                                            size=11,
                                            color=ft.Colors.WHITE38,
                                        ),
                                    ],
                                    spacing=4,
                                ),
                            ],
                            spacing=4,
                        ),
                        padding=ft.padding.only(left=10, right=10, top=8, bottom=10),
                    ),
                ],
                spacing=0,
            ),
            border_radius=12,
            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            on_click=self._handle_click,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            on_hover=self._handle_hover,
        )

    def _handle_click(self, e):
        if self._on_click:
            self._on_click(self.work)

    def _handle_hover(self, e):
        if e.data == "true":
            self.scale = 1.03
            self.shadow = ft.BoxShadow(
                spread_radius=1,
                blur_radius=16,
                color=ft.Colors.with_opacity(0.4, ft.Colors.DEEP_PURPLE),
                offset=ft.Offset(0, 4),
            )
        else:
            self.scale = 1.0
            self.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            )
        self.update()
