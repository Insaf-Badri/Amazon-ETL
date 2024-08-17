from bs4 import BeautifulSoup
import requests
import pandas as pd 
import numpy as np


# Fuction to extract product's title 
def get_title(soup):
    try:
		#Search Tag
        title = soup.find("span" ,attrs = {"id" : 'productTitle'}) 

        # Inner NavigatableString Object(the text value)
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string
        

# Function to extract Product's price 
def get_price(soup):
    try:
        
        price= soup.find("span", class_="a-offscreen").string.strip()

    except AttributeError:
        price = "" 
 
    return price

#Function to extract Dicription
def get_description(soup): 

    try : 
        description =soup.find ( "ul", attrs={'class':'a-unordered-list a-vertical a-spacing-mini'}).text.strip()
          
    except AttributeError : 

        description = "NO DESCRIPTION "	

    return description
    
  
# Function to extract Product Rating
def get_rating(soup):

	try:
		rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
		
	except AttributeError:
		
		try:
			rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
		except:
			rating = ""	

	return rating

# Function to extract review_count
def get_review_count(soup):
	try:
		review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
		
	except AttributeError:
		review_count = ""	

	return review_count

def get_availability(soup):
	try:
		available = soup.find("div", attrs={'id':'availability'})
		available = available.find("span").string.strip()

	except AttributeError:
		available = ""	

	return available	


HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

url = "https://www.amazon.com/Apple-iPhone-13-Mini-Starlight/dp/B09LKYXHK5/ref=sr_1_8?crid=3UROYK1HVSI20&dib=eyJ2IjoiMSJ9.Ln-hU6FflqpQLC0k4dwhS57oJiCuXnXZWioAtc01zy9U7Gkt5ptMbX29-x-uLsLBiqFm9KIBSEuf8Tvk61MOJYc1kcA4rQh0J4ZAonHsUhAL5w-Y0P7V5lJARVSpzJNGqif4AP4R6-qmduPlDQnt_4-LQJHh2xUchWRpsZ526szytfugo2i2VKdYALRyG6oNWECHwAVvc1tfe0ZquMABi0Q3tBYhIkJhPRPsVEp7EpY.ci1qcipmonPoyZCfp4Ix7-mj89jO0SRxc4a9_tmHkeU&dib_tag=se&keywords=iphone&qid=1723844024&sprefix=iphone%2Caps%2C249&sr=8-8&th=1"
page = requests.get(url , headers=HEADERS)
soup = BeautifulSoup(page.content, 'lxml')

#Test one Product
""""""
print("Product Title =", get_title(soup))
print("Product Price =", get_price(soup))
print("Product Rating =", get_rating(soup))
print("Number of Product Reviews =", get_review_count(soup))
print("Availability =", get_availability(soup))
print("Product Description = " , get_description(soup))
""""""


# Fetch links as List of Tag Objects
links = soup.find_all("a", attrs={'class':'a-link-normal'})

links_list = []

# Loop for extracting links from Tag Objects
for link in links:
    href = link.get('href')
    if href and href.startswith('/'):
    	links_list.append(href)

# Loop for extracting product details from each link 
for link in links_list:

	new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
	new_soup = BeautifulSoup(new_webpage.content, "html.parser")

	# Function calls to display all necessary product information
	
	print("Product Title =", get_title(new_soup))
	print("Product Price =", get_price(new_soup))
	print("Product Rating =", get_rating(new_soup))
	print("Number of Product Reviews =", get_review_count(new_soup))
	print("Availability =", get_availability(new_soup))
	print("Product Description = " , get_description(new_soup))		
	
	