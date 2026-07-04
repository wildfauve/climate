from decimal import Decimal

import click

from climate import command
from climate.initialiser import db, environment

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
