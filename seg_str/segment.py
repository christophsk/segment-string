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
import os

import numpy as np
from scipy.special import logsumexp

try:
    import ujson as json
except ImportError:
    import json


class Segment:
    def __init__(self, word_freq_file=None, cost_type="prob"):
        """
        This uses a dynamic programming method to optimally insert spaces into a
        string of letters, e.g., "theman" -> "the man". The objective is to
        maximize either the negative log likelihood or the log Zipf
        rank-frequency.

        The default language model is the frequency distribution of words from
        English Wikipedia with a minimum frequency of 200 in the included file
        `enwiki_vocab_min200_freq.json.gz`.

        Args:
            word_freq_file (str): The schema is `{word: frequency}`
                sorted ascending by frequency, encoded utf-8, gzipped.

            cost_type (str): One of (`prob`, `zipf`), default = `prob`

        Raises:
            ValueError if `cost_type` is not recognized

        Examples:
            segment = Segment()
            words, cost = segment("theman")

            words = ["the", "man"]
            log cost = 12.23
        """
        if word_freq_file is None:
            here = os.path.dirname(os.path.abspath(__file__))
            word_freq_file = os.path.join(
                here, "enwiki_vocab_min200_freq.json.gz"
            )

        word_freq = self._read_wordfreq(word_freq_file)
        self.max_len = max(len(w) for w in word_freq.keys())

        if cost_type == "zipf":
            self.log_costs = self._log_zipf(word_freq.keys())
        elif cost_type == "prob":
            self.log_costs = self._neg_log_prob(word_freq)
        else:
            raise ValueError("unknown cost_type")

        self.cost_type = cost_type
        self.max_cost = 1.0e16

    def __call__(self, text):
        """
        Run the Forward-Backward method on `text` to find a segmentation that
        is optimal with respect to the objective function.

        Args:
            text (str): string to be segmented

        Returns:
            list, float: The list of segmented words, log cost of segmentation
        """
        # forward pass
        log_costs_idx = np.array([(0.0, 0)])  # log_costs, previous index
        for idx in range(1, len(text) + 1):
            min_cost_ptr = self._forward_step(idx, text, log_costs_idx[:, 0])
            log_costs_idx = np.vstack([log_costs_idx, min_cost_ptr])

        # backward pass
        words = list()
        prev_index = int(log_costs_idx.shape[0]) - 1
        while prev_index > 0:
            index = int(log_costs_idx[prev_index][1])
            words.append(text[prev_index - index: prev_index])
            prev_index -= index
        log_cost = logsumexp(log_costs_idx[1:, ])
        return list(reversed(words)), log_cost

    def _forward_step(self, idx, text, log_costs):
        return min(
            (
                log_cand_cost
                + self.log_costs.get(
                    text[idx - j - 1: idx].lower(), self.max_cost
                ),
                j + 1,
            )
            for j, log_cand_cost in enumerate(
                reversed(log_costs[max(0, idx - self.max_len): idx])
            )
        )

    @staticmethod
    def _read_wordfreq(filename):
        with gzip.open(filename) as fh:
            wordfreq = json.loads(fh.read().decode("utf-8"))
        return wordfreq

    @staticmethod
    def _neg_log_prob(wordfreq):
        log_denom = np.log(sum(wordfreq.values()))
        return {w: log_denom - np.log(wordfreq[w]) for w in wordfreq}

    @staticmethod
    def _log_zipf(wordlist):
        return {w: np.log((r + 1) * 2.5) for r, w in enumerate(wordlist)}
