import yaml
import cgi
import wsgiref.handlers
from google.appengine.ext import (
    webapp, db
)
from gdata.analytics.client import (
    AnalyticsClient, ProfileQuery
)

class GoogleAccount(db.Model):
    email = db.StringProperty(required=True)
    password = db.StringProperty(required=True)

class AnalyticsTest(webapp.RequestHandler):
    def get(self):
        account = GoogleAccount.all().fetch(1)[0]
        client = AnalyticsClient()
        client.ClientLogin(account.email, account.password, 'gpc-test')
        profile_query = ProfileQuery()
        feed = client.GetMgmtFeed(profile_query)
        self.response.out.write(yaml.dump(feed))

application = webapp.WSGIApplication([
    ('/', AnalyticsTest)
], debug=True)

def main():
    wsgiref.handlers.CGIHandler().run(application)

if __name__ =='__main__':
    main()
