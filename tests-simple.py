from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:5000/map')

assert browser.title == 'Adjective Map'

