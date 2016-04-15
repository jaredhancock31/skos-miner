#!/usr/bin/env python
import rdflib
import skos
from constants import *

# filename = 'res/pp_project_carproject.rdf'
filename = 'res/pp_project_manuterms.rdf'
g = rdflib.Graph()
g.load(filename)

g = rdflib.Graph()
g = g.parse(location=filename, format="application/rdf+xml")
thesaurus = skos.RDFLoader(g)

keys = thesaurus.keys()
values = thesaurus.values()
concept = thesaurus['http://infoneer.poolparty.biz/Processes/347']

print concept.prefLabel
print 'relateds: ', concept.related
print 'syn: ', concept.synonyms
# print 'relatedMatch: '. con.relatedMatch


class SkosTool(object):
    """
     TODO doc
    """

    def __init__(self, rdf_file):
        self.rdf_file = rdf_file
        self.__g = rdflib.Graph()
        self.__g.parse(location=rdf_file, format='application/rdf+xml')
        self.thesaurus = skos.RDFLoader(self.__g)
        self.keys = self.thesaurus.keys()
        # setup separate dict (with same keys) with a skeleton to house our calculated metrics
        self.metrics = {key: {PREF_LABEL: '',
                              IMPORTANCE_SCORE: 0,
                              NUM_RELATIONS: 0,
                              NUM_EXTERNAL: 0,
                              FREQUENCY: 0} for key in self.keys}

    def parse(self):
        for concept in self.keys:
            pass




