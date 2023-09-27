from __future__ import annotations
from typing import List
from functools import partial
from dataclasses import dataclass
from decimal import Decimal

import pendulum

from rdflib import Graph, URIRef, Literal, RDF, BNode

from clojos_common.util import fn, monad

from climate import rdf, repo

@dataclass
class TemperatureDTO:
    subject: URIRef
    maximum: Decimal
    minimum: Decimal
    recorded_at: pendulum.DateTime
    locale_subject: URIRef
    locale_name: str


def upsert(g: repo.GraphRepo, temp_record) -> monad.EitherMonad:
    return rdf.subject_finder_creator(g,
                                      temp_record.subject,
                                      rdf.MinMaxTemperatureRecord,
                                      creater_fn=partial(_creator, temp_record),
                                      update_fn=partial(_updater, temp_record))


def get_all(g: repo.GraphRepo):
    results = rdf.many(rdf.query(g, _by_locale_by_date_query()))
    return [_to_dto(record) for record in results]

def _creator(temp_record, g: repo.GraphRepo, sub) -> monad.EitherMonad:
    g.add((sub, RDF.type, rdf.MinMaxTemperatureRecord))
    g.add((sub, rdf.recordedAtLocale, temp_record.locale.subject))
    g.add((sub, rdf.hasDailyMaximum, Literal(temp_record.maximum)))
    g.add((sub, rdf.hasDailyMinimum, Literal(temp_record.minimum)))
    g.add((sub, rdf.isRecordedOnDateTime, Literal(temp_record.recorded_at)))
    g.add((sub, rdf.isRecordedForDate, Literal(temp_record.recorded_for)))
    return monad.Right(g)


def _updater(temp_record, g: repo.GraphRepo, sub):
    breakpoint()


def _to_dto(record):
    return TemperatureDTO(subject=record.rec,
                          minimum=record.min.toPython(),
                          maximum=record.max.toPython(),
                          recorded_at=pendulum.instance(record.datetime.toPython()),
                          locale_subject=record.locale,
                          locale_name=record.locale_name.toPython())

def _by_locale_by_date_query():
    return """
    SELECT * WHERE {{
  
    ?rec a plz-cl:MinMaxTemperatureRecord ;
  		 plz-cl:hasDailyMaximum ?max ;
    	 plz-cl:hasDailyMinimum ?min ;
     	 plz-cl:isRecordedOnDateTime ?datetime ;
      	 plz-cl:recordedAtLocale ?locale .
      
    ?locale foaf:name ?locale_name . 
  
    }}
    """
