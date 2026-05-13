from textual.screen import Screen
from textual.widgets import Button, Input, Static
from textual.containers import Vertical, Horizontal, Center
import bcrypt
from ui.home import HomeScreen
from ui.register import RegisterScreen
from ui.banners import generateBanner
from db import findUser

class LoginScreen(Screen):
    CSS_PATH = "styles.tcss"
    def __init__(self, message = "", **kwargs):
        super().__init__(**kwargs)
        self.message = message

    def handle_message(self, message):
        if message:
            self.query_one("#error-message", Static).update("")
            self.query_one("#success-message", Static).update(message)
            self.query_one("#email-input", Input).focus()
            self.query_one("#password-input", Input).value = ""

    def compose(self):
        with Center():
            yield Static(generateBanner("Login"), classes="banner")
        with Center():
            yield Vertical(
                Static("", id="error-message", classes="error"),
                Static("", id="success-message", classes="success"),
                Input(placeholder="Email", id="email-input"),
                Input(placeholder="Password", password=True, id="password-input"),
            )
        with Center():
            yield Horizontal(
                    Button("Login", id="login-button"),
                    Button("Register", id="register-button", classes="gap-left"),
                    Button("Exit", id="exit-button", classes="gap-left"),
                )
        
    def on_button_pressed(self, event):
        if event.button.id == "login-button":
            email = self.query_one("#email-input", Input).value
            password = self.query_one("#password-input", Input).value
            error = self.query_one("#error-message", Static)

            user = findUser(self, email)

            if not user:
                error.update("No user found with that email")
                self.query_one("#email-input", Input).value = ""
                self.query_one("#password-input", Input).value = ""
                self.query_one("#email-input", Input).focus()
                return

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                self.app.user = user
                self.app.push_screen(HomeScreen(), self.handle_message)
            else:
                error.update("Incorrect password")
                self.query_one("#password-input", Input).value = ""
                self.query_one("#password-input", Input).focus()
                return

        elif event.button.id == "register-button":
            self.app.push_screen(RegisterScreen(), self.handle_message)

        elif event.button.id == "exit-button":
            self.app.exit()

    