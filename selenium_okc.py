from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
from pyvirtualdisplay import Display
from json import dumps

# input password REMEMBER MUST BE AT LEAST 5 CHARACTERS
# input username REMEMBER MUST BE LESS THAN 16 CHARACTERS

# ensure Firefox page doesn't open
def create_new_user(orientation, gender, birthmonth, birthday, birthyear, zip, email, screenname, password):
    display = Display(visible=0, size=(800, 600))
    display.start()

    driver = webdriver.Firefox()
    driver.get("https://www.okcupid.com/")
    # time.sleep(10)

    # select orientation
    driver.execute_script("document.querySelector('#orientation_container').innerHTML = '<input type\"hidden\" id=\"orientation\" name=\"orientation\" data-default=\"1\" value="+dumps(orientation)+">';")

    # select gender
    driver.execute_script("document.querySelector('#gender_container').innerHTML = '<input type=\"hidden\" id=\"gender\" name=\"gender\" data-default=\"2\" value="+dumps(gender)+">';")

    # click green next button
    (driver.find_element_by_class_name('next_page')).click()

    ################################ SECOND PAGE ##################################################################

    # input birthmonth
    driver.execute_script("document.querySelector('#birthmonth').value="+dumps(birthmonth))

    # input birthday
    driver.execute_script("document.querySelector('#birthday').value="+dumps(birthday))

    # input birthyear
    driver.execute_script("document.querySelector('#birthyear').value="+dumps(birthyear))

    # input zip
    driver.execute_script("document.querySelector('#zip_or_city').value="+dumps(zip))

    # input email
    driver.execute_script("document.querySelector('#email1').value="+dumps(email))

    # input email (confirming)
    driver.execute_script("document.querySelector('#email2').value="+dumps(email))

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

    ########### start email verification loop
    email_loop = True

    while email_loop:
        email_verification = driver.execute_script("return document.querySelectorAll('.okform-feedback')[5].innerHTML;")

        if email_verification == "This email is already in use.":
            return "This email is already in use."

            # input email (confirming)
            driver.execute_script("document.querySelector('#email1').value="+dumps(email))
            driver.execute_script("document.querySelector('#email2').value="+dumps(email))


        else:
            email_loop = False

        email1 = driver.find_element_by_id("email1")
        email1.send_keys(Keys.TAB)

        email2 = driver.find_element_by_id("email2")
        email2.send_keys(Keys.TAB)
    ########## END LOOP 


    # click next button
    driver.execute_script("document.querySelectorAll('button[type=button]')[2].click();")


    ################################ THIRD PAGE ##################################################################

    # input username REMEMBER MUST BE LESS THAN 16 CHARACTERS
    driver.execute_script("document.querySelector('#screenname_input').value="+dumps(screenname))

    time.sleep(3)

    #TAB 1 time
    screenname_input = driver.find_element_by_id("screenname_input")
    screenname_input.send_keys(Keys.TAB)

    #TAB 2 time
    screenname_input = driver.find_element_by_id("screenname_input")
    screenname_input.send_keys(Keys.TAB)


    ########## start screenname loop
    screenname_loop = True

    while screenname_loop:

        # suggestions hidden

        screenname_verification = driver.execute_script('return document.querySelector("#screenname_inputContainer").innerHTML')
        
        if "Available names:" in screenname_verification:
            return "Screenname already in use."
            # screenname = raw_input("Screenname already in use")
            # driver.execute_script("document.querySelector('#screenname_input').value="+dumps(screenname))

            #TAB 1 time
            screenname_input = driver.find_element_by_id("screenname_input")
            screenname_input.send_keys(Keys.TAB)

            #TAB 2 time
            screenname_input = driver.find_element_by_id("screenname_input")
            screenname_input.send_keys(Keys.TAB) 


        else:
            screenname_loop = False
            
            
        #TAB 1 times
        screenname_input = driver.find_element_by_id("screenname_input")
        screenname_input.send_keys(Keys.TAB)
    ###########END LOOP

    # input password REMEMBER MUST BE AT LEAST 5 CHARACTERS
    driver.execute_script("document.querySelector('#password_input').value="+dumps(password))

    #TAB 1 times
    password_input = driver.find_element_by_id("password_input")
    password_input.send_keys(Keys.TAB)

    ########## start password loop
    password_loop = True

    while password_loop:
        
        password_verification = driver.execute_script("return document.querySelectorAll('.okform-feedback')[8].innerHTML;")
        
        if password_verification =="Password is too weak, choose again.":
            # password = raw_input("Enter another password")
            return "Password is too weak, choose again."
            # driver.execute_script("document.querySelector('#password_input').value="+dumps(password))
        
        else:
            password_loop = False
        
        #TAB 1 times
        password_input = driver.find_element_by_id("password_input")
        password_input.send_keys(Keys.TAB)
    ###########END LOOP


    # sequence to click submit
    driver.execute_script("document.querySelectorAll('button[type=submit]')[0].click();")
    try:
        driver.execute_script("document.querySelectorAll('button[type=submit]')[0].click();")
    except Exception as e:
        print type(e)
    try:
        driver.execute_script("document.querySelectorAll('button[type=submit]')[0].click();")
    except Exception as e:
        print type(e)

    display.stop()
    return "success"
    # driver.current_url
    # printing positive results to the terminal
    # print current_url
    # if current_url == "https://www.okcupid.com/onboarding/steps":
    #     print "F YEAH BABY"

