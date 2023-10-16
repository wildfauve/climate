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
        minimum = helpers.prompt_for_temperature('Minimum')
        maximum = helpers.prompt_for_temperature('Maximum')
        command.add_temperature(locale, minimum, maximum, record_date)
    return flow


def _narrative(record_date):
    flow = None
    while True:
        locale = helpers.get_locale_from_input()
        if isinstance(locale, helpers.ExitTerminator):
            flow = locale
            break
        command.add_narrative(locale=locale,
                              terms=helpers.get_narrative_terms_from_import(),
                              date=record_date)
    return flow


def _main_menu():
    return {
        1: ('Add Temperatures', _temperatures),
        2: ('Add Narrative', _narrative),
        3: ('Exit', None)
    }
