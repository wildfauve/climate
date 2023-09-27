import click
from decimal import Decimal

from climate.initialiser import environment, db

from climate import command

from . import helpers



@click.group()
def cli():
    pass


@click.command()
@click.option("--date", "-d", required=False, help="Reading Date", prompt=True, default=helpers.default_record_date())
def add(date):
    """
    Add a weather narrative using defined terms
    """
    command.add_narrative(locale=helpers.get_locale_from_input(),
                          terms=helpers.get_narrative_terms_from_import(),
                          date=date)
    pass


@click.command()
def fix():
    """
    Any FIX entrypoint
    """
    command.narrative_fix()
    pass


cli.add_command(add)
cli.add_command(fix)
