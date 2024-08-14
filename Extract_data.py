from bs4 import BeautifulSoup
import requests


# Step 1: Sending a HTTP request to a URL
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

url = "https://www.amazon.com/Sony-PlayStation-Pro-1TB-Console-4/dp/B07K14XKZH/"
page = requests.get(url , headers=HEADERS)

soup = BeautifulSoup(page.content, 'lxml')

# fuction to extract product's title 

def get_title(soup):
    try:

        title = soup.find("span" ,attrs = {"id" : 'productTitle'}) 

        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""
    return title_string
        

# Function to extract Product's price 
def get_price(soup):
    try:
        
        price_div = soup.find("div", class_="a-section a-spacing-none aok-align-center aok-relative")
        
        # Find the relevant spans and extract their text
        price_symbol = price_div.find("span", class_="a-price-symbol").text.strip()
        price_whole = price_div.find("span", class_="a-price-whole").text.strip()
        price_decimal = price_div.find("span", class_="a-price-decimal").text.strip()
        price_fraction = price_div.find("span", class_="a-price-fraction").text.strip()
        
        # Concatenate to get the full price
        price = f"{price_symbol}{price_whole}{price_decimal}{price_fraction}"
        
    except AttributeError:
        price = ""  # Fallback in case of an error

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

# Function calls to display all necessary product information
print("the data is ")
print("Product Title =", get_title(soup))
print("Product Price =", get_price(soup))
print("Product Rating =", get_rating(soup))
print("Number of Product Reviews =", get_review_count(soup))
print("Product's description is : ", get_description(soup))
print("Availability =", get_availability(soup))
#first commit
