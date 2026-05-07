from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button, DataTable, Static
from textual.containers import Center, Vertical, Horizontal
from models.circuit import Circuit
from ui.banners import generateBanner
from db import establish_connection
from sqlalchemy import select

db_conn = establish_connection()
circuit_stmt = select(Circuit).order_by(Circuit.circuit_name)
circuits = db_conn.execute(circuit_stmt).scalars().all()

class CircuitsTableScreen(Screen):
    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
        with Center():
            yield Static(generateBanner("Circuits"), classes="banner")
        with Center():
            yield Vertical(
                DataTable(id="circuits-table")
            )
        with Center():
            yield Horizontal(
                    Button("Back to Home", id="back-button"),
                    Button("Exit", id="exit-button", classes="gap-left"),
                )
                 
    
    def on_mount(self):
        data_table = self.query_one(DataTable)
        data_table.add_columns("Circuit Name", "Location", "Country")
        data_table.cursor_type = "row"
        data_table.zebra_stripes = True
        for c in circuits:
            data_table.add_row(c.circuit_name, c.location, c.country)

    def on_button_pressed(self, event):
        if event.button.id == "back-button":
            self.app.pop_screen()
        
        elif event.button.id == "exit-button":
            self.app.exit()