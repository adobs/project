from okcupyd.session import Session
from okcupyd.json_search import SearchFetchable
from okcupyd.user import User
# from okcupyd.html_search import SearchFetchable
def is_signed_in(screenname, password):
    try:
        session = Session.login(screenname, password)
        user = User(session=session)
    except Exception as e:
        print (e)
        return "False"   
    
    return "True"