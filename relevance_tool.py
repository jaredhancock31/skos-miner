"""
    Author: Jared Hancock
    Date: March 2016
    Email: jaredhancock31@gmail.com
"""
import corpus_frequency
import thesaurus_related
from collections import OrderedDict


def get_most_important_concept(scores):
    return max(scores.iterkeys(), key=lambda key: scores[key])


def normalize_on_max(scores, hi_score=None):
    if hi_score is None:
        hi_score = get_most_important_concept(scores)

    for key in scores:
        scores[key] = round((float(scores.get(key)) / hi_score), 4)

    return scores


def normalize_on_sum(scores, total=None):
    if total is None:
        return None
    for key in scores:
        scores[key] = round((float(scores.get(key)) / total), 4)

    return scores


def main():
    relateds = thesaurus_related.get_relateds()
    frequencies = corpus_frequency.get_all_frequencies()
    relevance = {}              # has all metrics associated with a key
    importance_scores = {}      # importance metric only value for key
    total_imp = 0               # sum of total importance in case we want to normalize against the sum
    max_score = 0

    for label, num_related in relateds.items():
        if label in frequencies:
            freq = frequencies.get(label)   # get frequency from corpus list
            importance = round(((0.3 * num_related) + (0.7 * freq)), 4)
            total_imp += importance
        else:
            importance = round((0.3 * num_related), 4)

        if importance > max_score:
            max_score = importance
        importance_scores[label] = importance

        # ********************** uncomment line below if you want to keep a more comprehensive list ****************
        # relevance[label] = {'related': num_related, 'frequency': freq, 'importance': importance}

    # sort the dict by highest importance
    # ordered_rel = OrderedDict(sorted(relevance.iteritems(), reverse=True, key=lambda x: x[1]['importance']))
    # for concept in ordered_rel:
    #     print concept + ": " + str(ordered_rel[concept]['importance'])

    importance_scores = normalize_on_max(importance_scores, max_score)

    print("\n===================================================")

    # for key in importance_scores:
    #     print key + ' : ' + str(importance_scores.get(key))

    for k in sorted(importance_scores, key=importance_scores.get, reverse=True):
        print '{0:45} {1:.3f}'.format(k, importance_scores[k])


if __name__ == "__main__":
    main()
