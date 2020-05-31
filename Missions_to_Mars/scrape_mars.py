# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
# Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests
import os


# %%
executable_path = {'executable_path': './chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
mars_nasa_url = 'https://mars.nasa.gov/news/'
browser.visit(mars_nasa_url)

html=browser.html
soup = bs(html, 'html.parser')


# %%
# ```python
# Example:
# news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
news_t = soup.find_all('div', class_='content_title')
print(news_t)


# %%
# Iterate through all pages
for x in range(1):
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # Retrieve all elements that contain book information
    titles = soup.find_all('div', class_='content_title')
    soup.find_next('href')

    # Iterate through each book
    for title in titles:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        header = title.find_next('a')
        print('-----------')
        print(header)


# %%
# not sure why this grabs a title in the middle of the page???
leadtitle = title.find('a')
print(leadtitle)


# %%
# yet this works?? for paragraph...
news_p = soup.find('div', class_='article_teaser_body')
print(news_p)


# %%
# Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
executable_path = {'executable_path': './chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(jpl_url)
html_image = browser.html

# Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
full_image_button = browser.find_by_id("full_image")
# Make sure to find the image url to the full size `.jpg` image.
full_image_button.click()
# Make sure to save a complete url string for this image.
featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA11591_hires.jpg'


# %%
### Mars Weather

# Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. 
# Save the tweet text for the weather report as a variable called `mars_weather`.
# **Note: Be sure you are not signed in to twitter, or scraping may become more difficult.**
# **Note: Twitter frequently changes how information is presented on their website. 
# If you are having difficulty getting the correct html tag data, consider researching Regular Expression Patterns and how they can be used in combination with the .find() method.**
executable_path = {'executable_path': './chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
twitter_url = "https://twitter.com/marswxreport?lang=en"
browser.visit(twitter_url)

html = browser.html
weather_soup = bs(html, "html.parser")


# %%
# ```python
# Example:
# mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
mars_weather = soup.find_all('div', class_='js-tweet-text-container')
print(mars_weather)


# %%
# mars_weather_tweet = weather_soup.find("div", attrs={"class": "tweet", "data-name": "Mars Weather"})
# can't figure out hierarchy convention to display the tweet
# mars_weather = weather_soup.find('div', class_='css-901aoa')
# print(mars_weather)


# %%
### Mars Facts

# * Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# * Use Pandas to convert the data to a HTML table string.
mars_df = pd.read_html("https://space-facts.com/mars/")[0]
print(mars_df)


# %%
mars_df.columns=["Description", "Value"]
mars_df


# %%
### Mars Hemispheres

# * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
executable_path = {'executable_path': './chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

# * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg
# https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg
# https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg
# https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg

# * Have both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. 
# Use a Python dictionary to store the data using the keys `img_url` and `title`.

# scrape images of Mars' hemispheres from the USGS site
mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
dicts = []

for i in range(1,9,2):
    dict = {}
    
    browser.visit(mars_hemisphere_url)
    
    hemi_html = browser.html
    hemi_soup = bs(hemi_html, 'html.parser')
    hemi_name_links = hemi_soup.find_all('a', class_='product-item')
    hemi_name = hemi_name_links[i].text.strip('Enhanced')
    
    detail_links = browser.find_by_css('a.product-item')
    detail_links[i].click()
    
    browser.find_link_by_text('Sample').first.click()
    
    browser.windows.current = browser.windows[-1]
    hemi_img_html = browser.html
    browser.windows.current = browser.windows[0]
    browser.windows[-1].close()
    
    hemi_img_soup = bs(hemi_img_html, 'html.parser')
    hemi_img_path = hemi_img_soup.find('img')['src']

    print(hemi_name)
    dict['title'] = hemi_name.strip()
    
    print(hemi_img_path)
    dict['img_url'] = hemi_img_path

    dicts.append(dict)
# * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

# ```python
# Example:
# hemisphere_image_urls = [
#     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
#     {"title": "Cerberus Hemisphere", "img_url": "..."},
#     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
#     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
# ]

