from typing import Optional
import mysql.connector
import mysql
import typer


from rich.table import Table
from rich.console import Console
import json
table = Table(show_header=True, header_style="bold blue", show_lines=True)
import Database

app = typer.Typer()
f = open('data.json')
data = json.load(f)


user ="62f3575ab51f8a773cde8ed1"
a = Database.connection

@app.command()
def start(id: Optional[str] = None):
        typer.echo(f"Hello to AIops project")

        if(user == id):
            typer.echo(f"Hello to AIops project {id}")
        else:
            typer.echo(f"You have to enter your id so I can recognize you")

console = Console()

@app.command(short_help="shows all data")
def show():
    if len(data) == 0:
        console.print("[bold red]No data to show[/bold red]")
    else:

        table.add_column("#", style="dim", width=3, justify="center")
        table.add_column("id", min_width=20, justify="center")
        table.add_column("SPH", min_width=12, justify="center")
        table.add_column("UOM", min_width=12, justify="center")
        table.add_column("UOC", min_width=12, justify="center")
        table.add_column("IsPdfSend", min_width=12, justify="center")
        table.add_column("CreatedAt", min_width=12, justify="center")

        table.add_row(f'[cyan]{1}[/cyan]',f'[cyan]{data["id"]}[/cyan]', f'[green]{data["SPH"]}[/green]',f'[green]{data["UOM"]}[/green]',f'[green]{data["UOC"]}[/green]',f'[green]{data["IsPdfSend"]}[/green]',f'[green]{data["CreatedAt"]}[/green]')
        console.print(table)

@app.command(short_help="shows all data")
def AllPredictionRecords():
    connection = mysql.connector.connect(host='localhost',
                                         database='aiopsdb',
                                         user='root',
                                         password='root', auth_plugin='mysql_native_password')

    sql_select_Query = "SELECT * FROM aiopsdb.usageserver"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    table.add_column("#", style="dim", width=3, justify="center")
    table.add_column("id", min_width=20, justify="center")
    table.add_column("SPH", min_width=12, justify="center")
    table.add_column("UOM", min_width=12, justify="center")
    table.add_column("UOC", min_width=12, justify="center")
    table.add_column("IsPdfSend", min_width=12, justify="center")
    table.add_column("CreatedAt", min_width=12, justify="center")
    for idx, row in enumerate(records, start=1):
        table.add_row(str(idx), f'[cyan]{row[0]}[/cyan]', f'[green]{row[1]}[/green]',f'[cyan]{row[2]}[/cyan]', f'[green]{row[3]}[/green]',f'[green]{row[4]}[/green]',f'[green]{row[5]}[/green]')
    console.print(table)
@app.command()
def prediction(SPH:int = None,IsPdfSend:int = None):
    import main
    main.main_(SPH,IsPdfSend)


@app.command()
def bye(name: Optional[str] = None):
    if name:
        typer.echo(f"Bye {name}")
    else:
        typer.echo("Goodbye!")

if __name__ == "__main__":
    app()