from __future__ import annotations
from typing import Tuple, List, Optional, Callable, Set, Union
from functools import partial
from rdflib import Literal, URIRef, Graph, RDF
from rdflib.query import ResultRow
from rdflib.plugins.sparql.processor import SPARQLResult

import pendulum

from climate import repo, model
from clojos_common.util import fn, monad
from . import sparql


def single_result_or_none(result: SPARQLResult) -> Optional[ResultRow]:
    result_list = list(result)
    if len(result_list) != 1:
        return None
    return result_list[0]


def many(result: SPARQLResult) -> List[ResultRow]:
    return list(result)


def subject_finder_creator(g: repo.GraphRepo,
                           sub_uri: URIRef,
                           type_of: URIRef,
                           creater_fn: Callable,
                           update_fn: Callable):
    s, _, rdf_type = first_match(g, (sub_uri, RDF.type, type_of))
    match (s, rdf_type):
        case (None, None):
            return creater_fn(g, sub_uri)
        case _:
            return update_fn(g, sub_uri)


def _predicate_eq(term, triple: Tuple) -> bool:
    return triple[1] == term


def all_objects(triple_collection: List[Tuple]):
    return [o for _, _, o in triple_collection]


def obj(triple):
    return triple[2]


def subject(triple):
    return triple[0]


def triple_finder(term, t_map: List[Tuple], filter_fn=fn.find, cond=_predicate_eq, builder=obj):
    """
    Takes a triples map and applies a filter fn and a condition to return either
    a List[(s,p,o)] if builder=object_collection
    or (s,p,o) if builder=object_ind

    The Term can be a subject, predicate, object.  The default is a predicate (the _predicate_eq fn)
    """
    result = filter_fn(partial(cond, term), t_map)
    if result:
        return builder(result)
    return builder((None, None, None))


def subjects(g: Graph) -> Set[URIRef]:
    """
    Returns a set of unique subjects in a Graph
    """
    return set(g.subjects())


def object_for_property(g: Graph, predicate: URIRef, ) -> Union[URIRef, Literal]:
    """
    Extracts the object for a property
    """
    return first_match(g, (None, predicate, None), obj)


def first_match(g, pattern: Tuple, form=fn.identity) -> Union[Tuple, URIRef, Literal]:
    triple_list = list(all_matching(g, pattern))
    if not triple_list:
        return form((None, None, None))
    return form(triple_list[0])


def query_match(g, query, **kwargs):
    return sparql.query(g, query(**kwargs))


def all_matching(g, pattern: Tuple, form=fn.identity) -> List[Tuple]:
    return [form(t) for t in g.triples(pattern)]


@monad.monadic_try()
def safe_time_convert(time_literal: Literal):
    return time_literal.value.isoformat()


@monad.monadic_try()
def safe_datetime_to_pendulum(time_literal: Literal):
    return pendulum.instance(time_literal.value)


def literal_time(time_literal: Literal, converter: Callable = safe_time_convert) -> Optional[str]:
    if not time_literal:
        return None
    iso_time = converter(time_literal)
    return iso_time.value if iso_time.is_right else None


@monad.monadic_try()
def safe_date_convert(date: str):
    return pendulum.parse(date, tz=model.TZ)


@monad.monadic_try()
def safe_time_parser(time_str: str) -> monad.EitherMonad[pendulum.DateTime]:
    return pendulum.parse(time_str)


def literal_time_triple_parser(triple: Tuple):
    return literal_time(obj(triple), converter=safe_datetime_to_pendulum)

def price_label(amt: URIRef, ccy: URIRef) -> str:
    # TODO: Add the rdf-cty-ccy lib
    return "{c}{a}".format(c=ccy.split("/")[-1], a=str(amt.value))


def coerce_literal_value(literal: Literal) -> Optional:
    if not hasattr(literal, 'value'):
        return None
    return literal.value


def coerce_uri(uri: URIRef) -> Optional[str]:
    if not hasattr(uri, 'toPython'):
        return uri if isinstance(uri, str) else None
    return uri.toPython()


def month_day_from_datetime(datetime) -> Tuple[str, str]:
    if isinstance(datetime, pendulum.DateTime) or isinstance(datetime, pendulum.Date):
        return datetime.format("YYYY-MM"), datetime.to_date_string()
    time = safe_time_convert(datetime) >> safe_time_parser
    if time.is_left():
        return None, None
    return time.value.format("YYYY-MM"), time.value.to_date_string()


def gr(g: Graph):
    return list(g.triples((None, None, None)))


class Grapher:

    def __init__(self, name: str = None, init_g: Callable = None):
        self.source_g, self.query_g = None, None
        self.name = name if name else self.__class__.__name__
        self.init_g_fn = init_g if init_g else repo.initgraph

    def g(self, graph):
        self.source_g = graph
        return self

    def sub_grapher(self, name: str = None):
        return self.__class__(name).g(self.query_g) if self.query_g else self.__class__(name).g(self.source_g)

    def c(self, cq, **kwargs):
        """
        Expects a CONSTRUCT query, therefore a collection of triples
        """
        result = query_match(self.source_g, cq, **kwargs)
        self.query_g = self.init_g_fn()
        for row in result:
            self.query_g.add(row)

        return self

    def property_constructor(self, constructor_fn: Callable, **kwargs):
        return constructor_fn(self.query_g, **kwargs)
