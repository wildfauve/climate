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


def get_all_narratives(g: repo.GraphRepo):
    return rdf.all_matching(g, (None, RDF.type, rdf.WeatherNarrative))


def _creator(narrative_record, g: repo.GraphRepo, sub) -> monad.EitherMonad:
    g.add((sub, RDF.type, rdf.WeatherNarrative))
    g.add((sub, rdf.recordedAtLocale, narrative_record.locale.subject))
    g.add((sub, rdf.isRecordedAtDateTime, Literal(narrative_record.recorded_at)))
    for statement in narrative_record.narrative_statements:
        _add_narrative(g, sub, statement)
    return monad.Right(g)


def _add_narrative(g, sub, statement):
    bn = BNode()
    g.add((sub, rdf.hasWeatherNarrativeStatement, bn))
    g.add((bn, RDF.type, rdf.WeatherNarrativeStatement))
    g.add((bn, rdf.isStatementOnWeatherPhenomenon, statement.noun))
    for temp_adj in statement.temporal_adjectives:
        _add_temporal_adjective(g, bn, temp_adj)
    return g


def _add_temporal_adjective(g, bn, temp_adj):
    temp_adj_bn = BNode()
    g.add((bn, rdf.hasTemporalAdjective, temp_adj_bn))
    g.add((temp_adj_bn, rdf.hasAdjective, temp_adj.adjective.value))
    for temporal_statement in temp_adj.temporal_statements:
        if not temporal_statement:
            breakpoint()
        g.add((temp_adj_bn, rdf.hasTemporalExpression, temporal_statement.value))

def _updater(temp_record, g: repo.GraphRepo, sub):
    breakpoint()
