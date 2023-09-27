import click
from decimal import Decimal

from climate.initialiser import environment, db

from climate import command

from . import helpers



@click.group()
def cli():
    pass


@click.command()
@click.option("--locale", "-l", type=str)
@click.option("--terms", "-t", multiple=True)
@click.option("--date", "-d", required=False, help="Reading Date", prompt=True, default=helpers.default_record_date())
def add(locale, terms, date):
    """
    Add a waether narrative using defined terms
    """
    # x = click.prompt("And...", type=int, default=2)
    command.add_narrative(locale, terms, date)
    pass


cli.add_command(add)
