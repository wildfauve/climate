from climate.initialiser import environment, db

from climate import command, presenter

from . import helpers


def run():
    record_date = helpers.prompt_for_date()
    while True:
        selection = helpers.show_menu_and_prompt(_main_menu())
        if selection is None:
            break
        flow_step = selection(record_date)
        if isinstance(flow_step, helpers.ExitTerminator) and flow_step.is_exit():
            break


def _temperatures(record_date):
    flow = None
    while True:
        locale = helpers.get_locale_from_input()
        if isinstance(locale, helpers.ExitTerminator):
            flow = locale
            break
        minimum = helpers.prompt_for_temperature(f'{locale.name.toPython()}: Minimum')
        maximum = helpers.prompt_for_temperature(f'{locale.name.toPython()}: Maximum')
        command.add_temperature(locale, minimum, maximum, record_date)
    return flow


def _narrative(record_date):
    flow = None
    while True:
        locale_or_terminator = helpers.get_locale_from_input()
        if isinstance(locale_or_terminator, helpers.ExitTerminator):
            flow = locale_or_terminator
            break
        command.add_narrative(locale=locale_or_terminator,
                              terms=helpers.get_narrative_terms_from_import(),
                              date=record_date)
    return flow


def _plot(_record_date):
    channel = helpers.get_channel_from_input()
    command.plot_temperatures(channel=channel)
    return None

def _main_menu():
    return {
        1: ('Add Temperatures', _temperatures),
        2: ('Add Narrative', _narrative),
        4: ('Plot', _plot),
        3: ('Exit', None)
    }
