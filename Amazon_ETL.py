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

#Function to extract Description
def get_description(soup): 

    try : 
        description =soup.find ("ul", attrs={'class':'a-unordered-list a-vertical a-spacing-mini'}).text.strip()
          
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


if __name__ == '__main__':
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    URL = "https://www.amazon.com/s?k=laptop&crid=73UWUS1S13Y9&sprefix=laptop%2Caps%2C247&ref=nb_sb_noss_1"
    page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')


    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
        href = link.get('href')
        if href and href.startswith('/'):
            links_list.append(href)

    # dic of list to store our data
    d = {"title": [], "price": [], "rating": [], "count_review": [], "availability": []}
    # to see how many links we've
    print(f"Total links found: {len(links_list)}")
     
    # Loop for extracting product details from each link
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['count_review'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))

    # Store our data into csv file   
    amazon_df = pd.DataFrame.from_dict(d)
    #Replace the empty String with NaN in titile column
    amazon_df['title']= amazon_df['title'].replace('', np.nan)
    #Drop rows with NaN value in title column 
    amazon_df = amazon_df.dropna(subset=['title'])
    # hnaya dart 2 dyal file jarabthom 
    amazon_df.to_csv("Amazon_data2.csv", header=True, index=False)