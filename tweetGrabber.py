import sys
import twitter
from twitterCredentials import api

results = api.GetSearch(raw_query="q=%23" + sys.argv[1] + "&count=1000")
results = [res.text for res in results]
print(str(results).encode('utf-8'))

