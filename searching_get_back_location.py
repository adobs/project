from __future__ import generators
from okcupyd.session import Session
from okcupyd.json_search import SearchFetchable
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import nltk
# nltk.download()
import operator

session = Session.login('adobsthecat', 'meow6996')

for profile in SearchFetchable(session=session)[:5]:
            try:
                if profile.essays.self_summary:
                    print profile
                    print profile.location

            except Exception as e:
                # e will be the exception object
                print type(e)
                continue
