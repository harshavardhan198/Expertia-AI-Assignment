#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import random
import pandas as pd 
from parsel import Selector
from time import sleep
# ------------- # 

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
opts = Options()


driver = webdriver.Chrome(executable_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

def validate_field(field):
    if field:
        pass
    else:
        field = 'No results'
    return field


driver.get('https://www.linkedin.com')

username = driver.find_element(By.ID, 'session_key')

username.send_keys('************************')

sleep(0.5)
password =  driver.find_element(By.ID, 'session_password')

password.send_keys('***************')

sleep(0.5)

sign_in_button = driver.find_element(By.XPATH, '//*[@type ="submit"]')

sign_in_button.click()

sleep(15)


Jobdata = []
lnks = []

for x in range(0,100,5):

    driver.get(f'https://www.google.com/search?q=site%3Alinkedin.com%2Fin%2F+AND+%22Developer%22+AND+%22London%22&ei=2SUvZI2WKrWPseMPnuyp4A0&ved=0ahUKEwjN5rPahpb-AhW1R2wGHR52CtwQ4dUDCA8&uact=5&oq=site%3Alinkedin.com%2Fin%2F+AND+%22Developer%22+AND+%22London%22&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQA0oECEEYAVDpClivZ2Cza2gBcAB4AIABWIgB8gaSAQIxM5gBAKABAcABAQ&sclient=gws-wiz-serp{x}')
    time.sleep(random.uniform(2.5,4.9))
    linkedin_urls = [my_elem.get_attribute("href") for my_elem in WebDriverWait(driver,20).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class = 'yuRUbf']/a[@href]")))]
    lnks.append(linkedin_urls)          
    
for x in lnks:
    for i in x:
        driver.get(i)
        time.sleep(random.uniform(2.5,4.9))
        
        sel = Selector(text = driver.page_source)
        
        name = sel.xpath('//*[starts-with(@class, "text-heading-xlarge inline t-24 v-align-middle break-words")]/text()').extract_first()
        
        
        if name:
            
            name = name.strip()
            
            
        job_title = sel.xpath('//*[starts-with(@class, "text-body-medium break-words")]/text()').extract_first()
        
        if job_title:
            job_title = job_title.strip()
            
        try:
            company = driver.find_element(By.XPATH, 'ul[@class = "pv-text-details__right-panel"]').text
            
        except:
            company = 'None'
            
        if company:
            company = company.strip()
            
        location = sel.xpath('//*[starts-with(@class, "text-body-small inline t-black--light break-words")]/text()').extract_first()
        
        
            
        if location:
            location = location.strip()
            
        college = sel.xpath('//*[starts-with(@class, "pv-top-card-v2-section__entity-name pv-top-card-v2-section__school-name")]/text()').extract_first()

        if college:
            college = college.strip()
        
    




        linkedin_url = driver.current_url

            
        name = validate_field(name)
        job_title = validate_field(job_title)
        company = validate_field(company)
        college = validate_field(college)
        location = validate_field(location)
        linkedin_url = validate_field(linkedin_url)
        
        
        print('\n')
        print('Name: ' + name)
        print('Job Title: ' + job_title)
        print('Company: ' + company)
        print('Location: ' + location)
        print('URL: ' + linkedin_url)
        print('\n')

        
        data = {
                 'Name ' :  name,
                 'Job Title' : job_title,
                 'Company' : company,
                'Location' : location,
                'URL' : linkedin_url
               }
            
        Jobdata.append(data)

        
import json
json_string = json.dumps(Jobdata)

with open('Jobdata.json', 'w') as f:
    f.write(json_string)
    
    
driver.quit()
                   

                

