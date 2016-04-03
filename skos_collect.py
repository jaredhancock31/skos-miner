#!/usr/bin/env python
import rdflib
import json
import requests
import re
from requests.auth import HTTPBasicAuth
from skos import RDFLoader
from collections import OrderedDict
import sys
from django.utils.http import urlunquote_plus
from constants import *

MAX_ITEM_PER_REQUEST = 100
THESAURUS_URL = "http://infoneer.poolparty.biz/PoolParty/api/thesaurus/" \
                  "1DBC67E1-7669-0001-8A4A-F4B06F409540/"


# TODO move away from the skos api for gathering URIs
def get_uris(filename="res/pp_project_manuterms.rdf"):
    # filename = "res/pp_project_manuterms.rdf"   # currently 2188 concepts
    # filename = "res/testfile.rdf"
    g = rdflib.Graph()
    g = g.parse(location=filename, format="application/rdf+xml")
    loader = RDFLoader(g)
    concepts = loader.getConcepts()  # type is skos.Concepts, despite just being a list, so we need to transform it

    # make it a list of uri's. We need a list of strings so we can actually do stuff with it.
    concept_uri_list = []
    for c in concepts:
        concept_uri_list.append(c)
    return concept_uri_list


# TODO unicode stuff where values are lists
def parse_response(concepts, thesaurus):
    """
    Takes the JSON response and parses it into a python dict with additional key-values pairs that can be used later
    when calculating metrics. Also increments overall importance if it finds any externally linked keys.
    :param concepts: concepts with properties in JSON (dict) form
    :param thesaurus: custom representation of the thesaurus
    :return:
    """
    for node in concepts:
        uri = node['uri'].encode('utf-8')                               # decode the uri for our thesaurus
        thesaurus[uri] = {}

        # create skeleton for later calculations
        thesaurus[uri].update({IMPORTANCE_SCORE: 0})
        thesaurus[uri].update({NUM_RELATIONS: 0})
        thesaurus[uri].update({FREQUENCY: 0})

        for key in node:
            utf_key = key.encode('utf-8')                           # get rid of unicode
            value = node[key]                                       # don't encode value, will mess up if it's a list
            if utf_key != 'definitions':                            # skip definitions - too wordy, don't need them
                thesaurus[uri].update({utf_key: value})             # add key-value pair into that concept entry
            if utf_key in EXTERNAL_PROPERTIES:                      # if any externally linked data, increment score
                thesaurus[uri][IMPORTANCE_SCORE] += EXTERNAL_LINK_FACTOR


def query_api(uri_list, index=0):

    url = THESAURUS_URL
    url += 'concepts?properties=all'
    itr = 0
    while itr < MAX_ITEM_PER_REQUEST and index < len(uri_list):
        uri = uri_list[index]
        url += '&concepts=' + uri
        index += 1
        itr += 1

    response = requests.get(url, auth=HTTPBasicAuth('ppuser', 'infoneer'))

    if response.text == '[]' or response.text == '[ ]':
        return None, 0
    else:
        return json.loads(response.text), index


# TODO make collect cmd capable (kwargs)
def collect():
    """
    Returns a dictionary of all concepts and their respective properties
    :return: dict of thesaurus
    """
    uri_list = get_uris()
    thesaurus = {}
    num_items_requested = 0

    sys.stdout.write("collecting thesaurus data")    # start loading message
    while num_items_requested < len(uri_list):
        response, num_items_requested = query_api(uri_list, num_items_requested)

        if response is not None:
            parse_response(response, thesaurus)
            sys.stdout.write('.')   # for the loading message

    print "done."

    # target = u'http://dbpedia.org/resource/Pincer_%28tool%29'
    # print thesaurus[target]
    # for key in thesaurus:
    #     print key, thesaurus[key].keys(), type(thesaurus[key][NUM_RELATIONS])
    return thesaurus


if __name__ == "__main__":
    collect()
