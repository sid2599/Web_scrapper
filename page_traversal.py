#import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient

#connecting to mongo client
client = MongoClient('mongodb+srv://Hinton:asdfghjk42@mongoclusterint-jkb8r.mongodb.net/test?retryWrites=true&w=majority')

#Creating the database
db = client.reviewtest

#Accesing drivers of firefox
driver = webdriver.Firefox()
#driver.get('https://www.tripadvisor.in/Restaurants-g32655-Los_Angeles_California.html')

driver.get('https://www.tripadvisor.in/Hotels-g60763-oa180-New_York_City_New_York-Hotels.html')
print(driver.title)
main_window = driver.current_window_handle

#Restaurant hyperlinks
# restuarnt res_buttons = driver.find_elements_by_class_name('restaurants-list-ListCell__restaurantName--2aSdo')

res_buttons = driver.find_elements_by_class_name('property_title.prominent')

#res_buttons = res_buttons[2:len(res_buttons)]
#print(len(res_buttons)) 


for i in range(len(res_buttons)):
 #clicking the resaturant hyperlink
 if res_buttons[i].is_displayed():
  driver.execute_script("arguments[0].click();",res_buttons[i])
  time.sleep(3)

  #switching tab to new restaurant
  driver.switch_to.window(driver.window_handles[1])

  #Expanding hidden reviews
  #more_buttons = driver.find_elements_by_class_name('taLnk.ulBlueLinks')
  more_buttons = driver.find_elements_by_class_name("hotels-hotel-review-about-csr-Description__readMore--3rZ3t")
  #print(len(more_buttons))
  if len(more_buttons)!=0:
   if more_buttons[0].is_displayed():
      driver.execute_script("arguments[0].click();", more_buttons[0])
      time.sleep(4)

  #time.sleep(3)
  print(' ')
  print('Hotel name:',driver.title)
  print(' ')
  #test for review scraping
  
  #a = driver.find_elements_by_class_name('partial_entry')
  #DOV = driver.find_element_by_class_name("prw_rup.prw_reviews_stay_date_hsx")
  #curl = driver.current_url
  a = driver.find_element_by_class_name("cPQsENeY")
  #for multiple elements(chnage element to elements) print(len(a))
  #for i in a(a.text to i.text):
  rev = {'Description': a.text,
          #'Date of visit':DOV.text,
          #'Url extracted from':curl,


           }
  
  db.hotel_description.insert_one(rev)

  #closing tab and switching to main  
  driver.close()
  driver.switch_to.window(main_window)
  time.sleep(2)

#print(driver.title)
print('finished updating')


