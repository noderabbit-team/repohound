#xsearch - search with the xgoogle wrapper 
from xgoogle.search import GoogleSearch, SearchError
try:
  q = '"manage.py" "settings.py" "urls.py" intitle:"- Github" -inurl:/wiki/ -inurl:manage.py -inurl:commits -inurl:README -inurl:gist site:github.com'
  gs = GoogleSearch(q, debug=True)
  print gs.num_results
  gs.results_per_page = 1000
  results = gs.get_results()
  for res in results:
    #print res.title.encode('utf8')
    #print res.desc.encode('utf8')
    print res.url.encode('utf8')
    #print
except SearchError, e:
  print "Search failed: %s" % e
