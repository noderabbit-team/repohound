import pickle
import time
from github2.client import Github

github = Github()

f = open('data.txt', 'r')
pickles = open('pickled.pic','w')
repdataset = {}
for line in f:
    try:
        repo = line.split('https://github.com/')[1].strip()
        print "repo <%s>" % repo
        repodata = dict(github.repos.show(str(repo)))
        repdataset[repo] = repodata
        time.sleep(2)
    except (IndexError, RuntimeError), ex:
        print ex
        time.sleep(2)

f.close()
pickle.dump(repdataset, pickles)
pickles.close()

import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(repdataset)