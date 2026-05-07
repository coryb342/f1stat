from textual.screen import Screen
from textual.widgets import Button, Input, Static, Select
from textual.containers import Center, Vertical, Horizontal
from db import establish_connection
from models.user import User
from models.driver import Driver
from sqlalchemy import select
import bcrypt
from ui.banners import generateBanner

db_conn = establish_connection()
driver_stmt = select(Driver).order_by(Driver.last_name)
drivers = db_conn.execute(driver_stmt).scalars().all()

class RegisterScreen(Screen):
    CSS_PATH = "styles.tcss"

    def compose(self):
        with Center():
            yield Static(generateBanner("Register"), classes="banner")
        with Center():
            yield Vertical(
                Static("", id="error-message", classes="error"),
                Input(placeholder="Email", id="email-input"),
                Input(placeholder="First Name", id="first-name-input"),
                Input(placeholder="Last Name", id="last-name-input"),
                Input(placeholder="Password", password=True, id="password-input"),
                Select(id="favorite-driver-input", options=[(f"{driver.first_name} {driver.last_name}", driver.driver_code) for driver in drivers], prompt="Select Favorite Driver", classes="verticalSelect"),  
            )
        with Center():
            yield Horizontal(
                    Button("Register", id="register-button"),
                    Button("Back to Login", id="back-button", classes="gap-left"),
                    Button("Exit", id="exit-button", classes="gap-left"),
                )
            
        
    def on_button_pressed(self, event):
        if event.button.id == "register-button":
            email = self.query_one("#email-input", Input).value
            first_name = self.query_one("#first-name-input", Input).value
            last_name = self.query_one("#last-name-input", Input).value
            password = self.query_one("#password-input", Input).value
            favorite_driver = self.query_one("#favorite-driver-input", Select).value
            error = self.query_one("#error-message", Static)

            if not email or not password or not first_name or not last_name or not favorite_driver:
                error.update("All fields are required")
                return

            stmt = select(User).where(User.email == email)
            existing_user = db_conn.execute(stmt).scalars().first()

            if existing_user:
                error.update("A user with that email already exists")
                self.query_one("#email-input", Input).focus()
                return

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                favorite_driver=favorite_driver,
                password=hashed_password.decode('utf-8')
            )

            db_conn.add(new_user)
            db_conn.commit()

            self.dismiss("Registration successful! Please log in.")

        elif event.button.id == "back-button":
            self.app.pop_screen()
        
        elif event.button.id == "exit-button":
            self.app.exit()