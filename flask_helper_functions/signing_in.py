from okcupyd.session import Session
from okcupyd.user import User

def is_signed_in(screenname, password):
    try:
        session = Session.login(screenname, password)
        user = User(session=session)
    except Exception as e:
        print (e)
        return "False"   
    
    return "True"