from textual.app import App
from ui.login import LoginScreen

class F1StatsApp(App):
    def __init__(self):
        super().__init__()
        self.user = None
    def on_mount(self):
        self.push_screen(LoginScreen())

if __name__ == "__main__":
    F1StatsApp().run()