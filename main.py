import undetected_chromedriver as uc
uc.install()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import os, sys
import time,requests
from bs4 import BeautifulSoup
from watson import audioToText

delayTime = 2
audioToTextDelay = 10
filename = 'audio.mp3'
byPassUrl = 'https://www.google.com/recaptcha/api2/demo'
googleIBMLink = 'https://speech-to-text-demo.ng.bluemix.net/'

option = webdriver.ChromeOptions()
option.add_argument('--disable-notifications')
option.add_argument("--mute-audio")

def saveFile(content,filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)

driver = webdriver.Chrome(options=option)
driver.get(byPassUrl)

googleClass = driver.find_elements_by_class_name('g-recaptcha')[0]
outeriframe = googleClass.find_element_by_tag_name('iframe')
outeriframe.click()

allIframesLen = driver.find_elements_by_tag_name('iframe')
audioBtnFound = False
audioBtnIndex = -1

for index in range(len(allIframesLen)):
    driver.switch_to.default_content()
    iframe = driver.find_elements_by_tag_name('iframe')[index]
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(delayTime)
    try:
        audioBtn = driver.find_element_by_id('recaptcha-audio-button') or driver.find_element_by_id('recaptcha-anchor')
        audioBtn.click()
        audioBtnFound = True
        audioBtnIndex = index
        break
    except Exception as e:
        pass

if audioBtnFound:
    try:
        while True:
            try:
                href = driver.find_element_by_id('audio-source').get_attribute('src')
            except:
                raise Exception("Unable to find audio source")
            response = requests.get(href, stream=True)
            saveFile(response,filename)
            response = audioToText(os.getcwd() + '/' + filename)

            driver.switch_to.default_content()
            iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
            driver.switch_to.frame(iframe)

            inputbtn = driver.find_element_by_id('audio-response')
            inputbtn.send_keys(response)
            inputbtn.send_keys(Keys.ENTER)

            time.sleep(2)
            errorMsg = driver.find_element_by_class_name('rc-audiochallenge-error-message')

            if errorMsg.value_of_css_property('display') == 'none':
                print("\033[32m"+"Success"+"\033[0m")
            else:
                raise Exception("Unable to solve captcha")
            break
    except Exception as e:
        print(e)
        print("\033[31m"+"Failed"+"\033[0m")
else:
    print('Button not found. This should not happen.')

driver.close()