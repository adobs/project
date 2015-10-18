import okcupyd
okcupyd.session.do_login("adobsthecat","meow6996")
me = okcupyd.user.User()
me.from_credentials("adobsthecat", "meow6996")
print me.profile