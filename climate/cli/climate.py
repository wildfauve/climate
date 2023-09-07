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
@click.option("--minimum", "-n", type=Decimal)
@click.option("--maximum", "-x", type=Decimal)
@click.option("--date", "-d", required=False, help="Reading Date")
def add_temperature(locale, minimum, maximum, date):
    """
    Add a new daily min/max temperature reading.
    """
    command.add_temperature(locale, minimum, maximum, date)
    pass


@click.command()
@click.option("--locale", "-l", type=str)
@click.option("--terms", "-t", multiple=True, type=click.Choice(helpers.narrative_term_names()))
@click.option("--date", "-d", required=False, help="Reading Date")
def add_narrative(locale, terms, date):
    """
    Add a waether narrative using defined terms
    """
    command.add_narrative(locale, terms, date)
    pass


@click.command()
@click.option("--channel", "-c", type=click.Choice(helpers.channels()))
def plot(channel):
    """
    Plot Stub
    """
    command.plot_temperatures(channel=channel)
    pass



cli.add_command(add_temperature)
cli.add_command(add_narrative)
cli.add_command(plot)
