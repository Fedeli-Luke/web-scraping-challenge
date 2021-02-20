from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import pymongo

def init_browser():
    executable_path = {'executable_path': '/Users/lukefedeli/Documents/GitHub/web-scraping-challenge/Missions_to_Mars/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_mars_info():
    # New dictionary that can be imported into Mongo
    mars_info = {} 

    try:
        # Initialize browser
        browser = open_browser()

        # Site to scrape news from
        nasa_site = 'https://mars.nasa.gov/news/'
        browser.visit(nasa_site)

        # Beautiful Soup to parse data
        html = browser.html
        nasa_soup = BeautifulSoup(html, 'html.parser')

        news_data = []
  
        news_title = nasa_soup.find('div', class_='content_title').find('a')
        print(news_title)

        # Collect paragraph from atricles
        news_paragraph = nasa_soup.find('div', class_='article_teaser_body').text
        print(news_paragraph)

        # Add to list
        news_comb = {"news_title" : news_title, "news Paragraph" : news_paragraph}
        
        news_data.append(news_comb)

        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_paragraph
    
        browser.quit()

    except Exception as error:
        print(error)

    try:
        # Initialize browser
        browser = open_browser()

        jpl_url_image = 'https://www.jpl.nasa.gov/images?search=&category=Mars'
        browser.visit(jpl_url_image)

        # Find image of current article
        current_image = browser.find_by_id('img')
        current_image.click() 

        # Find the more images button
        more_info = browser.find_link_by_partial_text('more info')
        more_info.click()

        # Find the more images button
        more_info = browser.find_link_by_partial_text('more info')
        more_info.click()

        html = browser.html
        image_soup = BeautifulSoup(html, 'html.parser')

        # Find image URL
        image_url = image_soup.find('figure', class_='lede').find('img')['src']
        image_url


        # Add image url to the base url
        base_url = 'https://www.jpl.nasa.gov'
        current_image_url = base_url + image_url
        current_image_url

        browser.quit()

    except Exception as error:
        print(error)

    try:
        # Initialize browser
        browser = open_browser()

        # URL of page to be scraped - Mars Facts
        facts_url = 'http://space-facts.com/mars/'
        browser.visit(facts_url)

        mars_facts = pd.read_html(browser.html)

        mars_df = mars_facts[0]

        mars_df.columns = ['Data', 'Values']

        facts_table = mars_df.to_html('facts_table.html')

        print(facts_table)

        mars_info['mars_facts'] = facts_table

        browser.quit()

    except Exception as error:
        print(error)

    try:
        # Initialize browser
        browser = open_browser()    

        # Site url
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # Parse data with Beautiful Soup
        html_hemispheres = browser.html
        hemispheres_soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Gather all the hemisphere items
        items = hemispheres_soup.find_all('div', class_='item')
        hemisphere_image_urls = []


        hemispheres_main_url = 'https://astrogeology.usgs.gov'

        # Loop through the items previously urls
        for item in items: 
            # Titles
            title = item.find('h3').text
    
            # Links for image website
            img_url = item.find('a', class_='itemLink product-item')['href']
    
            # Go to image website
            browser.visit(hemispheres_main_url + img_url)
    
            # HTML for image website 
            img_html = browser.html
    
            # Parse HTML for image website 
            image_soup = BeautifulSoup( img_html, 'html.parser')
    
            # Create full image url 
            img_url = hemispheres_main_url + image_soup.find('img', class_='wide-image')['src']
    
            hemisphere_urls = {"title" : title, "img_url" : img_url}
     
            hemisphere_image_urls.append(hemisphere_urls)

        # Display the urls
        print(hemisphere_image_urls)

        browser.quit()

    except Exception as error:
        print(error)    

    mars_info['hemisphere_urls'] = hemisphere_urls

     
    return mars_info        




