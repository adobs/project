import okcupyd
okcupyd.session.do_login("adobsthecat","meow6996")
me = okcupyd.user.User()
me.from_credentials("adobsthecat", "meow6996")
print me.profile

###############################################

<type 'exceptions.UnicodeEncodeError'>
--Return--
> /home/user/src/dobs/import_session.py(87)searchOKC()->None
-> import pdb; pdb.set_trace()
