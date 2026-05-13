from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button, DataTable, Static
from textual.containers import Center, Horizontal, HorizontalScroll
from ui.banners import generateBanner
from db import fetchQualifyingResults

class QualifyingResultsTableScreen(Screen):
    def __init__(self, seasons_selected, circuits_selected, drivers_selected, **kwargs):
        super().__init__(**kwargs)
        self.seasons_selected = seasons_selected
        self.circuits_selected = circuits_selected
        self.drivers_selected = drivers_selected

    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
        with Center():
            yield Static(generateBanner("Qualifying Results"), classes="banner")
        with HorizontalScroll():
                yield DataTable(id="qualifying-results-table")
        with Center():
            yield Horizontal(
                    Button("Home", id="home-button"),
                    Button("Exit", id="exit-button", classes="gap-left"),  
                )
    
    def on_mount(self):
        results = fetchQualifyingResults(self)
        data_table = self.query_one(DataTable)
        data_table.add_columns("Session Date", "Driver Code", "First Name", "Last Name", "Circuit", "Position", "Q1", "Q2", "Q3")
        data_table.cursor_type = "row"
        data_table.zebra_stripes = True
        for r in results:
            data_table.add_row(str(r.session_date), r.driver_code, r.first_name, r.last_name, r.circuit_name, r.position, r.Q1_time, r.Q2_time, r.Q3_time)

    def on_button_pressed(self, event):
        if event.button.id == "home-button":
            from ui.home import HomeScreen
            self.app.push_screen(HomeScreen())
        
        elif event.button.id == "exit-button":
            self.app.exit()