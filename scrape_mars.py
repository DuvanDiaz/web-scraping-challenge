import pymongo
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# MongoDB setup

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = mars_db


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless = False)

def scrape():
    browser = init_browser()
    collection.drop()

    # NASA: Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    news_html = browser.html
    news_soup = bs(news_html, 'lxml')
    news_title = news_soup.find("div", class_ = "content_title").text
    news_p = news_soup.find("div", class_ = "rollover_description_inner").text

    # JPL Imgs
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    img_html = browser.html
    img_soup = bs(img_html, "html.parser")
    url_j = img_soup.find("div", class_ = "carousel_container").article.footer.a["data-fancybox-href"]
    base_link = "https:" + img_soup.find("div", class_ = "jpl_logo").a["href"].rstrip('/')
    feat_url = base_link + url_j
    feat_img_title = img_soup.find("h1", class_ = "media_feature_title").text.strip()

    # NASA: Mars weather (twitter api)
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(tweet_url)
    twitter_html = browser.html
    twitter_soup = bs(twitter_html, "html.parser")
    mars_weather = twitter_soup.find("p", class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    # Mars Facts
    facts_url = "https://space-facts.com/mars/"
    facts_table = pd.read_html(facts_url)
    facts_df = facts_table[0]
    facts_df = facts_df[["Mars - Earth Comparison", "Mars"]]
    facts_html = facts_df.to_html(header = False, index = False)

    # Mars: Hemispheres
    hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    hemis_html = browser.html
    hemis_soup = bs(hemis_html, "html.parser")
    results = hemis_soup.find_all("div", class_ = "item")
    hemis_imgs = []
    for results in results:
        products_dict = {}
        titles = result.find("h3").text
        end_link = result.find("a")["href"]
        img_link = "https://astrogeology.usgs.gov/" + end_link
        browser.visit(img_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_ = "downloads")
        img_url = downloads.find("a")["href"]
        products_dict["title"] = titles
        products_dict["img_url"] = img_url
        hemispheres_imgs_url.append(products_dict)



    browser.quit()

    # Results
    mars_df = {
        "news_title": news_title,
        "summary": news_p,
        "featured_image": feat_url,
        "featured_image_title": feat_img_title,
        "weather": mars_weather,
        "fact_table": facts_html,
        "hemispheres_images_urls": hemispheres_images_urls,
        "news_url": url,
        "jpl_url":jpl_url,
        "weather_url": tweet_url,
        "fact_url": facts_url,
        "hemispheres_url": hemis_url,
    }
    collection.insert(mars_df)


                


 

