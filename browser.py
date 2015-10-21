import re 
from mechanize import Browser
br = Browser()

# Ignore robots.txt
br.set_handle_robots( False )
# Google demands a user-agent that isn't a robot
br.addheaders = [('User-agent', 'Firefox')]

# Retrieve the Google home page, saving the response
br.open( "https://m.okcupid.com/signup" )
# br.open("https://www.google.com")

for f in br.forms():
    print f
    f.set_all_readonly(False)



br.select_form(nr=0)



# Select the search box and search for 'foo'
# br.select_form( 'signup_form' )
br.form[ 'orientation' ] = ["1"]
br.form["gender"] = ["1"]
br.form["birthmonth"]=["1"]
br.form["birthday"]=["1"]
br.form["birthyear"] =["1990"]
# br["lquery"]=94108
br.form["email"]=""
br.form["screenname"]="aqqwwcce"
br.form["password"]="meow6996"

# br.select_form(name="signup_form")
# br["orientation"] =[1]

# formcount = 0
# for frm in br.forms():
#     if str(frm.attrs["id"]) == "orientation":
#         break
#     formcount = formcount +1

# br.select_form(nr=5) #orientation
 



# # Get the search results
br.submit()
print br.response().read()
print br.geturl()
