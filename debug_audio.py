import flet as ft
import flet_audio as fta

# Define AudioPlayer inline to debug
class DebugAudioPlayer(ft.Container):
    def __init__(self):
        print("DebugAudioPlayer init start")
@ft.control("audio")
class MyAudio(fta.Audio):
    pass

class DebugAudioPlayer(ft.Container):
    def __init__(self):
        print("DebugAudioPlayer init start")
        try:
            self.audio = MyAudio(
                src="https://luan.xyz/files/audio/ambient_c_motion.mp3",
                autoplay=False,
                on_position_change=self._on_position_change,
                on_state_change=self._on_state_change,
                on_duration_change=self._on_duration_change,
            )
            print("Audio created")
        except Exception as e:
            print(f"Audio creation failed: {e}")
            raise

        super().__init__(
            content=ft.Text("Debug Player"),
            bgcolor=ft.Colors.BLUE,
        )
        print("DebugAudioPlayer init done")

    def _on_position_change(self, e):
        print(f"pos: {e.data}")

    def _on_state_change(self, e):
        print(f"state: {e.data}")

    def _on_duration_change(self, e):
        print(f"duration: {e.data}")

def main(page: ft.Page):
    print("Main start")
    try:
        player = DebugAudioPlayer()
        page.add(player)
        page.overlay.append(player.audio) # 0.80+ way?
        # or page.services.append(player.audio) if available
        if hasattr(page, "services"):
             page.services.append(player.audio)
        else:
             page.overlay.append(player.audio)
             
        page.add(ft.Text("Player added"))
    except Exception as e:
        print(f"Main error: {e}")
        import traceback
        traceback.print_exc()

ft.app(target=main)
