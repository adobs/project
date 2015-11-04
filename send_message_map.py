from okcupyd.session import Session
from okcupyd.user import User
from okcupyd.profile import Profile

def send_message_map(username, password, recipient_list, message):
    session = Session.login(username, password)
    user = User(session=session)
    for recipient in recipient_list:
        user.message(username=recipient, message_text=message)

