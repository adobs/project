from mechanize import Browser
br = Browser()

# Ignore robots.txt
br.set_handle_robots( False )
# Google demands a user-agent that isn't a robot
br.addheaders = [('User-agent', 'Firefox')]

# Retrieve the Google home page, saving the response
br.open( "https://www.okcupid.com/" )

for f in br.forms():
    # print f
    f.set_all_readonly(False)




br.select_form(nr=0)
br.form[ 'orientation_dropdown' ] = ["1"]
br.form["gender_dropdown"] = ["1"]

br.submit()
# print br.response().read()
# print br.geturl()


br.select_form(nr=0)
br.form[ 'birthmonth' ] = "03"
br.form["birthday"] = "04"
br.form["birthyear"] = "1989"
br.form["zip_or_city"] = "94108" 
br.form["email"] = "saysmith123@gmail.com" 
br.form["email2"] = "saysmith123@gmail.com" 

br.submit()

br.select_form(nr=0)
br.form[ 'screenname' ] = "apple3shoney1298"
br.form["password"] = "feiwan23499"
br.submit()

print br.response().read()
print "###############"
print br.geturl()