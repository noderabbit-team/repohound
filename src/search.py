# This example request includes an optional API key which you will need to
# remove or replace with your own key.
# Read more about why it's useful to have an API key.
# The request also includes the userip parameter which provides the end
# user's IP address. Doing so will help distinguish this legitimate
# server-side traffic from traffic which doesn't come from an end-user.
#url = ('https://ajax.googleapis.com/ajax/services/search/web'
#       '?v=1.0&q=Paris%20Hilton&key=INSERT-YOUR-KEY&userip=USERS-IP-ADDRESS')

# See here: http://stackoverflow.com/questions/4506173/google-search-api-only-returning-4-results

import datetime
import simplejson
import time
import urllib

backoff = BACKOFF = 60
num_queries = 10000
query = urllib.urlencode({'q' : '"manage.py" "settings.py" "urls.py" intitle:"- Github" -inurl:/wiki/ -inurl:manage.py -inurl:commits -inurl:README -inurl:gist site:github.com'})
url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
start = 0
out = open('data.txt', 'aw')
out.seek(0, 2)
out.write(40 * '*' + '\n' + str(datetime.datetime.now()) + '\n')
while start < num_queries:
    request_url = '{0}&start={1}'.format(url, start)
    search_results = urllib.urlopen(request_url)
    json = simplejson.loads(search_results.read())
    try:
        results = json['responseData']['results']
        for i in results:
            out.write(i['title'] + ": " + i['url'] + "\n")
        start += 4
        #we were successful, so return to normal backoff
        backoff = BACKOFF
        out.flush()
    except TypeError:
        print '** empty result set at', start, 'backing off', backoff
        time.sleep(backoff)
        # and remember to double it next time, if we still have problems
        backoff *= 2
