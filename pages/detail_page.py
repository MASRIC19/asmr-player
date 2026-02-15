"""
作品详情页
展示作品详细信息和音轨列表，支持音频播放。
"""

import flet as ft
from asmr_api import AsmrApi


class DetailPage(ft.Column):
    """作品详情页"""

    def __init__(self, work: dict, audio_player, on_back=None):
        super().__init__(expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)
        self.work = work
        self.audio_player = audio_player
        self._on_back = on_back
        self._tracks = []

        work_id = work.get("id", 0)
        title = work.get("title", "未知作品")
        circle_name = work.get("circle", {}).get("name", "")
        rate = work.get("rate_average_2dp", 0)
        dl_count = work.get("dl_count", 0)
        price = work.get("price", 0)
        tags = work.get("tags", [])

        cover_url = f"https://api.asmr-200.com/api/cover/{work_id}.jpg?type=main"

        # 评分颜色
        rate_color = (
            ft.Colors.AMBER if rate >= 4.0
            else ft.Colors.ORANGE if rate >= 3.0
            else ft.Colors.GREY
        )

        # 标签
        tag_chips = []
        for t in tags[:10]:
            tag_name = t.get("name", "") if isinstance(t, dict) else str(t)
            if tag_name:
                tag_chips.append(
                    ft.Container(
                        content=ft.Text(tag_name, size=11, color=ft.Colors.DEEP_PURPLE_ACCENT_100),
                        padding=ft.padding.symmetric(horizontal=10, vertical=4),
                        border_radius=12,
                        bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.DEEP_PURPLE),
                    )
                )

        # 音轨列表容器
        self.tracks_column = ft.Column(spacing=2)
        self.tracks_loading = ft.Container(
            content=ft.ProgressRing(width=24, height=24, color=ft.Colors.DEEP_PURPLE_ACCENT_100),
            alignment=ft.Alignment(0, 0),
            padding=20,
        )

        # 返回按钮
        back_btn = ft.IconButton(
            icon=ft.Icons.ARROW_BACK_ROUNDED,
            icon_color=ft.Colors.WHITE,
            on_click=self._go_back,
        )

        # 构建页面
        self.controls = [
            # 顶部返回栏
            ft.Container(
                content=ft.Row(
                    controls=[
                        back_btn,
                        ft.Text(
                            "作品详情",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.WHITE,
                        ),
                    ],
                    spacing=4,
                ),
                padding=ft.padding.only(left=4, right=16, top=8, bottom=0),
            ),
            # 封面区域
            ft.Container(
                content=ft.Image(
                    src=cover_url,
                    fit="cover",
                    border_radius=16,
                    error_content=ft.Container(
                        content=ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED, size=60, color=ft.Colors.GREY_400),
                        alignment=ft.Alignment(0, 0),
                        height=250,
                    ),
                ),
                height=250,
                width=float("inf"),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                border_radius=16,
                margin=ft.margin.symmetric(horizontal=16, vertical=8),
                shadow=ft.BoxShadow(
                    spread_radius=0, blur_radius=20,
                    color=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
                    offset=ft.Offset(0, 8),
                ),
            ),
            # 信息区
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            title,
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                        ft.Text(
                            circle_name,
                            size=13,
                            color=ft.Colors.WHITE54,
                        ),
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.STAR_ROUNDED, size=18, color=rate_color),
                                ft.Text(f"{rate}", size=15, color=rate_color, weight=ft.FontWeight.W_600),
                                ft.Container(width=16),
                                ft.Icon(ft.Icons.DOWNLOAD_ROUNDED, size=15, color=ft.Colors.WHITE38),
                                ft.Text(f"{dl_count}", size=13, color=ft.Colors.WHITE38),
                                ft.Container(width=16),
                                ft.Icon(ft.Icons.SELL_ROUNDED, size=15, color=ft.Colors.WHITE38),
                                ft.Text(f"¥{price}" if price else "免费", size=13, color=ft.Colors.WHITE38),
                            ],
                            spacing=4,
                        ),
                        # 标签
                        ft.Row(
                            controls=tag_chips,
                            wrap=True,
                            spacing=6,
                            run_spacing=6,
                        ) if tag_chips else ft.Container(),
                    ],
                    spacing=8,
                ),
                padding=ft.padding.symmetric(horizontal=20, vertical=8),
            ),
            # 音轨列表标题
            ft.Container(
                content=ft.Text(
                    "🎵 音轨列表",
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.WHITE,
                ),
                padding=ft.padding.only(left=20, top=16, bottom=8),
            ),
            self.tracks_loading,
            ft.Container(
                content=self.tracks_column,
                padding=ft.padding.only(left=12, right=12, bottom=100),
            ),
        ]

    async def load_tracks(self, page: ft.Page):
        """加载音轨列表"""
        work_id = self.work.get("id", 0)
        try:
            async with AsmrApi() as api:
                tracks = await api.get_tracks(work_id)
            self._tracks = tracks
            self._build_track_list(tracks, page)
        except Exception as e:
            self.tracks_column.controls.append(
                ft.Text(f"加载音轨失败: {e}", color=ft.Colors.RED_300)
            )
        finally:
            self.tracks_loading.visible = False
            self.update()

    def _build_track_list(self, items: list, page: ft.Page, depth: int = 0):
        """递归构建音轨列表（支持文件夹嵌套）"""
        for item in items:
            item_type = item.get("type", "")
            title = item.get("title", "未知")

            if item_type == "folder":
                # 文件夹
                self.tracks_column.controls.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.FOLDER_ROUNDED, size=18, color=ft.Colors.AMBER),
                                ft.Text(
                                    title, size=13,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.WHITE70,
                                ),
                            ],
                            spacing=8,
                        ),
                        padding=ft.padding.only(left=20 + depth * 16, top=8, bottom=4),
                    )
                )
                children = item.get("children", [])
                if children:
                    self._build_track_list(children, page, depth + 1)
            else:
                # 音频文件
                media_url = item.get("mediaStreamUrl", "") or item.get("mediaDownloadUrl", "")
                duration_text = ""
                duration = item.get("duration", 0)
                if duration:
                    m, s = divmod(int(duration), 60)
                    duration_text = f"{m}:{s:02d}"

                is_audio = any(
                    title.lower().endswith(ext)
                    for ext in (".mp3", ".wav", ".flac", ".m4a", ".ogg", ".aac")
                )

                icon = ft.Icons.AUDIOTRACK_ROUNDED if is_audio else ft.Icons.INSERT_DRIVE_FILE_ROUNDED
                icon_color = ft.Colors.DEEP_PURPLE_ACCENT_100 if is_audio else ft.Colors.WHITE38

                row = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(icon, size=18, color=icon_color),
                            ft.Text(
                                title, size=13,
                                color=ft.Colors.WHITE,
                                expand=True,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(duration_text, size=11, color=ft.Colors.WHITE38),
                            ft.IconButton(
                                icon=ft.Icons.PLAY_ARROW_ROUNDED,
                                icon_size=20,
                                icon_color=ft.Colors.DEEP_PURPLE_ACCENT_100,
                                on_click=lambda e, u=media_url, t=title: self._play_track(u, t, page),
                                visible=bool(media_url and is_audio),
                            ),
                        ],
                        spacing=6,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.only(left=20 + depth * 16, right=8, top=2, bottom=2),
                    border_radius=8,
                    on_hover=lambda e, c=None: self._track_hover(e),
                )
                self.tracks_column.controls.append(row)

    def _play_track(self, url: str, title: str, page: ft.Page):
        if url and hasattr(self.audio_player, "play"):
            self.audio_player.play(url, title, page)

    def _track_hover(self, e):
        e.control.bgcolor = (
            ft.Colors.with_opacity(0.08, ft.Colors.WHITE)
            if e.data == "true" else None
        )
        e.control.update()

    def _go_back(self, e):
        if self._on_back:
            self._on_back()
