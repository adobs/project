from okcupyd.session import Session
from okcupyd.json_search import SearchFetchable
from okcupyd.user import User
# from okcupyd.html_search import SearchFetchable
def send_message(screenname, password, minimum_age, maximum_age, gentation, message, num, word="I"):
    session = Session.login(screenname, password)
    user = User(session=session)
    print screenname
    print password
    print minimum_age
    print maximum_age
    print gentation
    print message
    print num
    print word
    # location="San Francisco"
    # radius=10
    # minimum_age=40
    # maximum_age=55
    # gentation="women"
    # word="fun"
    # (session=session, location=location, radius=radius, minimum_age= minimum_age, maximum_age=maximum_age, gentation="bisexual")[:5]:
    for profile in user.search(minimum_age=minimum_age, maximum_age=maximum_age, gentation=gentation)[:num]:
        if word in profile.essays.self_summary:
            profile.message(message)

