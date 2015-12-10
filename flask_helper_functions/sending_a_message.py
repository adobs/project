from okcupyd.session import Session
from okcupyd.user import User

def send_message(screenname, password, minimum_age, maximum_age, location, radius, gentation, message, num):
    session = Session.login(screenname, password)
    user = User(session=session)
    try:
        for profile in user.search(minimum_age=minimum_age, maximum_age=maximum_age, location=location, radius=radius, gentation=gentation)[:num]:
        # for profile in user.search(minimum_age=minimum_age, maximum_age=maximum_age)[:num]:

           profile.message(message)

    except Exception as e:
        print type(e)
        return "I couldn't find anyone with those specifications"
