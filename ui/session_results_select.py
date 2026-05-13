from textual.screen import Screen
from textual.widgets import Button, Pretty, SelectionList, Static, RadioButton, RadioSet
from textual.containers import Center, Horizontal
from ui.banners import generateBanner
from textual import on
from textual.events import Mount

SESSION_TYPE_MAP = {
    "Race Sessions": "R",
    "Qualifying Sessions": "Q"
}

class SessionResultsSelectScreen(Screen):
    CSS_PATH = "styles.tcss"

    all_drivers_selected = False
    all_circuits_selected = False

    def compose(self):
        with Center():
            yield Static(generateBanner("Session Selector"), classes="banner")
        with Center():
            yield RadioSet(
                RadioButton("Race Sessions", "R"),
                RadioButton("Qualifying Sessions", "Q"),
                id="selected-session-type"
            )
        with Center():
            yield Button("Select All", id="select-all-drivers-button")
            yield Horizontal(
                SelectionList(
                    *[(f"{d.first_name} {d.last_name}", d.driver_code) for d in self.app.drivers], 
                    id="selected-drivers-list"
                ),
                Pretty([], id="selected-drivers-pretty")
            )
            yield Button("Select All", id="select-all-circuits-button")
            yield Horizontal(
                SelectionList(
                    *[(f"{c.circuit_name} {c.country}", c.circuit_name) for c in self.app.circuits], 
                    id="selected-circuits-list"
                ),
                Pretty([], id="selected-circuits-pretty")
            )
            yield Horizontal(
                SelectionList(
                    ("2023", 2023),
                    ("2024", 2024),
                    ("2025", 2025),
                    id="selected-seasons-list"
                ),
                Pretty([], id="selected-seasons-pretty")
            )
        with Center():
            yield Horizontal(
                    Button("Fetch Results", id="fetch-stats-button"),
                    Button("Back", id="back-button", classes="gap-left"),
                    Button("Exit", id="exit-button", classes="gap-left"),  
                )
    
    def on_mount(self) -> None:
        self.query_one("#selected-drivers-list", SelectionList).border_title = "Select Driver(s)"
        self.query_one("#selected-circuits-list", SelectionList).border_title = "Select Circuit(s)"
        self.query_one("#selected-seasons-list", SelectionList).border_title = "Select Season(s)"

        self.query_one("#selected-circuits-pretty", Pretty).border_title = "Selected Circuit(s)"
        self.query_one("#selected-seasons-pretty", Pretty).border_title = "Selected Season(s)"
        self.query_one("#selected-drivers-pretty", Pretty).border_title = "Selected Driver(s)"

        self.session_type = "R"

    
    @on(Mount)
    @on(SelectionList.SelectedChanged, "#selected-drivers-list")
    def update_drivers_selected_view(self) -> None:
        self.query_one("#selected-drivers-pretty", Pretty).update(self.query_one("#selected-drivers-list", SelectionList).selected)

    @on(SelectionList.SelectedChanged, "#selected-seasons-list")
    def update_seasons_selected_view(self) -> None:
        self.query_one("#selected-seasons-pretty", Pretty).update(self.query_one("#selected-seasons-list", SelectionList).selected)

    @on(SelectionList.SelectedChanged, "#selected-circuits-list")
    def update_circuits_selected_view(self) -> None:
        self.query_one("#selected-circuits-pretty", Pretty).update(self.query_one("#selected-circuits-list", SelectionList).selected)

    @on(RadioSet.Changed, "#selected-session-type")
    def handle_session_type(self, event: RadioSet.Changed):
        label = str(event.pressed.label)
        self.session_type = SESSION_TYPE_MAP[label]

    def on_button_pressed(self, event):
        if event.button.id == "back-button":
            self.app.pop_screen()
        
        elif event.button.id == "exit-button":
            self.app.exit()
        
        elif event.button.id == "select-all-drivers-button":
            if not self.all_drivers_selected:
                self.query_one("#selected-drivers-list",SelectionList).select_all()
                self.query_one("#select-all-drivers-button", Button).label = "Deselect All"
                self.update_drivers_selected_view
            else:
                self.query_one("#selected-drivers-list",SelectionList).deselect_all()
                self.query_one("#select-all-drivers-button", Button).label = "Select All"
                self.update_drivers_selected_view()
            self.all_drivers_selected = not self.all_drivers_selected

        elif event.button.id == "select-all-circuits-button":
            if not self.all_circuits_selected:
                self.query_one("#selected-circuits-list",SelectionList).select_all()
                self.query_one("#select-all-circuits-button", Button).label = "Deselect All"
                self.update_circuits_selected_view
            else:
                self.query_one("#selected-circuits-list",SelectionList).deselect_all()
                self.query_one("#select-all-circuits-button", Button).label = "Select All"
                self.update_circuits_selected_view()
            self.all_circuits_selected = not self.all_circuits_selected

        elif event.button.id == "fetch-stats-button":
            seasons_selected = self.query_one("#selected-seasons-list", SelectionList).selected
            drivers_selected = self.query_one("#selected-drivers-list", SelectionList).selected
            circuits_selected = self.query_one("#selected-circuits-list", SelectionList).selected
            session_type_selected = self.session_type

            if session_type_selected == "R":
                from ui.race_results_table import RaceResultsTableScreen
                self.app.push_screen(RaceResultsTableScreen(seasons_selected, circuits_selected, drivers_selected))
            
            if session_type_selected == "Q":
                from ui.qualifying_results_table import QualifyingResultsTableScreen
                self.app.push_screen(QualifyingResultsTableScreen(seasons_selected, circuits_selected, drivers_selected))

