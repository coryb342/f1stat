from sqlalchemy import select
from textual.screen import Screen
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option
from textual.containers import Center, Vertical
from db import establish_connection
from models.driver import Driver
from ui.banners import generateBanner
from ui.circuits_table import CircuitsTableScreen
from ui.drivers_table import DriversTableScreen
from ui.driver_select import DriverSelectScreen

db_conn = establish_connection()

class HomeScreen(Screen):
    CSS_PATH = "styles.tcss"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = self.app.user

    def greet_user(self, user):
        favorite_driver_stmt = select(Driver).where(Driver.driver_code == user.favorite_driver)
        favorite_driver = db_conn.execute(favorite_driver_stmt).scalars().first()
        self.query_one("#welcome-message", Static).update(f"Welcome, {user.first_name} {user.last_name}!")
        self.query_one("#favorite-driver", Static).update(f"Your favorite driver, {favorite_driver.first_name} {favorite_driver.last_name}, says hello!")

    def compose(self):
        with Center():
            yield Static(generateBanner("Home"), classes="banner")
        with Center():
            yield Vertical(
                Static("", id="welcome-message"),
                Static("", id="favorite-driver"),
                OptionList(
                    Option("View Drivers", id="view-drivers-option"),
                    Option("View Circuits", id="view-circuits-option"),
                    Option("Driver Stats", id="driver-stats-option"),
                    Option("Session Results", id="session-results-option"),
                    Option("Logout", id="logout-option"),
                    Option("Exit", id="exit-option"),
                )
            )
    
    def on_mount(self):
        self.greet_user(self.user)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        if event.option.id == "logout-option":
            self.app.user = None
            from ui.login import LoginScreen
            self.app.push_screen(LoginScreen("Successfully Logged Out"))
        
        elif event.option.id == "exit-option":
            self.app.exit()

        elif event.option.id == "view-drivers-option":
            self.app.push_screen(DriversTableScreen())

        elif event.option.id == "view-circuits-option":
            self.app.push_screen(CircuitsTableScreen())

        elif event.option.id == "driver-stats-option":
            self.app.push_screen(DriverSelectScreen())
        
        elif event.option.id == "session-results-option":
            from ui.session_results_select import SessionResultsSelectScreen
            self.app.push_screen(SessionResultsSelectScreen())