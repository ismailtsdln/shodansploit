import json
import os

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich import print as rprint
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False

BANNER = """
      _               _                       _       _ _
  ___| |__   ___   __| | __ _ _ __  ___ _ __ | | ___ (_) |_
 / __| '_ \ / _ \ / _` |/ _` | '_ \/ __| '_ \| |/ _ \| | __|
 \__ \ | | | (_) | (_| | (_| | | | \__ \ |_) | | (_) | | |_
 |___/_| |_|\___/ \__,_|\__,_|_| |_|___/ .__/|_|\___/|_|\__|
                                       |_|            v1.2.0
	Author : Ismail Tasdelen
	GitHub : github.com/ismailtasdelen
      Linkedin : linkedin.com/in/ismailtasdelen
       Twitter : twitter.com/ismailtsdln
"""

MENU = """
[1] GET > /shodan/host/{ip}
[2] GET > /shodan/host/count
[3] GET > /shodan/host/search
[4] GET > /shodan/host/search/tokens
[5] GET > /shodan/ports

[6] GET > /shodan/exploit/author
[7] GET > /shodan/exploit/cve
[8] GET > /shodan/exploit/msb
[9] GET > /shodan/exploit/bugtraq-id
[10] GET > /shodan/exploit/osvdb
[11] GET > /shodan/exploit/title
[12] GET > /shodan/exploit/description
[13] GET > /shodan/exploit/date
[14] GET > /shodan/exploit/code
[15] GET > /shodan/exploit/platform
[16] GET > /shodan/exploit/port

[17] GET > /dns/resolve
[18] GET > /dns/reverse
[19] GET > /labs/honeyscore/{ip}

[20] GET > /account/profile
[21] GET > /tools/myip
[22] GET > /tools/httpheaders
[23] GET > /api-info

[24] Exit
[25] Shodan Dorks Library
[26] View Search History
"""

class UI:
    @staticmethod
    def show_banner():
        if HAS_RICH:
            console.print(Panel(BANNER, style="bold red"))
        else:
            print(BANNER)

    @staticmethod
    def show_menu():
        if HAS_RICH:
            console.print(Panel(MENU, title="Menu", style="bold green"))
        else:
            print(MENU)

    @staticmethod
    def get_input(prompt_text):
        if HAS_RICH:
            return console.input(f"[bold cyan]{prompt_text}[/bold cyan] ")
        else:
            return input(prompt_text)

    @staticmethod
    def print_result(data):
        if HAS_RICH:
            json_str = json.dumps(data, indent=2, sort_keys=True)
            syntax = Syntax(json_str, "json", theme="monokai", line_numbers=True)
            console.print(syntax)
        else:
            print(json.dumps(data, indent=2, sort_keys=True))

    @staticmethod
    def print_error(message):
        if HAS_RICH:
            console.print(f"[bold red][✘] Error: {message}[/bold red]")
        else:
            print(f"[✘] Error: {message}")

    @staticmethod
    def print_success(message):
        if HAS_RICH:
            console.print(f"[bold green][✔] {message}[/bold green]")
        else:
            print(f"[✔] {message}")
