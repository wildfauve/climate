from __future__ import annotations
from typing import List, Tuple
from functools import partial
from dataclasses import dataclass

from rdflib import Graph, URIRef, Literal, RDF, BNode

from clojos_common.util import fn, monad

from climate import rdf, repo


@dataclass
class LocaleDTO:
    name: str
    subject: URIRef


def upsert(g: repo.GraphRepo, locale) -> monad.EitherMonad:
    return rdf.subject_finder_creator(g,
                                      locale.subject,
                                      rdf.Locale,
                                      creater_fn=partial(_creator, locale),
                                      update_fn=partial(_updater, locale))


def find_by_name(g: repo.GraphRepo, name):
    return _to_locale(rdf.first_match(g, (None, rdf.name, Literal(name))))


def find_by_sub(g: repo.GraphRepo, sub):
    return _to_locale(rdf.first_match(g, (sub, rdf.name, None)))


def get_all(g: repo.GraphRepo):
    return [find_by_sub(g, sub) for sub in rdf.all_matching(g, (None, RDF.type, rdf.Locale), form=rdf.subject)]


def _creator(locale, g: repo.GraphRepo, sub) -> monad.EitherMonad:
    g.add((sub, RDF.type, rdf.Locale))
    g.add((sub, rdf.name, Literal(locale.name)))
    return monad.Right(g)


def _updater(temp_record, g: repo.GraphRepo, sub):
    breakpoint()

def _to_locale(locale: Tuple):
    sub, _, name = locale
    if not sub:
        breakpoint()
    return LocaleDTO(name=name, subject=sub)