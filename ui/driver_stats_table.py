from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button, DataTable, Static
from textual.containers import Center, Vertical, Horizontal
from ui.banners import generateBanner
from db import establish_connection
from models.driver import Driver
from models.qualifying_result import Qualifying_Result
from models.race_result import Race_Result
from models.session import Session
from sqlalchemy import select, func

db_conn = establish_connection()


class DriversStatsTableScreen(Screen):
    def __init__(self, seasons, stats, drivers, **kwargs):
        super().__init__(**kwargs)
        self.seasons = seasons
        self.stats = stats
        self.drivers = drivers

    def fetch_stats(self):
        pole_results = {}
        wins_results = {}
        fastest_lap_results = {}
        points_results = {}
        podiums_results = {}

        pole_stmt = (
            select(Qualifying_Result.driver_code, func.count(Qualifying_Result.position).label("pole_positions"))
            .join(Session, Qualifying_Result.session_id == Session.session_id)
            .where(Qualifying_Result.driver_code.in_(self.drivers))
            .where(Qualifying_Result.position == 1)
            .where(Session.season.in_(self.seasons))
            .group_by(Qualifying_Result.driver_code)
        ) 
        wins_stmt = (
            select(Race_Result.driver_code, func.count(Race_Result.position).label("wins"))
            .join(Session, Race_Result.session_id == Session.session_id)
            .where(Race_Result.driver_code.in_(self.drivers))
            .where(Race_Result.position == 1)
            .where(Session.season.in_(self.seasons))
            .group_by(Race_Result.driver_code)
        )
        fastest_lap_stmt = (
            select(Race_Result.driver_code, func.min(Race_Result.fastest_lap_time).label("fastest_lap"))
            .join(Session, Race_Result.session_id == Session.session_id)
            .where(Race_Result.driver_code.in_(self.drivers))
            .where(Race_Result.fastest_lap_time != "NA")
            .where(Session.season.in_(self.seasons))
            .group_by(Race_Result.driver_code)
        )
        points_stmt = (
            select(Race_Result.driver_code, func.sum(Race_Result.points_earned).label("total_points"))
            .join(Session, Race_Result.session_id == Session.session_id)
            .where(Race_Result.driver_code.in_(self.drivers))
            .where(Session.season.in_(self.seasons))
            .group_by(Race_Result.driver_code)
        )
        podiums_stmt = (
            select(Race_Result.driver_code, func.count(Race_Result.position).label("podiums"))
            .join(Session, Race_Result.session_id == Session.session_id)
            .where(Race_Result.driver_code.in_(self.drivers))
            .where(Race_Result.position <= 3)
            .where(Session.season.in_(self.seasons))
            .group_by(Race_Result.driver_code)
        )

        if "pole_positions" in self.stats:
            pole_results = {r.driver_code: r.pole_positions for r in db_conn.execute(pole_stmt).all()}
        if "wins" in self.stats:
            wins_results = {r.driver_code: r.wins for r in db_conn.execute(wins_stmt).all()}
        if "points" in self.stats:
            points_results = {r.driver_code: r.total_points for r in db_conn.execute(points_stmt).all()}
        if "fastest_lap" in self.stats:
            fastest_lap_results = {r.driver_code: r.fastest_lap for r in db_conn.execute(fastest_lap_stmt).all()}
        if "podiums" in self.stats:
            podiums_results = {r.driver_code: r.podiums for r in db_conn.execute(podiums_stmt).all()}

        return pole_results, wins_results, fastest_lap_results, points_results, podiums_results

    def build_table(self):
        data_table = self.query_one(DataTable)
        data_table.add_columns("Driver Code", "First Name", "Last Name")

        if "pole_positions" in self.stats:
            data_table.add_column("Pole Positions")
        if "wins" in self.stats:
            data_table.add_column("Wins")
        if "points" in self.stats:
            data_table.add_column("Points")
        if "fastest_lap" in self.stats:
            data_table.add_column("Fastest Lap")
        if "podiums" in self.stats:
            data_table.add_column("Podiums")

        data_table.cursor_type = "row"
        data_table.zebra_stripes = True

        pole_results, wins_results, fastest_lap_results, points_results, podiums_results = self.fetch_stats()

        for driver_code in self.drivers:
            driver = db_conn.execute(select(Driver).where(Driver.driver_code == driver_code)).scalars().first()
        
            row = [driver.driver_code, driver.first_name, driver.last_name]

            if "pole_positions" in self.stats:
                row.append(str(pole_results.get(driver_code, 0)))
            if "wins" in self.stats:
                row.append(str(wins_results.get(driver_code, 0)))
            if "points" in self.stats:
                row.append(str(points_results.get(driver_code, 0)))
            if "fastest_lap" in self.stats:
                row.append(str(fastest_lap_results.get(driver_code, "N/A")))
            if "podiums" in self.stats:
                row.append(str(podiums_results.get(driver_code, 0)))

            data_table.add_row(*row)

    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
        with Center():
            yield Static(generateBanner("Driver Stats"), classes="banner")
        with Center():
            yield Vertical(
                DataTable(id="driver-stats-table"),
            )
        with Center():
            yield Horizontal(
                    Button("Home", id="home-button"),
                    Button("Exit", id="exit-button", classes="gap-left"),  
                )
    
    def on_mount(self):
        self.build_table()
        
    def on_button_pressed(self, event):
        if event.button.id == "home-button":
            from ui.home import HomeScreen
            self.app.push_screen(HomeScreen())
        
        elif event.button.id == "exit-button":
            self.app.exit()