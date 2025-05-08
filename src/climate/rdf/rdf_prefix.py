from rdflib import Namespace

__plz_cl_ns = "https://palazzo.io/ontology/Climate/"
__plz_cl_ind_ns = "https://palazzo.io/ontology/Climate/Ind/"

owl = Namespace("http://www.w3.org/2002/07/owl#")
skos = Namespace('http://www.w3.org/2004/02/skos/core#')

plz_cl = Namespace(__plz_cl_ns)

plz_cl_nar = Namespace(f"{__plz_cl_ns}NarrativeTerm/")

plz_cl_ind = Namespace(__plz_cl_ind_ns)

plz_cl_ind_loc = Namespace(f"{__plz_cl_ind_ns}Locale/")

plz_cl_ind_tem = Namespace(f"{__plz_cl_ind_ns}Temperature/")

plz_cl_ind_nar = Namespace(f"{__plz_cl_ind_ns}Narrative/")

foaf = Namespace("http://xmlns.com/foaf/0.1/")

dcterms = Namespace("http://purl.org/dc/terms/")
