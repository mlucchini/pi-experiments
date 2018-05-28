import time

from selenium import webdriver
from pyvirtualdisplay import Display


display = Display(visible=0, size=(800, 600))
display.start()
print('Display started')

browser = webdriver.Firefox()
print('Browser started')

browser.get('https://purrli.com')
print('Web page loaded')

vol_minus = browser.find_element_by_css_selector('body > div.tile1 > div.ctrSection > img:nth-child(1)')
vol_plus = browser.find_element_by_css_selector('body > div.tile1 > div.ctrSection > img:nth-child(3)')

user_input = None

while user_input is not 'q':
    user_input = input('Volume (+) or (-). Or quit (q)\n')
    vol_plus.click() if user_input == '+' else vol_minus.click()

time.sleep(1000)

browser.quit()
display.stop()
