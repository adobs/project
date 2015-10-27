from okcupyd.session import Session
from okcupyd.json_search import SearchFetchable
# from okcupyd.html_search import SearchFetchable

session = Session.login('adobsthecat', 'woof6996')
location="San Francisco"
radius=10
minimum_age=40
maximum_age=55
gentation="women"
word="fun"
# (session=session, location=location, radius=radius, minimum_age= minimum_age, maximum_age=maximum_age, gentation="bisexual")[:5]:

for profile in SearchFetchable(session=session, location=location, radius=radius, minimum_age= minimum_age, maximum_age=maximum_age, gentation=gentation)[:5]:
    if word in profile.essays.self_summary:
        profile.message("you're hawt, girlie...")
