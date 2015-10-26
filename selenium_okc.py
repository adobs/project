from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
from pyvirtualdisplay import Display
from json import dumps

# display = Display(visible=0, size=(800, 600))
# display.start()


driver = webdriver.Firefox()
driver.get("https://www.okcupid.com/")
# time.sleep(10)

# select orientation
driver.execute_script("document.querySelector('#orientation_container').innerHTML = '<input type\"hidden\" id=\"orientation\" name=\"orientation\" value=\"3\" data-default=\"1\">';")

# select gender
driver.execute_script("document.querySelector('#gender_container').innerHTML = '<input type=\"hidden\" id=\"gender\" name=\"gender\" value=\"1\" data-default=\"2\">';")

# click green next button
(driver.find_element_by_class_name('next_page')).click()

################################ SECOND PAGE ##################################################################

# input birthmonth
driver.execute_script("document.querySelector('#birthmonth').value='02';")

# input birthday
driver.execute_script("document.querySelector('#birthday').value='04';")

# input birthyear
driver.execute_script("document.querySelector('#birthyear').value='1990';")

# input zip
driver.execute_script("document.querySelector('#zip_or_city').value='94108';")

# input email
driver.execute_script("document.querySelector('#email1').value='dobs@northwestern.edu';")

# input email (confirming)
driver.execute_script("document.querySelector('#email2').value='dobs@northwestern.edu';")

#TAB 5 times
birthmonth = driver.find_element_by_id("birthmonth")
birthmonth.send_keys(Keys.TAB)

birthday = driver.find_element_by_id("birthday")
birthday.send_keys(Keys.TAB)

birthyear = driver.find_element_by_id("birthyear")
birthyear.send_keys(Keys.TAB)

country_select = driver.find_element_by_id("country_selectContainer")
country_select.send_keys(Keys.TAB)

zip_or_city = driver.find_element_by_id("zip_or_city")
zip_or_city.send_keys(Keys.TAB)

email1 = driver.find_element_by_id("email1")
email1.send_keys(Keys.TAB)

email2 = driver.find_element_by_id("email2")
email2.send_keys(Keys.TAB)


########TODO PUT THIS IN A LOOP
email_loop = True

while email_loop:
    # time.sleep(10)
    # email verification
    email_verification = driver.execute_script("return document.querySelectorAll('.okform-feedback')[5].innerHTML;")

    if email_verification == "This email is already in use.":
        email = raw_input("Enter another email")

        # input email (confirming)
        driver.execute_script("document.querySelector('#email1').value="+dumps(email))
        driver.execute_script("document.querySelector('#email2').value="+dumps(email))


    else:
        email_loop = False

    email1 = driver.find_element_by_id("email1")
    email1.send_keys(Keys.TAB)

    email2 = driver.find_element_by_id("email2")
    email2.send_keys(Keys.TAB)
##########END LOOP 


# click next button
driver.execute_script("document.querySelectorAll('button[type=button]')[2].click();")


################################ THIRD PAGE ##################################################################

# input username
driver.execute_script("document.querySelector('#screenname_input').value='adobsthecat';")

time.sleep(3)

#TAB 1 time
screenname_input = driver.find_element_by_id("screenname_input")
screenname_input.send_keys(Keys.TAB)

#TAB 2 time
screenname_input = driver.find_element_by_id("screenname_input")
screenname_input.send_keys(Keys.TAB)


##########TODO PUT THIS IN A LOOP
screenname_loop = True

while screenname_loop:

    # suggestions hidden

    screenname_verification = driver.execute_script("return document.querySelectorAll('#signup_email_typo_hoverbox, .label')[0].innerHTML;")
    print screenname_verification
    
    if "<div class=\"label\">(this gets filled by JS)</div><a href=\"#\" id=\"revert_typo\">Nope, change it back</a><div class=\"arrow\"></div>" == screenname_verification:
        screenname_loop = False
        print "FALSE"

    else:
        screenname = raw_input("Enter another screenname")
        driver.execute_script("document.querySelector('#screenname_input').value="+dumps(screenname))

        #TAB 1 time
        screenname_input = driver.find_element_by_id("screenname_input")
        screenname_input.send_keys(Keys.TAB)
        print "TRUE"
        
    #TAB 1 times
    screenname_input = driver.find_element_by_id("screenname_input")
    screenname_input.send_keys(Keys.TAB)
###########END LOOP

# input password REMEMBER MUST BE AT LEAST 5 CHARACTERS
driver.execute_script("document.querySelector('#password_input').value='ro1zzaa332';")

#TAB 1 times
password_input = driver.find_element_by_id("password_input")
password_input.send_keys(Keys.TAB)

##########TODO PUT THIS IN A LOOP

password_loop = True

while password_loop:
    
    password_verification = driver.execute_script("return document.querySelectorAll('.okform-feedback')[8].innerHTML;")
    
    if password_verification =="Password is too weak, choose again.":
        password = raw_input("Enter another password")
        driver.execute_script("document.querySelector('#password_input').value="+dumps(password))
    
    else:
        password_loop = False
    
    #TAB 1 times
    password_input = driver.find_element_by_id("password_input")
    password_input.send_keys(Keys.TAB)

###########END LOOP

# # sequence to click submit
# driver.execute_script("document.querySelectorAll('button[type=submit]')[0].click();")
# try:
#     driver.execute_script("document.querySelectorAll('button[type=submit]')[0].click();")
# except Exception as e:
#     print type(e)
# try:
#     driver.execute_script("document.querySelectorAll('button[type=submit]')[0].click();")
# except Exception as e:
#     print type(e)

# # printing positive results to the terminal
# current_url = driver.current_url;
# print current_url
# if current_url == "https://www.okcupid.com/onboarding/steps":
#     print "F YEAH BABY"

# display.stop()
