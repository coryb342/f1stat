from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button, DataTable, Static
from textual.containers import Center, Vertical, Horizontal
from ui.banners import generateBanner

class DriversTableScreen(Screen):
    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
        with Center():
            yield Static(generateBanner("Drivers"), classes="banner")
        with Center():
            yield Vertical(
                DataTable(id="drivers-table"),
            )
        with Center():
            yield Horizontal(
                    Button("Back to Home", id="back-button"),
                    Button("Exit", id="exit-button", classes="gap-left"),  
                )
    
    def on_mount(self):
        data_table = self.query_one(DataTable)
        data_table.add_columns("Driver Code", "First Name", "Last Name", "Nationality")
        data_table.cursor_type = "row"
        data_table.zebra_stripes = True
        for d in self.app.drivers:
            data_table.add_row(d.driver_code, d.first_name, d.last_name, d.nationality)

    def on_button_pressed(self, event):
        if event.button.id == "back-button":
            self.app.pop_screen()
        
        elif event.button.id == "exit-button":
            self.app.exit()
