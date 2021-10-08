from segs.segment import Segment

texts = [
        "iamnotanumberiamaperson",
        "splittingstringsusingdynamicprogramming",
        "mylifeboatisfullofeels",
        "asgregorsamsaawokeonemorningfromuneasydreamshefoundhimselftransformedinhisbedintoagiganticinsect",
        "wheninthecourseofhumaneventsitbecomesnecessary",
    ]

cost_t = "prob"
seg = Segment(cost_type=cost_t)
for txt in texts:
    word_list, seg_cost = seg(txt)
    print(
        "{}: {} = \n\t{}, obj = {:3.2f}".format(
                cost_t, txt, " ".join(word_list), seg_cost
        )
    )
