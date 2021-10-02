# stringsegmentationbydynamicprogramming
### _string segmentation by dynamic programming_

This didactic implementation shows how to segment a string this using dynamic programming. 
Two different (linear) objective functions are demonstrated, one probabilistic and one based on
Zipf's frequency-rank distribution. The underlying language model is the frequency distribution
of (English) Wikipedia having a minimum frequency of 200.

See the [WordNinja](https://github.com/keredson/wordninja) package which uses one of the
objective functions considered here.

## Example
```python
seg = Segment(cost_type="prob")  # default
seg("mylifeboatisfullofeels")

# returns (['my', 'lifeboat', 'is', 'full', 'of', 'eels'],1.570e-76)
```
# License
MIT License Copyright &copy; 2021 Chris Skiscim

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