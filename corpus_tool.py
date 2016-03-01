

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


def parse_response(response):
    """
    parse json object and create list of concepts and their frequencies
    :param response:
    :return:
    """
    pass


def query_corpus(startIdx=0):
    """
    this method sends an http request to the PoolParty API to retrieve all extracted concepts from the given corpus
    :return: JSON object of all extracted concepts and their associated metrics
    """

    url = "http://infoneer.poolparty.biz/PoolParty/api/corpusmanagement/" \
          "1DBC67E1-7669-0001-8A4A-F4B06F409540/results/" \
          "concepts?corpusId=corpus:7183eaa9-ddac-4a8f-82b6-1e62a31610fa&startIndex="+startIdx

    result = requests.get(url, auth=HTTPBasicAuth('ppuser', 'infoneer'))

    if result.text == "[]" or result.text == "[ ]":
        return None
    else:
        return json.loads(result.text)


def main():
    idx = 0
    response = query_corpus(idx)
    # TODO parse_response(response)
    while response is not None:
        idx += 20
        response = query_corpus(idx)
        # TODO parse_response(response)