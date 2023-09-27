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
@click.option("--date", "-d", required=False, help="Reading Date", prompt=True, default=helpers.default_record_date())
def add(locale, minimum, maximum, date):
    """
    Add a new daily min/max temperature reading.
    """
    command.add_temperature(locale, minimum, maximum, date)
    pass



@click.command()
def fix():
    """
    Any FIX entrypoint
    """
    command.temperature_fix()
    pass



@click.command()
@click.option("--channel", "-c", default='terminal', type=click.Choice(helpers.channels()))
def plot(channel):
    """
    Plot Stub
    """
    command.plot_temperatures(channel=channel)
    pass



cli.add_command(add)
cli.add_command(plot)
cli.add_command(fix)
