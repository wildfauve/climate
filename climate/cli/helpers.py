from typing import List
from functools import reduce, partial
from pathlib import Path
import json

import click
from clojos_common.util import fn

from climate import model, adapter, repo, presenter

console_save_file = Path(__file__).parent.parent.parent / "_temp" / "console.json"


def channels():
    return [c.name.lower() for c in adapter.Channel]


def default_record_date():
    return model.helpers.default_day(format_as_date_str=True)


def all_locales_indexed():
    return [(idx, locale.value) for idx, locale in enumerate(model.locale.get_all(repo.graph('climate_graph')))]


def get_locale_from_input():
    cons = console()
    all_locales = all_locales_indexed()
    for idx, locale in all_locales:
        cons.print(f"[bold red]{idx}. [magenta]{locale.name}")
    _, locale = all_locales[_prompt_for_locale_idx(all_locales)]
    return locale


def _prompt_for_locale_idx(all_locales):
    return int(click.prompt("Select Locale", type=click.Choice([str(idx) for idx, _ in all_locales])))


def get_narrative_terms_from_import():
    console_log, terms = reduce(_term_for_noun, model.narrative_parser.narrative_nouns(), (_console_input_file(), []))
    _write_dict(console_save_file, console_log)
    return terms


def _term_for_noun(acc: List, noun):
    console_log, terms = acc
    term = click.prompt(f"Narrative for {noun}", type=str,
                        default=_last_input(console_log, ['narrative', 'noun', noun.lower()]))

    full_term = _noun_wrap(noun, term)
    result = model.narrative_parser.parse(full_term)
    if result.is_left():
        console().print(f"Problem with the narrative; [bold magenta]{result.error()}")
        return _term_for_noun(acc, noun)
    _add_noun_to_log(console_log, noun, term)
    return (console_log, terms + [_noun_wrap(noun, term)])


def _add_noun_to_log(console_log, noun, term):
    current_logged_nouns = fn.deep_get(console_log, ['narrative', 'noun'])
    if not current_logged_nouns:
        console_log.update({'narrative': {'noun': {noun.lower(): term}}})
    else:
        console_log['narrative']['noun'].update({noun.lower(): term})
    pass


def _noun_wrap(noun, term):
    return f"{noun.lower()}[{term}]"


def console():
    return presenter.terminal_console()


def _last_input(console_log, path):
    return fn.deep_get(console_log, path)


def _console_input_file():
    with console_save_file.open(encoding="UTF-8") as source:
        objects = json.load(source)
    return objects


def _write_dict(file, struct):
    with file.open("w", encoding="UTF-8") as target:
        json.dump(struct, target, indent=4, sort_keys=True)
