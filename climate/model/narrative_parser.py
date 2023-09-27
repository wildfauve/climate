from typing import List, Union, Tuple
import re
from dataclasses import dataclass
from enum import Enum

from climate import rdf

noun_concept = re.compile(r"(^\w*)\[")
temporal_adjectives = re.compile(r"\[([\w:,;]*)\]")

RAIN = rdf.plz_cl_nar.Rain
WIND = rdf.plz_cl_nar.WIND
TEMPERATURE = rdf.plz_cl_nar.Temperature
SKY = rdf.plz_cl_nar.Sky
TEMPORAL_TERM = rdf.plz_cl_nar.TemporalTerm


class RainTerms(Enum):
    DRY = RAIN + "/Dry"
    DROPS = RAIN + "Drops"
    DRIZZLE = RAIN + "/Drizzle"
    SHOWERS = RAIN + "/Showers"
    HEAVY = RAIN + "/Heavy"


class WindTerms(Enum):
    STILL = WIND + "/Still"
    LIGHT = WIND + "/Light"
    MODERATE = WIND + "/Moderate"
    STRONG = WIND + "/Strong"
    GALE_FORCE = WIND + "/GaleForce"


class TemperatureTerms(Enum):
    FROST = TEMPERATURE + "/Frost"
    COLD = TEMPERATURE + "/Cold"
    COOL = TEMPERATURE + "/Cool"
    MILD = TEMPERATURE + "/Mild"
    WARM = TEMPERATURE + "/Warm"
    HOT = TEMPERATURE + "/Hot"


class SkyTerms(Enum):
    SUNNY = SKY + "/Sunny"
    OVERCAST = SKY + "/Overcast"
    CLOUDY = SKY + "/Cloudy"


class NarrativeNoun(Enum):
    RAIN = (RAIN, RainTerms)
    WIND = (WIND, WindTerms)
    SKY = (SKY, SkyTerms)
    TEMPERATURE = (TEMPERATURE, TemperatureTerms)


class TemporalTerm(Enum):
    DAY = TEMPORAL_TERM + "/Day"
    NIGHT = TEMPORAL_TERM + "/Night"
    EARLY_MORNING = TEMPORAL_TERM + "/EarlyMorning"
    LATE_MORNING = TEMPORAL_TERM + "/LateMorning"
    MORNING = TEMPORAL_TERM + "/Morning"
    EARLY_AFTERNOON = TEMPORAL_TERM + "/EarlyAfternoon"
    LATE_AFTERNOON = TEMPORAL_TERM + "/LateAfternoon"
    AFTERNOON = TEMPORAL_TERM + "/Afternoon"
    EARLY_EVENING = TEMPORAL_TERM + "/EarlyEvening"
    LATE_EVENING = TEMPORAL_TERM + "/LateEvening"
    EVENING = TEMPORAL_TERM + "/Evening"
    OVER_NIGHT = TEMPORAL_TERM + "/OverNight"


@dataclass
class TemporalAdjectiveCollection:
    adjective: Union[RainTerms]
    temporal_statements: List[TemporalTerm]


@dataclass
class NarrativeStatement:
    noun: NarrativeNoun
    temporal_adjectives: List[TemporalAdjectiveCollection]


def narrative_nouns():
    return NarrativeNoun.__members__.keys()


def parse(component: str) -> NarrativeStatement:
    minified_component = _remove_fill(component)
    noun, adj_type = _noun(minified_component).value
    return NarrativeStatement(noun=noun,
                              temporal_adjectives=_temporal_adjectives(minified_component, adj_type))


def _remove_fill(component: str) -> str:
    return component.replace(" ", "")


def _noun(component: str) -> Tuple:
    search = noun_concept.search(component)
    if not search:
        breakpoint()
    noun, *_ = search.groups()
    return _term_or_none(noun.upper(), NarrativeNoun)


def _temporal_adjectives(component: str, adj_type: Union[RainTerms]):
    search = temporal_adjectives.search(component)
    if not search:
        breakpoint()
    all_adjs, *_ = search.groups()
    return [_individual_adjective(group, adj_type) for group in all_adjs.split(";")]


def _individual_adjective(group: str, adj_type):
    adj_name, temporality = group.split(":")
    return TemporalAdjectiveCollection(adjective=_term_or_none(adj_name.upper(), adj_type),
                                       temporal_statements=[_term_or_none(term.upper(), TemporalTerm) for term in
                                                            temporality.split(",")])


def _term_or_none(term, term_type: Enum):
    if term not in term_type.__members__:
        breakpoint()
        return None
    return term_type[term]
