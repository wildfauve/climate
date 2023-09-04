from __future__ import annotations
from typing import List
from functools import partial
from dataclasses import dataclass

from rdflib import Graph, URIRef, Literal, RDF, BNode

from clojos_common.util import fn, monad

from climate import rdf, repo


def upsert(g: repo.GraphRepo, temp_record) -> monad.EitherMonad:
    return rdf.subject_finder_creator(g,
                                      temp_record.subject,
                                      rdf.MinMaxTemperatureRecord,
                                      creater_fn=partial(_creator, temp_record),
                                      update_fn=partial(_updater, temp_record))


def _creator(temp_record, g: repo.GraphRepo, sub) -> monad.EitherMonad:
    g.add((sub, RDF.type, rdf.MinMaxTemperatureRecord))
    g.add((sub, rdf.recordedAtLocale, temp_record.locale.subject))
    g.add((sub, rdf.hasDailyMaximum, Literal(temp_record.maximum)))
    g.add((sub, rdf.hasDailyMinimum, Literal(temp_record.minimum)))
    g.add((sub, rdf.isRecordedOnDateTime, Literal(temp_record.date)))
    return monad.Right(g)


def _updater(temp_record, g: repo.GraphRepo, sub):
    breakpoint()
