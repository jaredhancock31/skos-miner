"""
Author: Jared Hancock
Date: Feb 2016
Email: jaredhancock31@gmail.com
"""
import rdflib
import json
import requests
from requests.auth import HTTPBasicAuth
from skos import RDFLoader
from collections import defaultdict

# TODO decode unicode strings?
# For quick testing:
# crown_of_queen = "http://dbpedia.org/resource/Crown_of_Queen_Elizabeth"         # should have 4 relateds
# process495 = "http://infoneer.poolparty.biz/Processes/495"                    # should have zero relateds


def parse_json(relateds, rel_table):
    """
    parse the json dictionary and increment frequency value for concepts found in the relateds parameter

    :param relateds: list of dicts containing related concepts in the API response
    :param rel_table: collection (defaultdict) of concepts (keys) and the number of times they have been a related
                      concept (values)
    :return:
    """
    for concept in relateds:
        uri = concept['uri']
        rel_table[uri] += 1


def query_related(concept):
    """
    send http request to PP API to get related concepts of a given concept.

    :param concept: URI of concept to query for
    :return: JSON object containing related concepts, or None for no relateds
    """

    related_url = "http://infoneer.poolparty.biz/PoolParty/api/thesaurus/" \
                  "1DBC67E1-7669-0001-8A4A-F4B06F409540/relateds?concept="
    qurl = related_url + concept
    result = requests.get(qurl, auth=HTTPBasicAuth('ppuser', 'infoneer'))

    if result.text == "[]" or result.text == "[ ]":
        return None
    else:
        return json.loads(result.text)


def main():
    """
    Builds a list of concepts ranked by relevance (relation-frequency)
    """
    filename = "pp_project_manuterms.rdf"
    # filename = "testfile.rdf"

    g = rdflib.Graph()
    g = g.parse(location=filename, format="application/rdf+xml")
    loader = RDFLoader(g)

    concepts = loader.getConcepts()
    rel_table = defaultdict(int)

    for concept in concepts:
        relateds = query_related(concept)
        if relateds is not None:
            parse_json(relateds, rel_table)
        else:
            # TODO collect concepts without any relations?
            pass

    # print [i for i in sorted(rel_table.iteritems(), reverse=True, key=lambda (k,v): v)]
    for i in sorted(rel_table.iteritems(), reverse=True, key=lambda (k,v): v):
        print i

if __name__ == "__main__":
    main()
