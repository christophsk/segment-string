# splittingstringsusingdynamicprogramming 
### _splitting strings using dynamic programming_

This demonstrates dynamic programming applied to optimally segmenting a contiguous string into words. 
The default language model is the ranked frequency distribution of unigrams from (English) Wikipedia, 
each with a frequency >= 200.

From this, a probability distribution or a Zipf rank-frequency distribution is defined 
over the ranked unigrams. The objective is to maximize the probability / Zipf of a 
particular segmentation.

Essentially, this is the Viterbi method applied to a unigram language model. For an interesting treatment,
see the article by [Peter Novig](http://norvig.com/ngrams/ch14.pdf).

The user can also supply their own (UTF-8 encoded) JSON file of word-frequency
pairs, sorted descending by frequency, gzipped.

## Example
See `example.py` for example usage:

```python
from seg_str.segment import Segment

seg = Segment(cost_type="prob", word_freq_file=None)  # defaults are shown
seg("mylifeboatisfullofeels")

# returns ['my', 'lifeboat', 'is', 'full', 'of', 'eels'], 51.29
```
# License
MIT License, copyright &copy; 2021 Chris Skiscim

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWAR