import re
import logging
import requests
import json
import time 
import random
from random import randint
from datetime import date
from bs4 import BeautifulSoup

# time.sleep(250)
start_time = time.time()

# We are adding the headers to make request as a normal browser rather than a bot
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }

header1 = {


"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}  

header2 = {

    "User-Agent":    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
      }

header3 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

#the decode email function is used decrypt the encrypted email scraped from the website
def decodeEmail(e):
    de = ""
    k = int(e[:2], 16)

    for i in range(2, len(e)-1, 2):
        de += chr(int(e[i:i+2], 16)^k)
    return de


company_details = []

logging.warning("companyDetails object created")
# logDetail = {}
# logging.warning("LogDetail object created")

base_url = 'https://ae.bizdirlib.com/node/'

# index = 1
logging.warning("Counter variable created")
counter = 550000

logging.warning("Logfile list created")
logFile = []



while counter < 575001 :
    startOfProcess = time.time()
    url = base_url + str(counter)
    startOfGetRequest = time.time()
    logDetail = {}
    logging.warning("LogDetail object created")

    try:

        
        response = requests.get(url, headers=header1)
        logging.warning("Got a response from " + url)
        endOfGetRequest = time.time()
        logging.warning(f"----------time_taken_for_getting_response_from_{url}-{counter} {round(endOfGetRequest - startOfGetRequest,5)} seconds")

        startOfParsingHtml = time.time()
        soup = BeautifulSoup(response.content, 'lxml')
        endOfParsingHtml = time.time()
        logging.warning(f"----------time_taken_for_parsing_html_from_{url}-{counter} {round(endOfParsingHtml - startOfParsingHtml,5)} seconds")
        logDetail['url'] = url
        logDetail['crawled'] = True
        logDetail['date'] = date.today().strftime("%d/%m/%Y")
        logDetail['message'] = "Begining to extract the company details"
        # company_name = soup.find('h1', class_ = 'title')
    # print(soup)

    except Exception as exc:
        print(f"Error: {str(exc)}")
        logDetail['url'] = url
        logDetail['crawled'] = False
        logDetail['date'] = date.today().strftime("%d/%m/%Y")
        logDetail['message'] = str(exc)
        logFile.append(logDetail)
            
    logging.warning("Soup object created")
    startOfCreatingJson = time.time()

    startOfFindingCompanyName = time.time()
    company_name = soup.find('h1', class_ = 'title')
# print(company_name.text.title())
    if company_name:
        cn = company_name.text.title().strip()
        logging.warning("companyName added in companyDetails " + str(counter))
        logDetail['companyName'] = "Company Name has been added"
    else:
        cn = ''
        logging.warning("Blocked while crawling the companyName" + str(counter))
        logDetail['companyName'] = "Company Name not found"

    endOfFindingCompanyName = time.time()
    logging.warning(f"----------time_taken_for_finding_company_name_{counter} {round(endOfFindingCompanyName - startOfFindingCompanyName,5)} seconds")
    
    startOfFindingLocation = time.time()
    country  = soup.find('span', {"itemprop": "location"})
    if country:
        cntry = country.text.title()
        logging.warning("location added in companyDetails " + str(counter))
        logDetail['location'] = "Location has been added"
    else:
        cntry = ''
        logging.warning("location is not available" + str(counter))
        logDetail['location'] = "Location not found"
    endOfFindingLocation = time.time()
    logging.warning(f"----------time_taken_for_finding_location_{counter} {round(endOfFindingLocation - startOfFindingLocation,5)} seconds")

    startOfFindingPhoneNumber = time.time()
    phone = soup.find('span', {"itemprop": "telephone"})
    if phone:
        phn = phone.text.replace(" ", "").split(',')[0]
        logging.warning("phoneNumber added in companyDetails " + str(counter))
        logDetail['phoneNumber'] = "Phone Number has been added"
    else:
        phn = ''
        logging.warning(" phoneNumber is not available" + str(counter))
        logDetail['phoneNumber'] = "Phone Number not found"
    endOfFindingPhoneNumber = time.time()
    logging.warning(f"----------time_taken_for_finding_phone_number_{counter} {round(endOfFindingPhoneNumber - startOfFindingPhoneNumber,5)} seconds")

    startOfFindingContactPerson = time.time()
    contact = soup.find('span', {"itemprop": "contactPoint"})
    if contact:
        cp = (contact.text.split(',')[0]).title()
        logging.warning("contactPoint added in companyDetails " + str(counter))
        logDetail['contactPoint'] = "Contact point has been added"
    else:
        cp = ''
        logging.warning("contactPoint not available" + str(counter))
        logDetail['contactPoint'] = "Contact point not found"
    endOfFindingContactPerson = time.time()
    logging.warning(f"----------time_taken_for_finding_phone_number_{counter} {round(endOfFindingContactPerson - startOfFindingContactPerson,5)} seconds")

    startOfFindingEmail = time.time()
    mail = soup.find('a', {'itemprop':"email"})
    if mail is not None:
        mail_str = str(mail)
        encoded_str = re.findall('data-cfemail="(.+?)"', mail_str)
        if encoded_str:
            ml = decodeEmail(encoded_str[0])
            logging.warning("email added in companyDetails " + str(counter))
            logDetail['email'] = "Email address has been added"
        else:
            ml = ''
            logging.warning("email is not available" + str(counter))
            logDetail['email'] = "Email address not found"
    else:
        ml = ''
        logging.warning("email is not available" + str(counter))
        logDetail['email'] = "Email address not found"

    endOfFindingEmail = time.time()
    logging.warning(f"----------time_taken_for_finding_email_{counter} {round(endOfFindingEmail - startOfFindingEmail,5)} seconds")

    startOfFindingYear = time.time()
    year = soup.find('span', {"itemprop": "foundingDate"})
    if year:
        yr = year.text
        logging.warning("establishedYear added in companyDetails " + str(counter))
        logDetail['establishedYear'] = "Established Year has been added"
    else:
        yr = ''
        logging.warning("establishedYear is not available" + str(counter))
        logDetail['establishedYear'] = "Established Year not found"
    endOfFindingYear = time.time()
    logging.warning(f"----------time_taken_for_finding_established_year_{counter} {round(endOfFindingYear - startOfFindingYear,5)} seconds")

    startOfFindingIndustry = time.time()
    try:
        ind = ""           
        industry_section = soup.find('div', {'class': 'content clearfix'}).find_all('li')
        
        if industry_section:
            for item in industry_section:
                if "Industry:" in item.text:
                    industry = item.text.replace("Industry:", "").strip()
                    ind = industry.title()
                    break
                    
            logging.warning("industry added in companyDetails " + str(counter))
            logDetail['industry'] = "Industry has been added"
    except AttributeError:
        industry_section = None
        logging.warning("industry is not available" + str(counter))
        logDetail['industry'] = "Industry not found"
    endOfFindingIndustry = time.time()
    logging.warning(f"----------time_taken_for_finding_industry_{counter} {round(endOfFindingIndustry - startOfFindingIndustry,5)} seconds")


    


    company_details.append({"urlId":counter,"url" : url,
                             "companyName" : cn,
                             "location" : cntry,
                            "contactNumber" : phn,
                            "contactPerson" : cp,
                            "email" :ml,
                            "establishedYear": yr,
                            "industry" : ind,
                            "dateCrawled" : str(date.today())})
    logging.warning("All the details for the url have been added in the companyDetails" +str(counter))
    endOfCreatingJson = time.time()
    logging.warning(f"----------time_taken_for_creating_json_{counter} {round(endOfCreatingJson - startOfCreatingJson,5)} seconds")

    endOfProcess = time.time()

    # if counter % 500 == 0:
    #     time.sleep(300)
    #     logging.warning("The requests have exceeded 500, adding pausing for 10 seconds")

    # # elif counter > 700:
        
    startOfSleepTime = time.time()
    time.sleep(0.3)
    endOfSleepTime = time.time()
    logging.warning(f"----------time_taken_to_sleep_before the next_counter {round(endOfSleepTime - startOfSleepTime,5)} seconds")

    logging.warning(f"----------total_time_taken_for__{counter} {round(endOfProcess - startOfProcess,5)} seconds")
    logging.warning("-----------------------------------------------------------------------------------------------------")
    logging.warning("-----------------------------------------------------------------------------------------------------")
    logging.warning("Counter "+ str(counter) ) 

    # if counter > 700:
    #     time.sleep(10)
    #     break
    
    logFile.append(logDetail)
    counter = counter + 1

# print(company_details)


f = open('dcd550k-575k_13thmay.json','w',encoding = 'utf-8')
for details in company_details:
        f.write(json.dumps(details))
        f.write('\n')
f.close()

out_file = open('logDetails550k-575k(new).json', "w")
logging.warning("logDetails JSON file created")

json.dump(logFile, out_file, indent = 6) 
logging.warning("LogFile added in JSON file")     
out_file.close()

logging.warning("Web scraping done")
end_time = time.time()

print(f"total time taken {end_time - start_time}")





     

# with open("company_details7.json", "w") as f:
#     json.dump(company_details, f)


    
# company_details = {}

    # company_details["Company Name"] = cn
    # company_details["Location"] = cntry
    # company_details["Contact Number"] = phn
    # company_details["Contact Person"] = cp
    # company_details["Email"] = ml
    # company_details["Industry"] = ind

# print(company_details)






# import requests
# import re
# from bs4 import BeautifulSoup
# url = 'https://ae.bizdirlib.com/node/1'
# page = requests.get(url, headers = headers)
# print(page.text)
# # soup = BeautifulSoup(page.content, 'lxml')
# # print(page.content)
# # company_name = soup.find('h1', class_ = 'title')
# # print(company_name)
# # soup.find('h1', id='company-name')




# import requests

# url = "https://ae.bizdirlib.com/node/4"

# payload = {}
# headers = {}

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

# import requests

# Set the URL to make a request to
# url = 'https://ae.bizdirlib.com/node/'

# Set the headers to be sent with the request
# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
#     }

# Make the GET request with headers
# response = requests.get(url, headers=headers)

# Print the response content
# print(response)
# print(response.content)
# soup = BeautifulSoup(response.content, 'lxml')
# # print(page.content)
# company_name = soup.find('h1', class_ = 'title')
# print(company_name)
# company_name_span = soup.find('href', itemprop='email')
# company_name = company_name_span

# print(company_name)

# artist_name_list = soup.find(class_='content clearfix')
# artist_name_list_items = artist_name_list.find('a', {'itemprop':"email"})
# # print(artist_name_list_items)
# print(type(str(artist_name_list_items)))
# input_string = str(artist_name_list_items)
# encoded_str = re.findall('data-cfemail="(.+?)"', input_string)[0]
# print(encoded_str)
# year = soup.find('span', {"itemprop": "foundingDate"})
# print(year.text)
# country  = soup.find('span', {"itemprop": "location"})
# print((country.text.split(',')[0]).title())

   
# # Find the index of the encoded number
# start_index = artist_name_list_items.find('data-cfemail="') + len('data-cfemail="')
# end_index = artist_name_list_items.find('"', start_index)

# # Extract the encoded number using slicing
# encoded_number = artist_name_list_items[start_index:end_index]

# # Print the encoded number
# print(encoded_number)
# print(artist_name_list_items)

# Create for loop to print out all artists' names
# for artist_name in artist_name_list_items:
#     print(artist_name.prettify())




# table = soup.find_all('li')
# for i in table:
#   get_td = i.find_all('span')
#   for j in get_td:
#     get_ = j.find('a')['href'].strip()
#     print(get_)

# # for i in table:
# #   get_td = i.find_all('td')
# #   for j in get_td:
# #     get_ = j.find('a')['href'].strip().split('/')[-2]
# #     link = "{}/{}".format(_baseurl_, get_)
# #     print(link)

# company_info_section = soup.find('div', {'class': 'content clearfix'})

# info_list_items = company_info_section.find_all('li')

# # Extract the information from each list item
# for item in info_list_items:
#     # Extract the label of the information
#     # label = item.find('span', {'class': 'field-label'})
#     # label_text = label.text.strip()

#     # Extract the content of the information
#     content = item.find('span', {'itemprop': 'name'})
#     content_text = content.text.strip()

#     print( content_text)
# # This code should print the label and content of each piece of company information. Note that you may need to adjust the CSS selector or attributes in soup.find depending on the specific structure of the website you are scraping.






