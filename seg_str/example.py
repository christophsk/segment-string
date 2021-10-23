from seg_str.segment import Segment

texts = [
        "iamnotanumberiamaperson",
        "splittingstringsusingdynamicprogramming",
        "mylifeboatisfullofeels",
        "asgregorsamsaawokeonemorningfromuneasydreamshefoundhimselftransformedinhisbedintoagiganticinsect",
        "wheninthecourseofhumaneventsitbecomesnecessary",
        "theman",
    ]

for cost_t in ("prob", "zipf"):
    seg = Segment(cost_type=cost_t)
    for txt in texts:
        word_list, seg_cost = seg(txt)
        print(
            "{}: {} = \n\t\t{}, obj = {:3.2f}".format(
                cost_t, txt, " ".join(word_list), seg_cost
            )
        )
    print()
