import flet as ft
class AudioPlayer(ft.Container):
    """底部音频播放条"""

    def __init__(self):
        # Audio 是 Service 类型，需要在 page 存在后才能创建，延迟到 play() 中初始化
        self.audio = None
        self.is_playing = False
        self.duration_ms = 0
        self.position_ms = 0
        self.current_title = ""

        self.title_text = ft.Text(
            "未在播放",
            size=13,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.W_500,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
            expand=True,
        )

        self.play_btn = ft.IconButton(
            icon=ft.Icons.PLAY_CIRCLE_FILLED_ROUNDED,
            icon_size=36,
            icon_color=ft.Colors.DEEP_PURPLE_ACCENT_100,
            on_click=self._toggle_play,
        )

        self.progress = ft.ProgressBar(
            value=0,
            height=3,
            color=ft.Colors.DEEP_PURPLE_ACCENT_100,
            bgcolor=ft.Colors.WHITE12,
        )

        self.time_text = ft.Text(
            "0:00 / 0:00",
            size=11,
            color=ft.Colors.WHITE38,
        )

        super().__init__(
            content=ft.Column(
                controls=[
                    self.progress,
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.Icons.MUSIC_NOTE_ROUNDED,
                                    size=20,
                                    color=ft.Colors.DEEP_PURPLE_ACCENT_100,
                                ),
                                self.title_text,
                                self.time_text,
                                self.play_btn,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        padding=ft.padding.symmetric(horizontal=12, vertical=4),
                    ),
                ],
                spacing=0,
            ),
            bgcolor=ft.Colors.with_opacity(0.85, "#1a1a2e"),
            blur=ft.Blur(10, 10),
            visible=False,
        )

    def _ensure_audio(self, page: ft.Page):
        """确保 Audio Service 已创建（必须在 page 上下文中）"""
        if self.audio is not None:
            return
        self.audio = ft.Audio(
            src="",
            autoplay=False,
            on_position_changed=self._on_position_change,
            on_state_changed=self._on_state_change,
            on_duration_changed=self._on_duration_change,
        )
        page.overlay.append(self.audio)
        page.update()

    def play(self, url: str, title: str, page: ft.Page):
        """播放指定音频"""
        try:
            self._ensure_audio(page)
            self.current_title = title
            self.title_text.value = title
            self.audio.src = url
            self.audio.autoplay = True
            self.is_playing = True
            self.play_btn.icon = ft.Icons.PAUSE_CIRCLE_FILLED_ROUNDED
            self.visible = True
            page.update()
        except Exception as e:
            print(f"Play Error: {e}")
            page.snack_bar = ft.SnackBar(ft.Text(f"播放出错: {e}"), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()

    def _toggle_play(self, e):
        try:
            if self.audio is None:
                return
            if self.is_playing:
                self.audio.pause()
                self.play_btn.icon = ft.Icons.PLAY_CIRCLE_FILLED_ROUNDED
                self.is_playing = False
            else:
                self.audio.resume()
                self.play_btn.icon = ft.Icons.PAUSE_CIRCLE_FILLED_ROUNDED
                self.is_playing = True
            self.update()
        except Exception as e:
            print(f"Toggle Error: {e}")
            if self.page:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"切换播放出错: {e}"), bgcolor=ft.Colors.RED)
                self.page.snack_bar.open = True
                self.page.update()

    def _on_position_change(self, e):
        self.position_ms = int(e.position)
        if self.duration_ms > 0:
            self.progress.value = self.position_ms / self.duration_ms
        self.time_text.value = (
            f"{self._fmt(self.position_ms)} / {self._fmt(self.duration_ms)}"
        )
        self.update()

    def _on_state_change(self, e):
        if e.state == "completed":
            self.is_playing = False
            self.play_btn.icon = ft.Icons.PLAY_CIRCLE_FILLED_ROUNDED
            self.progress.value = 0
            self.update()

    def _on_duration_change(self, e):
        self.duration_ms = int(e.duration)

    @staticmethod
    def _fmt(ms: int) -> str:
        """毫秒 → m:ss"""
        s = ms // 1000
        return f"{s // 60}:{s % 60:02d}"
