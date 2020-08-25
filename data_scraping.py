from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
from selenium.webdriver.common.action_chains import ActionChains
import os,sys
import shutil

iterator = 0
max_iterator = 200                      
create = 0

current_dir = os.getcwd()
current_dir = current_dir.replace('\\','/')
data_path = current_dir + '/' + 'datatest/'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome = r'D:\chrome\chromedriver.exe'
driver_web = webdriver.Chrome(chrome,options=chrome_options)
# driver_web = webdriver.Chrome(chrome)

try:
    os.makedirs(data_path)
except:
    pass

time.sleep(0.1)
cek = os.listdir(data_path)
try:
    if len (cek) == 0:
        pass
    else:
        for p in cek:
            os.remove(data_path+p)
except:
    print('Please close file')
    sys.exit()

now = datetime.now()

##test_data
d = now.strftime("%d/%m/%Y")
year =  d.split('/')[2]
month = d.split('/')[1]
day = d.split('/')[0]
##print(year + ' ' + month + ' ' + day)

while True:
    try:
        driver_web.get('https://www.cnnindonesia.com/indeks?date='+year+'/'+month+'/'+day)
        WebDriverWait(driver_web, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"container")))
        break
    except:
        print('Timeout')
        continue

while True:
    try:
        if iterator == max_iterator:
            break
        else:    
            filter_btn = driver_web.find_element_by_xpath('//*[@id="content"]/div/div[4]/div/div[2]/a').click()
            iterator += 1
            time.sleep(0.2)
            continue
    except:
        break    

while True:
    try:
        total = driver_web.find_element_by_xpath('//*[@id="content"]/div/div[4]/div/div[1]').find_elements_by_tag_name('a')
        for x in range (1,len(total)+1):
            train_dir = os.listdir(data_path)
            information = driver_web.find_element_by_xpath('//*[@id="content"]/div/div[4]/div/div[1]/article['+str(x)+']').find_element_by_class_name('title')
            cat = driver_web.find_element_by_xpath('//*[@id="content"]/div/div[4]/div/div[1]/article['+str(x)+']').find_element_by_class_name('kanal')
            if len(train_dir) == 0:
                with open (data_path+'test_data'+'.csv','w') as file:
                    file.write(information.text+'>'+cat.text+ '\n')
            else:
                with open (data_path+'test_data'+'.csv','a') as file:
                    file.write(information.text+'>'+cat.text+ '\n')
                    
            print('Progress: ' + str(x/len(total)*100) + '%')

        break
    
    except:
      print('ERROR_ARTICLE')
      continue

print('\nTest data complete')
driver_web.service.stop()
