
import rdflib
import json
import requests
from requests.auth import HTTPBasicAuth
from skos import RDFLoader
from collections import defaultdict

# TODO decode unicode strings

def query_relateds(concepts):
    """
    send http request to PP API to get related queries of a given concept
    :param concepts: list of concepts to retrieve relateds for
    :return:
    """
    related_url = "http://infoneer.poolparty.biz/PoolParty/api/thesaurus/" \
                  "1DBC67E1-7669-0001-8A4A-F4B06F409540/relateds?concept="
    for concept in concepts:
        qurl = related_url+concept
        result = requests.get(qurl, auth=HTTPBasicAuth('ppuser', 'infoneer'))


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


def query_rel_test():
    related_url = "http://infoneer.poolparty.biz/PoolParty/api/thesaurus/" \
                  "1DBC67E1-7669-0001-8A4A-F4B06F409540/relateds?concept="

    crown_of_queen = "http://dbpedia.org/resource/Crown_of_Queen_Elizabeth"
    qurl = related_url + crown_of_queen
    result = requests.get(qurl, auth=HTTPBasicAuth('ppuser', 'infoneer'))

    # process495 = "http://infoneer.poolparty.biz/Processes/495"
    # qurl = related_url + process495
    # result = requests.get(qurl, auth=HTTPBasicAuth('ppuser', 'infoneer'))
    # if result.text == "[]" or result.text == "[ ]":
    #     print "empty"

    r_json = json.loads(result.text)


    print r_json[0]['uri']
    print type(r_json[0]['uri'])


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
    query_rel_test()
    # query_relateds(concepts)


if __name__ == "__main__":
    main()
