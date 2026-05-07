from rich.panel import Panel
from rich.align import Align

def generateBanner(title):
    return Panel.fit(Align.center(title), style="bold red", border_style="bright_black", title="F1Stat", title_align="center")
