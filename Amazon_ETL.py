from bs4 import BeautifulSoup
import requests
import pandas as pd 
import numpy as np
import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine


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
		available = "NOT AVAILABLE"

	return available	


if __name__ == '__main__':
    load_dotenv()

    user_agent=os.getenv('USER_AGENT')
    HEADERS = ({'User-Agent':user_agent,'Accept-Language': 'en-US, en;q=0.5'})

    URL = "https://www.amazon.com/s?k=iphone+15+pro+max+case&crid=PF7JGHUOD8NI&sprefix=iphone%2Caps%2C529&ref=nb_sb_ss_pltr-xclick_7_6"
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

    amazon_df = pd.DataFrame.from_dict(d)
    #Replace the empty String with NaN in titile column
    amazon_df['title']= amazon_df['title'].replace('', np.nan)
    #Drop rows with NaN value in title column 
    amazon_df = amazon_df.dropna(subset=['title'])
    #store our data into csv file 
    amazon_df.to_csv("Amazon_data.csv", header=True, index=False)
    
    # establish connections to postgresql db
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT',5432)

    #conn_string = 'postgresql://db_user:db_password@db_host/db_port'
    conn_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    try:
        # Create SQLAlchemy engine and establish connection
        db = create_engine(conn_string)
        # Converting DataFrame to SQL
        amazon_df.to_sql('data', db, if_exists='append', index=False)
        print("Data inserted successfully.")

        """# Fetching all rows to verify insertion
        with db.connect() as conn:
            result = conn.execute('SELECT * FROM  data')
            for row in result:
                print(row)
"""
    except Exception as e:
        print(f"An error occurred: {e}")
    
   


