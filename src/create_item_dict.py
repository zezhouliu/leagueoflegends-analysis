import json
import numpy as np

outfilename = "SRitems.npy"

with open('allitems.json') as all_items:
    items =json.load(all_items)

print "Loaded items json file"

item_id_list = [k for (k,v) in items.iteritems() if "maps" not in v or "1" not in v["maps"]]

print "Filtered items"

np.save(outfilename, item_id_list)

print "Saved item map in", outfilename