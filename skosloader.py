
import rdflib
import json
import requests
from requests.auth import HTTPBasicAuth
from skos import RDFLoader
from collections import defaultdict

# TODO decode unicode strings?


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
        print uri
        rel_table[uri] += 1


def query_related(concept):
    """
    send http request to PP API to get related concepts of a given concept.

    :param concept: URI of concept to query for
    :return: JSON object containing related concepts, or None
    """

    related_url = "http://infoneer.poolparty.biz/PoolParty/api/thesaurus/" \
                  "1DBC67E1-7669-0001-8A4A-F4B06F409540/relateds?concept="
    qurl = related_url + concept
    result = requests.get(qurl, auth=HTTPBasicAuth('ppuser', 'infoneer'))

    if result.text == "[]" or result.text == "[ ]":
        return None
    else:
        return json.loads(result.text)


def app_test(rel_table):

    print "rel_table before: "
    print [i for i in rel_table.items()]
    related_url = "http://infoneer.poolparty.biz/PoolParty/api/thesaurus/" \
                  "1DBC67E1-7669-0001-8A4A-F4B06F409540/relateds?concept="

    crown_of_queen = "http://dbpedia.org/resource/Crown_of_Queen_Elizabeth"

    result = query_related(crown_of_queen)
    if result == None:
        return None
    else:
        parse_json(result, rel_table)

    print "rel_table after:"
    print [i for i in rel_table.items()]

    # qurl = related_url + crown_of_queen
    # result = requests.get(qurl, auth=HTTPBasicAuth('ppuser', 'infoneer'))

    # process495 = "http://infoneer.poolparty.biz/Processes/495"
    # qurl = related_url + process495
    # result = requests.get(qurl, auth=HTTPBasicAuth('ppuser', 'infoneer'))
    # if result.text == "[]" or result.text == "[ ]":
    #     print "empty"

    # r_json = json.loads(result.text)
    #
    # print type(r_json)
    # print r_json[0]['uri']
    # print type(r_json[0]['uri'])


def main():
    filename = "pp_project_manuterms.rdf"
    infile = open(filename)

    # xml_data = infile.read()
    # g = rdflib.Graph()
    # result = g.parse(data=xml_data, format="application/rdf+xml")

    g = rdflib.Graph()
    g = g.parse(location=filename, format="application/rdf+xml")
    loader = RDFLoader(g)

    concepts = loader.getConcepts()
    rel_table = defaultdict(int)
    app_test(rel_table)
    app_test(rel_table)
    # query_relateds(concepts)


if __name__ == "__main__":
    main()
