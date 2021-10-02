import gzip
import math

try:
    import ujson as json
except ImportError:
    import json


def read_wordfreq(filename):
    """
    Gzipped word - frequency file, one entry per line <word><space><frequency>,
    sorted descending by frequency.
    """
    with gzip.open(filename) as fin:
        wordfreq = json.loads(fin.read().decode("utf-8"))
    return wordfreq


def zipf(wordlist):
    log_len = math.log(len(wordlist))
    word_cost = {
        w: math.log((r + 1) * log_len) for r, w in enumerate(wordlist)
    }
    return word_cost


def neg_log_prob(wordfreq):
    log_denom = math.log(sum(wordfreq.values()))
    wordp = {w: log_denom - math.log(wordfreq[w]) for w in wordfreq}
    return wordp


class Segment(object):
    def __init__(self, word_freq_file=None, cost_type="prob"):
        if word_freq_file is None:
            word_freq_file = "enwiki_vocab_min200_freq.json.gz"
        self.word_freq = read_wordfreq(word_freq_file)
        self.max_len = max(len(w) for w in self.word_freq.keys())

        self.cost = None
        if cost_type == "zipf":
            self.cost = zipf(self.word_freq.keys())
        elif cost_type == "prob":
            self.cost = neg_log_prob(self.word_freq)
        else:
            raise ValueError("unknown cost_type")

        self.cost_type = cost_type
        self.max_cost = 1.0e16

    def min_cost_ptr(self, idx, text, costs):
        return min(
            (
                cand_cost
                + self.cost.get(
                    text[idx - j - 1: idx].lower(), self.max_cost
                ),
                j + 1,
            )
            for j, cand_cost in enumerate(
                reversed(costs[max(0, idx - self.max_len): idx])
            )
        )

    def __call__(self, text):

        # forward step
        costs = [0.0]
        costs_ptr = [(0.0, 0)]
        for idx in range(1, len(text) + 1):
            min_cost, min_idx = self.min_cost_ptr(idx, text, costs)
            costs_ptr.append((min_cost, min_idx))
            costs.append(min_cost)

        # backtrack
        words = list()
        seg_cost = 0.0
        ptr = len(costs_ptr) - 1
        while ptr > 0:
            mincost, min_idx = costs_ptr[ptr]
            words.append(text[ptr - min_idx: ptr])
            seg_cost += mincost
            ptr -= min_idx
        if self.cost_type == "prob":
            seg_cost = math.exp(-seg_cost)

        return list(reversed(words)), seg_cost
