import click
from decimal import Decimal

from climate.initialiser import environment, db

from climate import command

# from . import helpers



@click.group()
def cli():
    pass



@click.command()
@click.option("--name", "-n", type=str)
def create(name):
    """
    Starts the tournament,  applies the results, applies the fantasy selection and prints the leaderboard
    """
    command.add_locale(name)
    pass


cli.add_command(create)
