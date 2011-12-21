import pickle
pickles = open('pickled.pic','r')
repdataset = pickle.load(pickles)
pickles.close()

import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(repdataset)

