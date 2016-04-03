
from constants import *
from django.utils.http import urlunquote_plus
import sys


def make_pref_label(uri):
    uri = uri.split('/')[-1]
    uri = uri.replace('_', ' ')
    return uri


# TODO how should we handle missing concepts? just add them in, or separate from group?
def calc_related_scores(thesaurus):
    """
    Runs through our thesaurus, finds relateds and increments them at their key in the dict. If a related isn't found
    in our thesaurus, it's likely an external concept, and is added to a separate dict and returned in its own table
    :param thesaurus: dict of collected concepts from API
    :return: updated thesaurus with releted scores
    :return: dict of concepts found in relateds, but not found in overall thesaurus dict
    """
    missing_concepts = {}               # concepts found in relateds but not found in our overall thesaurus

    sys.stdout.write('calculating relation metrics...')
    for concept in thesaurus:
        if RELATEDS in thesaurus[concept].keys():
            for related in thesaurus[concept][RELATEDS]:
                rel_uri = related.encode('utf-8')                                   # get rid of unicode

                if rel_uri in thesaurus:
                    thesaurus[rel_uri][NUM_RELATIONS] += 1
                    thesaurus[rel_uri][IMPORTANCE_SCORE] += REL_SCORE_FACTOR        # update overall score
                else:
                    # concept wasn't found, so create an entry for it
                    missing_concepts[rel_uri] = {PREF_LABEL: make_pref_label(rel_uri),
                                                 NUM_RELATIONS: 1,
                                                 FREQUENCY: 0,
                                                 IMPORTANCE_SCORE: REL_SCORE_FACTOR}

    return thesaurus, missing_concepts





