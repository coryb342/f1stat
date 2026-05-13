from textual.screen import Screen
from textual.widgets import Button, Pretty, SelectionList, Static
from textual.containers import Center, Horizontal
from ui.banners import generateBanner
from textual import on
from textual.events import Mount
from ui.driver_stats_select import DriverStatsSelectScreen


class DriverSelectScreen(Screen):
    CSS_PATH = "styles.tcss"
    all_selected = False
    select_all_text = "Select All"

    def compose(self):
        with Center():
            yield Static(generateBanner("Driver Stats"), classes="banner")
        with Center():
            yield Button(f"{self.select_all_text}", id="select-all-button")
            yield Horizontal(
                SelectionList(
                    *[(f"{d.first_name} {d.last_name}", d.driver_code) for d in self.app.drivers]
                ),
                Pretty([])
            )
        with Center():
            yield Horizontal(
                    Button("Continue", id="continue-button"),
                    Button("Back to Home", id="back-button", classes="gap-left"),
                    Button("Exit", id="exit-button", classes="gap-left"),  
                )
    
    def on_mount(self) -> None:
        self.query_one(SelectionList).border_title = "Which Driver(s) Would You Like to View Stats for?"
        self.query_one(Pretty).border_title = "Selected Drivers"
    
    @on(Mount)
    @on(SelectionList.SelectedChanged)
    def update_selected_view(self) -> None:
        self.query_one(Pretty).update(self.query_one(SelectionList).selected)

    def on_button_pressed(self, event):
        if event.button.id == "back-button":
            self.app.pop_screen()
        
        elif event.button.id == "exit-button":
            self.app.exit()
        
        elif event.button.id == "select-all-button":
            if not self.all_selected:
                self.query_one(SelectionList).select_all()
                self.query_one("#select-all-button", Button).label = "Deselect All"
                self.update_selected_view()
            else:
                self.query_one(SelectionList).deselect_all()
                self.query_one("#select-all-button", Button).label = "Select All"
                self.update_selected_view()
            self.all_selected = not self.all_selected

        elif event.button.id == "continue-button":
            selected_drivers = self.query_one(SelectionList).selected
            if not selected_drivers:
                return
            self.app.push_screen(DriverStatsSelectScreen(selected_drivers))