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
import sys

# TODO decode unicode strings?
# For quick testing:
# crown_of_queen = "http://dbpedia.org/resource/Crown_of_Queen_Elizabeth"         # should have 4 relateds
# process495 = "http://infoneer.poolparty.biz/Processes/495"                    # should have zero relateds


def parse_json(concepts, rel_table):
    """
    parse the json dictionary and increment frequency value for concepts found in the relateds parameter

    :param relateds: list of dicts containing related concepts in the API response
    :param rel_table: collection (defaultdict) of concepts (keys) and the number of times they have been a related
                      concept (values)
    :return:
    """
    sys.stdout.write('.')   # for the loading message
    for concept in concepts:
        prefLabel = concept['prefLabel']

        # print(concept)

        if 'relateds' in concept:
            relateds = concept['relateds']
            for rel in relateds:
                # rel_table[rel] += 1
                rel_table[rel.encode('utf-8')] += 1


def query_related(concepts, index=0, max_param=100):
    """
    send http request to PP API to get related concepts of a given concept.

    :param max_param:
    :param index:
    :param concepts:
    :return: JSON object containing related concepts, or None for no relateds
    """

    url = "http://infoneer.poolparty.biz/PoolParty/api/thesaurus/" \
                  "1DBC67E1-7669-0001-8A4A-F4B06F409540/concepts?properties=skos:related"
    i = 0
    while i < max_param and index < len(concepts):
            c = concepts[index]
            url += "&concepts=" + c
            index += 1
            i += 1

    result = requests.get(url, auth=HTTPBasicAuth('ppuser', 'infoneer'))

    if result.text == "[]" or result.text == "[ ]":
        return None, 0
    else:
        # print "index" + str(index)
        return json.loads(result.text), index


def main():
    """
    Builds a list of concepts ranked by relevance (relation-frequency)
    """
    filename = "pp_project_manuterms.rdf"   # currently 2188 concepts
    # filename = "testfile.rdf"

    g = rdflib.Graph()
    g = g.parse(location=filename, format="application/rdf+xml")
    loader = RDFLoader(g)
    concepts = loader.getConcepts()  # type is skos.Concepts, despite just being a list

    # make it a list of uri's
    conceptList = []
    for c in concepts:
        conceptList.append(c)
    rel_table = defaultdict(int)

    max_concepts_per_req = 100
    num_concepts_requested = 0

    sys.stdout.write("collecting related metrics")  # make a kind of loading message
    while num_concepts_requested < len(conceptList):
        response, num_concepts_requested = query_related(conceptList, num_concepts_requested, 100)

        if response is not None:
            parse_json(response, rel_table)
        # print "index : " + num_concepts_requested

    print " done! "
    for i in sorted(rel_table.iteritems(), reverse=True, key=lambda (k,v): v):
        print i

if __name__ == "__main__":
    main()
