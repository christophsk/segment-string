# MIT License
# Copyright (c) 2021 Chris Skiscim
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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
    word_cost = {w: math.log((r + 1) * 2.0) for r, w in enumerate(wordlist)}
    return word_cost


def neg_log_prob(wordfreq):
    log_denom = math.log(sum(wordfreq.values()))
    wordp = {w: log_denom - math.log(wordfreq[w]) for w in wordfreq}
    return wordp


class Segment:
    def __init__(self, word_freq_file=None, cost_type="prob"):
        if word_freq_file is None:
            word_freq_file = "segs/enwiki_vocab_min200_freq.json.gz"

        word_freq = read_wordfreq(word_freq_file)
        self.max_len = max(len(w) for w in word_freq.keys())

        if cost_type == "zipf":
            self.cost = zipf(word_freq.keys())
        elif cost_type == "prob":
            self.cost = neg_log_prob(word_freq)
        else:
            raise ValueError("unknown cost_type")

        self.cost_type = cost_type
        self.max_cost = 1.0e16

    def _min_cost_ptr(self, idx, text, costs):
        return min(
            (
                cand_cost
                + self.cost.get(
                    text[idx - j - 1 : idx].lower(), self.max_cost
                ),
                j + 1,
            )
            for j, cand_cost in enumerate(
                reversed(costs[max(0, idx - self.max_len) : idx])
            )
        )

    def __call__(self, text):
        # forward step
        costs = [0.0]
        costs_ptr = [(0.0, 0)]
        for idx in range(1, len(text) + 1):
            min_cost, min_idx = self._min_cost_ptr(idx, text, costs)
            costs_ptr.append((min_cost, min_idx))
            costs.append(min_cost)

        # backtrack
        words = list()
        seg_cost = 0.0
        ptr = len(costs_ptr) - 1
        while ptr > 0:
            mincost, min_idx = costs_ptr[ptr]
            words.append(text[ptr - min_idx : ptr])
            seg_cost += mincost
            ptr -= min_idx
        return list(reversed(words)), seg_cost


if __name__ == "__main__":
    texts = [
        "iamnotanumberiamaperson",
        "splittingstringsusingdynamicprogramming",
        "mylifeboatisfullofeels",
    ]
    cost_t = "prob"
    seg = Segment(cost_type=cost_t)
    for txt in texts:
        s, c = seg(txt)
        print("{}: {} = {}, obj = {:3.2f}".format(cost_t, txt, " ".join(s), c))
