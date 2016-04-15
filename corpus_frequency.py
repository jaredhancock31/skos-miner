

"""
Author: Jared Hancock
Date: Feb 2016
Email: jaredhancock31@gmail.com
"""
import rdflib
import json
import sys
import requests
from requests.auth import HTTPBasicAuth
from skos import RDFLoader
from collections import defaultdict
from django.utils.http import urlunquote_plus
from constants import *


def calc_freq_scores(response, thesaurus):
    """
    given the overall thesaurus, iterate through and fill in frequency data
    :param thesaurus:
    :return:
    """
    missing_concepts = {}
    for concept in response:
        label = concept['name'].encode('utf-8')
        freq = concept[FREQUENCY]                                                   # find entry in overall table
        if label.lower() in thesaurus:
            thesaurus[label.lower()][FREQUENCY] = freq                                  # update frequency
            thesaurus[label.lower()][IMPORTANCE_SCORE] += (freq * FREQ_SCORE_FACTOR)    # update overall score
        else:
            missing_concepts[label.lower()] = {PREF_LABEL: label,
                                               FREQUENCY: freq,
                                               IMPORTANCE_SCORE: (freq * FREQ_SCORE_FACTOR),
                                               NUM_RELATIONS: None}
    return missing_concepts


def parse_into_dict(response):
    concepts = {}
    for con in response:
        name = urlunquote_plus(con['name']).encode('utf-8')
        freq = con['frequency']
        concepts[name.lower()] = freq
    return concepts


def query_corpus(startIdx=0):
    """
    this method sends an http request to the PoolParty API to retrieve all extracted concepts from the given corpus
    :return: JSON object of all extracted concepts and their associated metrics
    """

    url = "http://infoneer.poolparty.biz/PoolParty/api/corpusmanagement/" \
          "1DBC67E1-7669-0001-8A4A-F4B06F409540/results/" \
          "concepts?corpusId=corpus:7183eaa9-ddac-4a8f-82b6-1e62a31610fa&startIndex="+str(startIdx)

    result = requests.get(url, auth=HTTPBasicAuth('ppuser', 'infoneer'))

    if result.text == "[]" or result.text == "[ ]":
        return None
    else:
        return json.loads(result.text)


def get_corpus_data():
    idx = 0
    response = query_corpus(idx)
    concept_list = {}
    # missing_concepts = {}

    sys.stdout.write("collecting frequency metrics")  # make a kind of loading message
    while response is not None:
        concept_list.update(parse_into_dict(response))
        # missing_concepts.update(calc_freq_scores(response, thesaurus))
        idx += 20
        response = query_corpus(idx)
        sys.stdout.write('.')  # make a kind of loading message

    print('done.')
    # print concept_list.items()
    # for f in concept_list:
    #     print(f + ':' + str(concept_list.get(f)))

    return concept_list
    # return thesaurus, missing_concepts


if __name__ == '__main__':
    get_corpus_data()
