import click
from decimal import Decimal

from climate.initialiser import environment, db

from climate import command

# from . import helpers



@click.group()
def cli():
    pass



@click.command()
@click.option("--locale", "-l", type=str)
@click.option("--minimum", "-n", type=Decimal)
@click.option("--maximum", "-x", type=Decimal)
@click.option("--date", "-d", required=False, help="Reading Date")
def add_temperature(locale, minimum, maximum, date):
    """
    Starts the tournament,  applies the results, applies the fantasy selection and prints the leaderboard
    """
    command.add_temperature(locale, minimum, maximum, date)
    pass


cli.add_command(add_temperature)
