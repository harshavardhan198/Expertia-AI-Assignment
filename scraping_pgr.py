import requests
from bs4 import BeautifulSoup
from datetime import date
import re
import time
import logging
import json

start_time = time.time()
payload = {
          'Username': 'vinay@teml.net',
          'Password': 'vinayprasadlkq'
    }

header1 = {


"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}  
cookies = {'ci_session' : '5bf590ca47c301e50f1328280cc808ed18a60ca9'}
# Make a POST request to the login page with the login credentials
login_url = 'https://paganresearch.io/login'
session = requests.Session()
response = session.post(login_url, data=payload, cookies = cookies)


# Check if the login was successful
if response.status_code == 200:
    print('Login successful!')
    logging.warning('Login to the website succesful')
else:
    print('Login failed.')
    logging.warning("Not able to login to the website")

logging.warning('The links file is loaded')

with open('name_urls_pgr','r') as file:
    lines = [line.strip() for line in file]

logging.warning("Logfile list created")
logFile = []
links10000 = lines[50000:85001]
lead_details = []
start_time = time.time()
for url in links10000:
    logDetail = {}
    soup = None
    logging.warning("LogDetail object created")
    try:
        startOfGetRequest = time.time()
        response = session.get(str(url))
        logging.warning("Got a response from " + url)
        endOfGetRequest = time.time()
        logging.warning(f"----------time_taken_for_getting_response_from_{url}- {round(endOfGetRequest - startOfGetRequest,5)} seconds")

  # print(url)
        startOfParsingHtml = time.time()
        soup = BeautifulSoup(response.content, 'lxml')
        endOfParsingHtml = time.time()
        logging.warning(f"----------time_taken_for_parsing_html_from_{url}- {round(endOfParsingHtml - startOfParsingHtml,5)} seconds")
        logDetail['url'] = url
        logDetail['crawled'] = True
        logDetail['date'] = date.today().strftime("%d/%m/%Y")
        logDetail['message'] = "Begining to extract the lead details" 

    except Exception as e:
        print("Error occurred while processing URL:", url)
        print(f"Error: {str(e)}")
        logDetail['url'] = url
        logDetail['crawled'] = False
        logDetail['date'] = date.today().strftime("%d/%m/%Y")
        logDetail['message'] = str(e)
        logFile.append(logDetail)
            
    logging.warning("Soup object created")
    startOfCreatingJson = time.time()
    country = ''
    city = ''
    email = ''
    name = ''
    a = ''

    info_div = soup.find('div', class_='basic-infomration')
    logging.warning('Begining to scrape the elements')

    soup = BeautifulSoup(response.content, 'lxml')
    try:

        name = soup.find('h2', class_='person-name').text.strip()
        if name:
            logging.warning('name added in the leadDetails')
            logDetail['name'] = 'Name has been added'
        else:
            logging.warning('name not found')
            logDetail['name'] = 'Name is not available'
    except:
        name = ''
        logging.warning('name not found')
        logDetail['name'] = 'Name is not available'
    position = soup.find('h3', class_='person-deg').text.strip()
    if position:
        logging.warning('position added in the leadDetails')
        logDetail['position'] = 'Position has been added'
    else:
        logging.warning('position not found')
        logDetail['position' ] = 'Position of the person is not available'
    company =  soup.find('div', class_ = 'basic-infomration').find('a').text
    if company:
        logging.warning('company added in the leadDetails')
        logDetail['company'] = 'Company has been added'
    else:
        logging.warning('company not found')
        logDetail['company'] = 'Company is not available'

  # Extract country
    country_element = info_div.find('span', string=re.compile(r'Country\s*:.*', re.IGNORECASE))
    if country_element:
        country = country_element.find_next('strong').text.strip()
        logging.warning('country added in the leadDetails')
        logDetail['country'] = 'Country has been added'
    else:
        logging.warning('country not found')
        logDetail['country'] = 'Country is not available'
  # Extract city
    city_element = info_div.find('span', string=re.compile(r'City\s*:.*', re.IGNORECASE))
    if city_element:
        city = city_element.find_next('strong').text.strip()
        logging.warning('city added in the leadDetails')
        logDetail['city'] = 'City has been added'

    else:
        logging.warning('city not found')
        logDetail['city'] = 'City is not available'

  # Extract email
    a = info_div.find_all('li')[1].text
    if a:
        email = a.split(':')[1].strip()
        logging.warning('email added in the leadDetails')
        logDetail['email'] = 'Email has been added'
    else:
        logging.warning("email is not available" )
        logDetail['email'] = "Email address not found"



    lead_details.append({'url': url,
                          'name': name,
                          'company': company,
                          'position' : position,
                          'email' : email,
                          'city': city,
                          'country': country})
    logging.warning('All the details required for the url have been added in the leadDetails')
    endOfCreatingJson = time.time()
    logging.warning(f"----------time_taken_for_creating_json_ {round(endOfCreatingJson - startOfCreatingJson,5)} seconds")
    logFile.append(logDetail)

end_time =  time.time()
print('Total time taken:',end_time -start_time)

f = open('pgr50k-85k_19thmay.json','w',encoding = 'utf-8')
for details in lead_details:
        f.write(json.dumps(details))
        f.write('\n')
f.close()

out_file = open('logDetails50k-85k(new).json', "w")
logging.warning("logDetails JSON file created")

json.dump(logFile, out_file, indent = 6) 
logging.warning("LogFile added in JSON file")     
out_file.close()

logging.warning("Web scraping done")
end_time = time.time()

print(f"total time taken {end_time - start_time}")