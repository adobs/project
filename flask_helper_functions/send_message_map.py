from okcupyd.session import Session
from okcupyd.user import User

def send(username, password, recipient_list, message):
    """If logged in, sends a message to a list of recipients"""

    session = Session.login(username, password)
    user = User(session=session)
    for recipient in recipient_list:
        user.message(username=recipient, message_text=message)
    
    return "success"

