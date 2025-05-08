from typing import Callable
from textwrap import dedent
from rdflib import Literal
from rdflib.plugins.sparql.processor import SPARQLResult

from clojos_common.util import logger



def sparql_prefixes():
    return dedent("""prefix plz-cl: <https://palazzo.io/ontology/Climate/>
    prefix plz-cl-ind-loc: <https://palazzo.io/ontology/Climate/Ind/Locale/> 
    prefix plz-cl-nar: <https://palazzo.io/ontology/Climate/NarrativeTerm/>
    prefix foaf: <http://xmlns.com/foaf/0.1/>
    prefix skos: <http://www.w3.org/2004/02/skos/core#>
    prefix foaf: <http://xmlns.com/foaf/0.1/>
    """)

def query(g, query_exp: str, prefixes_fn: Callable = sparql_prefixes) -> SPARQLResult:
    logger.info(f"{prefixes_fn()}\n{query_exp}")
    return g.query(f"{prefixes_fn()}\n{query_exp}")


