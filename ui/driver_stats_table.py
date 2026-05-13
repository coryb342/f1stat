from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button, DataTable, Static
from textual.containers import Center, Vertical, Horizontal
from ui.banners import generateBanner
from db import fetchStats, findDriverByCode


class DriversStatsTableScreen(Screen):
    def __init__(self, seasons_selected, stats_selected, drivers_selected, **kwargs):
        super().__init__(**kwargs)
        self.seasons_selected = seasons_selected
        self.stats_selected = stats_selected
        self.drivers_selected = drivers_selected

    def build_table(self):
        data_table = self.query_one(DataTable)
        data_table.add_columns("Driver Code", "First Name", "Last Name")

        if "pole_positions" in self.stats_selected:
            data_table.add_column("Pole Positions")
        if "wins" in self.stats_selected:
            data_table.add_column("Wins")
        if "points" in self.stats_selected:
            data_table.add_column("Points")
        if "fastest_lap" in self.stats_selected:
            data_table.add_column("Fastest Lap")
        if "podiums" in self.stats_selected:
            data_table.add_column("Podiums")

        data_table.cursor_type = "row"
        data_table.zebra_stripes = True

        pole_results, wins_results, fastest_lap_results, points_results, podiums_results = fetchStats(self)

        for driver_code in self.drivers_selected:
            driver = findDriverByCode(self, driver_code)
        
            row = [driver.driver_code, driver.first_name, driver.last_name]

            if "pole_positions" in self.stats_selected:
                row.append(str(pole_results.get(driver_code, 0)))
            if "wins" in self.stats_selected:
                row.append(str(wins_results.get(driver_code, 0)))
            if "points" in self.stats_selected:
                row.append(str(points_results.get(driver_code, 0)))
            if "fastest_lap" in self.stats_selected:
                row.append(str(fastest_lap_results.get(driver_code, "N/A")))
            if "podiums" in self.stats_selected:
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