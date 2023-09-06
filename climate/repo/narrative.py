from __future__ import annotations
from typing import List
from functools import partial
from dataclasses import dataclass

from rdflib import Graph, URIRef, Literal, RDF, BNode

from clojos_common.util import fn, monad

from climate import rdf, repo


def upsert(g: repo.GraphRepo, narrative_record) -> monad.EitherMonad:
    return rdf.subject_finder_creator(g,
                                      narrative_record.subject,
                                      rdf.MinMaxTemperatureRecord,
                                      creater_fn=partial(_creator, narrative_record),
                                      update_fn=partial(_updater, narrative_record))


def _creator(narrative_record, g: repo.GraphRepo, sub) -> monad.EitherMonad:
    g.add((sub, RDF.type, rdf.WeatherNarrative))
    g.add((sub, rdf.recordedAtLocale, narrative_record.locale.subject))
    g.add((sub, rdf.isRecordedOnDateTime, Literal(narrative_record.recorded_at)))
    for t in narrative_record.terms:
        g.add((sub, rdf.hasWeatherNarrativeTerm, t.value))
    return monad.Right(g)


def _updater(temp_record, g: repo.GraphRepo, sub):
    breakpoint()
