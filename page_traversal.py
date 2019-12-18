#import packages
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient

#connecting to mongo client
client = MongoClient('mongodb+srv://Hinton:asdfghjk@mongoclusterint-jkb8r.mongodb.net/test?retryWrites=true&w=majority')

#Creating the database
db = client.reviewtest

#Accesing drivers of firefox
driver = webdriver.Firefox()

#Passing the link of the main hotel list page
driver.get('https://www.tripadvisor.in/Hotels-g60763-oa180-New_York_City_New_York-Hotels.html')
print(driver.title)

#Storing the main window handle
main_window = driver.current_window_handle

# Getting the hyperlinks of hotel names
res_buttons = driver.find_elements_by_class_name('property_title.prominent')

 

#Iterating through each hotel hyperlink
for i in range(len(res_buttons)):
 #clicking the resaturant hyperlink
 if res_buttons[i].is_displayed():
  driver.execute_script("arguments[0].click();",res_buttons[i])
  time.sleep(3)

  #Setting tab to new hotel
  driver.switch_to.window(driver.window_handles[1])

  #Expanding hidden reviews by clicking the (read more) button
  more_buttons = driver.find_elements_by_class_name("hotels-hotel-review-about-csr-Description__readMore--3rZ3t")
  
  if len(more_buttons)!=0:
   if more_buttons[0].is_displayed():
      driver.execute_script("arguments[0].click();", more_buttons[0])
      time.sleep(4)

  
  print(' ')
  print('Hotel name:',driver.title)
  print(' ')
  #Description scraping
  a = driver.find_element_by_class_name("cPQsENeY")
  rev = {'Description': a.text,
          #'Date of visit':DOV.text,
          #'Url extracted from':curl,


           }
  #Inserting into mongodb cloud  
  db.hotel_description.insert_one(rev)

  #closing tab and switching to main  
  driver.close()
  driver.switch_to.window(main_window)
  time.sleep(2)


print('finished updating')


