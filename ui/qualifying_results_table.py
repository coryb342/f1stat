from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button, DataTable, Static
from textual.containers import Center, Horizontal, HorizontalScroll
from ui.banners import generateBanner
from db import establish_connection
from models.driver import Driver
from models.qualifying_result import Qualifying_Result
from models.session_circuit import Session_Circuit
from models.session import Session
from sqlalchemy import select

db_conn = establish_connection()

class QualifyingResultsTableScreen(Screen):
    def __init__(self, seasons, circuits, drivers, **kwargs):
        super().__init__(**kwargs)
        self.seasons = seasons
        self.circuits = circuits
        self.drivers = drivers

    CSS_PATH = "styles.tcss"

    def fetch_results(self):
        quali_results_stmt = (
            select(
                Session.session_date,
                Qualifying_Result.driver_code,
                Driver.first_name,
                Driver.last_name,
                Session_Circuit.circuit_name,
                Qualifying_Result.position,
                Qualifying_Result.Q1_time,
                Qualifying_Result.Q2_time,
                Qualifying_Result.Q3_time
            )
            .select_from(Qualifying_Result)
            .join(Session, Qualifying_Result.session_id == Session.session_id)
            .join(Session_Circuit, Qualifying_Result.session_id == Session_Circuit.session_id)
            .join(Driver, Qualifying_Result.driver_code == Driver.driver_code)
            .where(Session.season.in_(self.seasons))
            .where(Qualifying_Result.driver_code.in_(self.drivers))
            .where(Session_Circuit.circuit_name.in_(self.circuits))
            .order_by(Session.session_date)
            .order_by(Qualifying_Result.position)
        )

        return db_conn.execute(quali_results_stmt).all()

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
        results = self.fetch_results()
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