from splinter import Browser
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def scrape():
    results_dict = {}
    executable_path = {'executable_path': 'C:/bin/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    # Mars News 
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html 
    soup = bs(html, 'html.parser')
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    results_dict['news_title'] = news_title
    results_dict['news_p'] = news_p

    # Mars Space Images - Featured Image

    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_image)
    image_list=[]
    for x in range(1, 2):
        html = browser.html
        soup = bs(html, 'html.parser')
        mars_image = soup.find_all('article',class_='carousel_item')
        for image in mars_image:
            print('page:', x, '-------------')
            print(image)
            image_list.append(image)
        try:
            browser.links.find_by_partial_text('more')    
        except:
            print("Scraping Complete")
    images= image_list[0]['style'].split("'")[1]
    beginn='https://www.jpl.nasa.gov'
    featured_image_url = beginn+images

    results_dict['featured_image_url'] = featured_image_url

    # Mars Facts
    url_facts='https://space-facts.com/mars/'
    time.sleep(1)
    tables = pd.read_html(url_facts)
    df=tables[0]
    df.columns=['Mars Profile','Figures']
    df.set_index('Mars Profile', inplace=True)
    mars_df= df.reset_index().to_html(index = False)

    results_dict['mars_df'] = mars_df

    # Mars Hemispheres

    hemis_url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url)
    soup = bs(browser.html, 'html.parser')

    hemisphere_image_urls = []

    results_hemis = soup.find_all('div', class_='item')

    for item in results_hemis:
        title_hemis = item.h3.text
        first_url = hemis_url[:30] + item.find('a', class_='itemLink')['href']
        browser.visit(first_url)
        soup = bs(browser.html, 'html.parser')
        time.sleep(1)
        final_url = hemis_url[:30] + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({'title': title_hemis, 'img_url':final_url})

    results_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return results_dict