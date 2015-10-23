from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()


driver = webdriver.Firefox()
driver.get("https://www.okcupid.com/")
# time.sleep(10)

# # not actually selecting orientation
# driver.execute_script("document.querySelector('#orientation_dropdown').click();");
# driver.execute_script("document.querySelector('#orientation_dropdown').selectedIndex='2';")


# # not actually selecting gender
# driver.execute_script("document.querySelector('#gender_dropdown').click();");
# driver.execute_script("document.querySelector('#gender_dropdown').selectedIndex='1';")

# ADD DRIVER EXECUTE
document.querySelector('#orientation_container').innerHTML = '<input type="hidden" id="orientation" name="orientation" value="3" data-default="1">'

document.querySelector('#gender_container').innerHTML = '<input type="hidden" id="gender" name="gender" value="1" data-default="2">'

# click green next button
(driver.find_element_by_class_name('next_page')).click()

# input birthmonth
driver.execute_script("document.querySelector('#birthmonth').value='02';")

# input birthday
driver.execute_script("document.querySelector('#birthday').value='04';")

# input birthyear
driver.execute_script("document.querySelector('#birthyear').value='1990';")

# input zip
driver.execute_script("document.querySelector('#zip_or_city').value='94108';")

# input email
driver.execute_script("document.querySelector('#email1').value='alexandradobkin@hotmail.com';")

# input email (confirming)
driver.execute_script("document.querySelector('#email2').value='alexandradobkin@hotmail.com';")

# clicking outside of input fields
driver.execute_script("document.querySelector('#form_container').click();")


time.sleep(10)
# click next button
driver.execute_script("document.querySelectorAll('button[type=button]')[2].click();")
try:
    driver.execute_script("document.querySelectorAll('button[type=button]')[2].click();")
except Exception as e:
    print type(e)
try:
    driver.execute_script("document.querySelectorAll('button[type=button]')[2].click();")
except Exception as e:
    print type(e)
# input username
driver.execute_script("document.querySelector('#screenname_input').value='ro1a1340';")

# input password
driver.execute_script("document.querySelector('#password_input').value='ro1zzaa332';")

# click outside of username/signup in div
driver.execute_script("document.querySelector('#signup').click();")

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

# printing positive results to the terminal
current_url = driver.current_url;
print current_url
if current_url == "https://www.okcupid.com/onboarding/steps":
    print "F YEAH BABY"

display.stop()
