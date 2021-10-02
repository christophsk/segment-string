# stringsegmentationbydynamicprogramming
### _string segmentation by dynamic programming_

This didactic implementation shows how to segment a string this using dynamic programming. 
Two different (linear) objective functions are demonstrated, one probabilistic and one based on
Zipf's frequency-rank distribution. The underlying language model is the frequency distribution
of (English) Wikipedia having a minimum frequency of 200.

See the [WordNinja](https://github.com/keredson/wordninja) package using one of the
objective functions considered here.

## Example
```python
seg = Segment(cost_type="prob")  # default
seg("mylifeboatisfullofeels")

# returns (['my', 'lifeboat', 'is', 'full', 'of', 'eels'],1.570e-76)
```