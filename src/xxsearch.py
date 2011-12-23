import time, random
from xgoogle.search import GoogleSearch, SearchError

f = open('a.txt','wb')

for i in range(0,100):
    wt = random.uniform(3, 10)
    q = '"manage.py" "settings.py" "urls.py" intitle:"- Github" -inurl:/wiki/ -inurl:/blob/ -inurl:manage.py -inurl:commits -inurl:README -inurl:gist site:github.com'
    gs = GoogleSearch(q)
    gs.results_per_page = 100
    gs.page = i
    results = gs.get_results()
    #Try not to annnoy Google, with a random short wait
    time.sleep(wt)
    print 'This is the %dth iteration and waited %f seconds' % (i, wt)
    for res in results:
        f.write(res.url.encode("utf8"))
        f.write("\n")
    f.flush()

print "Done"
f.close()
