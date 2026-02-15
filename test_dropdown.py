import flet as ft

def main(page):
    try:
        dd = ft.Dropdown(on_change=lambda e: print("change"))
        page.add(dd)
        page.add(ft.Text("Dropdown OK"))
    except Exception as e:
        print(f"Dropdown error: {e}")
        import traceback
        traceback.print_exc()

ft.app(target=main)
