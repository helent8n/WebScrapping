# import dependecies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from selenium import webdriver
import os


# initialize browser
def init_browser():
    
    # @NOTE: Replace the path with your actual path to the chromedriver
    # Windows users
    executable_path = {"executable_path": "C:\\Users\\jarrett\\Downloads\\chromedriver_win32 (1)\\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    browser = init_browser()

    # create Mission to Mars global dictionary that can be imported into Mongo
    mars_info = {}    


    ##################
    # NASA Mars News #
    ##################
   # Visit Nasa news url through splinter module
    nasa_mars_news_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_mars_news_url)

    time.sleep(2)

    # HTML object
    nasa_html = browser.html

    # Parse HTML with BeautifulSoup
    nasa_soup = bs(nasa_html, "html.parser")

    
    ### code to get all nasa news ###
    news_lists = nasa_soup.find_all('li', class_='slide')

    titles_list = []
    paragraphs_list = []

    # iterate all the news list
    for news_list in news_lists:

        title = news_list.find('h3').text
        
        paragraph = news_list.find('div', class_='article_teaser_body').text
        
        #Append both to a list
        titles_list.append(title)
        paragraphs_list.append(paragraph)

        
    # get the first title and paragraph
    news_title = titles_list[0]
    news_p = paragraphs_list[0]
   
    
    ### Store data in a dictionary ###
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_p
    
    

    ##################
    # NASA Mars News #
    ##################

    # visit mars image url through splinter module
    mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    # HTML object
    browser.visit(mars_image_url)

    time.sleep(5)

    browser.find_by_css('a.button').click()

    time.sleep(5)
    
    # parse HTML with BeautifulSoup
    soup = bs(browser.html,'html.parser')

    # find tag 'img'
    end = soup.find('img',class_='fancybox-image')['src']
    
    # cocatenate website url with scrapped route and store in variable feature_image_url
    feature_image_url = "https://www.jpl.nasa.gov"+end

    
    ### store feature image in the dictionary ###
    mars_info['feature_image_url'] = feature_image_url
    
    

    ##################
    #  Mars  Weather #
    ##################


   # Visit Nasa news url through splinter module
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    
    # HTML Object 
    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_weather, 'html.parser')

    # Find all elements that contain tweets
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

    weather_tweet_list = []

    for tweet in latest_tweets: 
        weather_tweet = tweet.find('p').text
    
        weather_tweet_list.append(weather_tweet)
    
        #Get the first weather tweet
        mars_weather = weather_tweet_list[0]
  


        ### store feature image in the dictionary ###
        mars_info['mars_weather'] = mars_weather
    
    
    
    ##################
    #    Mars Facts  #
    ##################

    
    # visit Mars facts URL
    facts_url = 'https://space-facts.com/mars/'

    # use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # get rid of trailing colon
    mars_df['Description'] = mars_df['Description'].str[:-1]

    # set the index to the `Description` column without row indexing
    mars_df = mars_df.set_index('Description')

    # Save html code to file 'facts.html'
    # mars_df.to_html(open('facts.html', 'w'))

    facts_html_table = mars_df.to_html()
    facts_html_table = facts_html_table.replace('\n', '')
    
    
    ### store facts in the dictionary ###
    mars_info['facts_html_table'] = facts_html_table
    
   
    ###################
    # Mars Hemisphere #
    ###################

    
    executable_path = {"executable_path": "C:\\Users\\jarrett\\Downloads\\chromedriver_win32 (1)\\chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    # Visit hemispheres website through splinter module 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    time.sleep(5)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items: 
        img_dict = {}
        # Store title
        title = i.find('h3').text
    
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
    
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
    
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = bs( partial_img_html, 'html.parser')
    
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
        img_dict["title"] = title
        img_dict["img_url"] = img_url
 
        # Append the retreived information into a list of dictionaries 
        #hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        hemisphere_image_urls.append(img_dict)
    
    mars_info["hemisphere_image_urls"] = hemisphere_image_urls
    
    # close the browser after scrapping
    browser.quit()

    # return results
    return mars_info

a = scrape()
print(a)