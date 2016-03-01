

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



def query_corpus():
    """
    this method sends an http request to the PoolParty API to retrieve all extracted concepts from the given corpus
    :return: JSON object of all extracted concepts and their associated metrics
    """

    url = "http://infoneer.poolparty.biz/PoolParty/api/corpusmanagement/" \
          "1DBC67E1-7669-0001-8A4A-F4B06F409540/results/" \
          "extractedterms?corpusId=corpus:7183eaa9-ddac-4a8f-82b6-1e62a31610fa"

    result = requests.get(url, auth=HTTPBasicAuth('ppuser', 'infoneer'))

    if result.text == "[]" or result.text == "[ ]":
        return None
    else:
        return json.loads(result.text)


