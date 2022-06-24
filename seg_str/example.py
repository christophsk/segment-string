from seg_str.segment import Segment
import time

texts = [
    "spam",
    "theman",
    "speedofart",
    "insufficientnumbers",
    "Mylifeboatisfullofeels",
    "iamnotanumberiamaperson",
    "Asgregorsamsaawokeonemorningfromuneasydreamshefoundhimselftransformedinhisbedintoagiganticinsect",
    "faroutintheunchartedbackwatersoftheunfashionableendofthewesternspiralarmofthegalaxyliesasmallunregardedyellowsun",
]

for cost_t in ("prob", "zipf"):
    seg = Segment(cost_type=cost_t)
    start = time.time()
    for txt in texts:
        word_list, seg_cost = seg(txt)
        print(
            "{}: {} = {}, obj = {:3.2f}".format(
                cost_t, txt, " ".join(word_list), seg_cost
            )
        )
    print("time: {:0.4f}".format(time.time() - start))
    print()
