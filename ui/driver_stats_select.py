from textual.screen import Screen
from textual.widgets import Button, Pretty, SelectionList, Static
from textual.containers import Center, Vertical, Horizontal
from ui.banners import generateBanner
from textual import on
from textual.events import Mount

class DriverStatsSelectScreen(Screen):
    def __init__(self, selected_drivers, **kwargs):
        super().__init__(**kwargs)
        self.drivers_selected = selected_drivers

    CSS_PATH = "styles.tcss"

    def compose(self):
        with Center():
            yield Static(generateBanner("Driver Stats"), classes="banner")
        with Center():
            yield Pretty("", id="selected-drivers-pretty")
            yield Horizontal(
                Vertical(
                    SelectionList(
                        ("Number of Pole Postions", "pole_positions"),
                        ("Number of Wins", "wins"),
                        ("Points Earned", "points"),
                        ("Fastest Lap", "fastest_lap"),
                        ("Number of Podiums", "podiums"),
                        id="stats-selection-list"
                    ),
                    Pretty([], id="selected-stats-pretty")
                ),
                Vertical(
                    SelectionList(
                        ("2023", 2023),
                        ("2024", 2024),
                        ("2025", 2025),
                        id="season-selection-list"
                    ),
                    Pretty([], id="selected-season-pretty")
                )
            )
        with Center():
            yield Horizontal(
                    Button("Fetch Stats", id="fetch-stats-button"),
                    Button("Back", id="back-button", classes="gap-left"),
                    Button("Exit", id="exit-button", classes="gap-left"),  
                )
    
    def on_mount(self) -> None:
        self.query_one("#stats-selection-list", SelectionList).border_title = "Select Stats"
        self.query_one("#season-selection-list", SelectionList).border_title = "Select Season"
        self.query_one("#selected-stats-pretty", Pretty).border_title = "Selected Stats"
        self.query_one("#selected-season-pretty", Pretty).border_title = "Selected Season"
        self.query_one("#selected-drivers-pretty", Pretty).border_title = "Selected Drivers"
        self.query_one("#selected-drivers-pretty", Pretty).update(self.drivers_selected)

    
    @on(Mount)
    @on(SelectionList.SelectedChanged, "#stats-selection-list")
    def update_stats_selected_view(self) -> None:
        self.query_one("#selected-stats-pretty", Pretty).update(self.query_one("#stats-selection-list", SelectionList).selected)

    @on(SelectionList.SelectedChanged, "#season-selection-list")
    def update_season_selected_view(self) -> None:
        self.query_one("#selected-season-pretty", Pretty).update(self.query_one("#season-selection-list", SelectionList).selected)

    def on_button_pressed(self, event):
        if event.button.id == "back-button":
            self.app.pop_screen()
        
        elif event.button.id == "exit-button":
            self.app.exit()

        elif event.button.id == "fetch-stats-button":
            seasons_selected = self.query_one("#season-selection-list", SelectionList).selected
            stats_selected = self.query_one("#stats-selection-list", SelectionList).selected
            from ui.driver_stats_table import DriversStatsTableScreen
            self.app.push_screen(DriversStatsTableScreen(seasons_selected, stats_selected, self.drivers_selected))
