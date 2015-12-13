"""
signing_in.py

Uses the okcupyd library to see if a user can log in to OkCupid with the given 
credentials.
"""

from okcupyd.session import Session
from okcupyd.user import User

def is_signed_in(screenname, password):
    """ Returns boolean that evalutes if OkCupid credentials are valid """
    
    try:
        session = Session.login(screenname, password)
        user = User(session=session)
    except Exception as e:
        print (e)
        return "False"   
    
    return "True"