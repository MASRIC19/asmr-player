import flet as ft
from components.audio_player import AudioPlayer

async def main(page: ft.Page):
    try:
        print("Creating AudioPlayer...")
        page.add(ft.Text("Creating AudioPlayer..."))
        try:
            ap = AudioPlayer()
            print("AudioPlayer created.")
            page.add(ft.Text("AudioPlayer created."))
            page.overlay.append(ap) # Add visual part
            # Wait, AudioPlayer inherits from Container, so it IS visual?
            # Yes. so page.add(ap)? or page.overlay.append(ap)? 
            # It's a bottom sheet like thing.
            # In main.py: page.add(ft.Stack(..., ft.Container(content=audio_player...)))
            # So it is added to visual tree.
            
            # The issue might be inside AudioPlayer.__init__ where it creates fta.Audio.
            page.update()
        except Exception as e:
            page.add(ft.Text(f"Error creating AudioPlayer: {e}"))
            import traceback
            traceback.print_exc()

    except Exception as e:
        print(f"Main Error: {e}")

ft.app(target=main)
