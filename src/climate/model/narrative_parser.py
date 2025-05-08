from typing import List, Union, Tuple, Optional, Generic, TypeVar
import re
from dataclasses import dataclass
from enum import Enum

from clojos_common.util import monad, fn

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
    STORMY = SKY + "/Stormy"


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


class TemporalShortCuts(Enum):
    D = TemporalTerm.DAY
    N = TemporalTerm.NIGHT
    EM = TemporalTerm.EARLY_MORNING
    LM = TemporalTerm.LATE_MORNING
    M = TemporalTerm.MORNING
    EA = TemporalTerm.EARLY_AFTERNOON
    LA = TemporalTerm.LATE_AFTERNOON
    A = TemporalTerm.AFTERNOON
    EE = TemporalTerm.EARLY_EVENING
    LE = TemporalTerm.LATE_EVENING
    E = TemporalTerm.EVENING


@dataclass
class TemporalAdjectiveCollection:
    adjective: Union[RainTerms]
    temporal_statements: list[TemporalTerm]


@dataclass
class NarrativeStatement:
    noun: NarrativeNoun
    temporal_adjectives: List[TemporalAdjectiveCollection]


def narrative_nouns():
    return NarrativeNoun.__members__.keys()


def parse(component: str) -> monad.Either[NarrativeStatement, str]:
    minified_component = _remove_fill(component)
    noun, adj_type = _noun(minified_component).value
    adjs = _temporal_adjectives(minified_component, adj_type)
    if noun is None:
        return monad.Left(f"Noun not found in term {component}")
    if not all(adjs):
        return monad.Left(f"Adjectives dont parse for {component}")
    if not all([t for adj in adjs for t in adj.temporal_statements]):
        return monad.Left(f"Adjectives dont parse for {component}")
    return monad.Right(NarrativeStatement(noun=noun,
                                          temporal_adjectives=_temporal_adjectives(minified_component, adj_type)))


def _remove_fill(component: str) -> str:
    return component.replace(" ", "")


def _noun(component: str) -> Tuple:
    search = noun_concept.search(component)
    if not search:
        return (None, None)
    noun, *_ = search.groups()
    return _term_or_none(noun.upper(), NarrativeNoun)


def _temporal_adjectives(component: str, adj_type: Union[RainTerms]):
    search = temporal_adjectives.search(component)
    if not search:
        breakpoint()
    all_adjs, *_ = search.groups()
    return [_individual_adjective(group, adj_type) for group in all_adjs.split(";")]

def _individual_adjective(group: str, adj_type) -> TemporalAdjectiveCollection | None:
# def _individual_adjective(group: str, adj_type) -> Optional[TemporalAdjectiveCollection]:
    if group.count(":") != 1:
        return None
    adj_name, temporality = group.split(":")
    term = _term_or_none(adj_name.upper(), adj_type)
    if term is None:
        return None
    return TemporalAdjectiveCollection(
        adjective=_term_or_none(adj_name.upper(), adj_type),
        temporal_statements=[_term_or_none(term.upper(), TemporalTerm, TemporalShortCuts) for term in temporality.split(",")])


def _term_or_none(term, term_type: Enum, short_cuts: Optional[Enum] = None):
    if term not in term_type.__members__:
        return _nothing_or_shortcut(term, short_cuts)
    return term_type[term]


def _nothing_or_shortcut(term, short_cuts: Optional[Enum]):
    if not short_cuts or term not in short_cuts.__members__:
        return None
    return short_cuts[term].value
