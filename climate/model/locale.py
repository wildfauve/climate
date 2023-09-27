from __future__ import annotations
from typing import List, Union
from dataclasses import dataclass

import pendulum
from rdflib import URIRef, Graph
from clojos_common.util import monad, tokeniser

from climate import model, repo, rdf


@dataclass
class Locale:
    name: str
    subject: URIRef

    def symbolised_name(self):
        return self.subject.split("/")[-1]


def create(g: repo.GraphRepo, name):
    locale = _to_locale(name)
    if result := repo.locale.upsert(g, locale):
        return monad.Right(locale)
    breakpoint()


def _to_locale(name):
    return Locale(name=name,
                  subject=_to_subject(name))


def locale_from_name(g: repo.GraphRepo, name) -> monad.EitherMonad:
    result_dto = repo.locale.find_by_name(g, name)
    return to_locale(name=result_dto.name, subject=result_dto.subject)


def locale_from_sub(g: repo.GraphRepo, sub) -> monad.EitherMonad:
    result_dto = repo.locale.find_by_sub(g, sub)
    return to_locale(name=result_dto.name.value, subject=result_dto.subject)


def to_locale(name, subject):
    return monad.Right(Locale(name=name, subject=subject))


def _to_subject(name) -> URIRef:
    token_name = tokeniser.titleiser_tokeniser(name, tokeniser.sp_splitter,
                                               tokeniser.special_char_set)
    return rdf.plz_cl_ind_loc[token_name]
