import pymongo
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# MongoDB setup


# client = pymongo.MongoClient('mongodb://localhost:27017')
# db = client.mars_db
# collection = mars_db


# def init_browser():
#     executable_path = {'executable_path': 'C:Users/DuvanFelipe/Downloads/chromedriver.exe'}
#     return Browser('chrome', **executable_path, headless = False)

# def scrape():
#     browser = init_browser()
#     collection.drop()

#     # NASA: Mars News
#     url = 'https://mars.nasa.gov/news/'
#     browser.visit(url)
#     news_html = browser.html
#     news_soup = bs(news_html, 'lxml')
#     news_title = news_soup.find("div", class_ = "content_title").text
#     news_p = news_soup.find("div", class_ = "rollover_description_inner").text

#     # JPL Imgs
#     img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
#     browser.visit(img_url)
#     img_html = browser.html
#     img_soup = bs(img_html, "html.parser")
#     url_j = img_soup.find("div", class_ = "carousel_container").article.footer.a["data-fancybox-href"]
#     base_link = "https:" + img_soup.find("div", class_ = "jpl_logo").a["href"].rstrip('/')
#     feat_url = base_link + url_j
#     feat_img_title = img_soup.find("h1", class_ = "media_feature_title").text.strip()

#     # NASA: Mars weather (twitter api)
#     tweet_url = "https://twitter.com/marswxreport?lang=en"
#     browser.visit(tweet_url)
#     twitter_html = browser.html
#     twitter_soup = bs(twitter_html, "html.parser")
#     mars_weather = twitter_soup.find("p", class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

#     # Mars Facts
#     facts_url = "https://space-facts.com/mars/"
#     facts_table = pd.read_html(facts_url)
#     facts_df = facts_table[0]
#     facts_df = facts_df[["Mars - Earth Comparison", "Mars"]]
#     facts_html = facts_df.to_html(header = False, index = False)

#     # Mars: Hemispheres
#     hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
#     browser.visit(hemispheres_url)
#     hemis_html = browser.html
#     hemis_soup = bs(hemis_html, "html.parser")
#     results = hemis_soup.find_all("div", class_ = "item")
#     hemis_imgs = []
#     for results in results:
#         products_dict = {}
#         titles = result.find("h3").text
#         end_link = result.find("a")["href"]
#         img_link = "https://astrogeology.usgs.gov/" + end_link
#         browser.visit(img_link)
#         html = browser.html
#         soup = bs(html, "html.parser")
#         downloads = soup.find("div", class_ = "downloads")
#         img_url = downloads.find("a")["href"]
#         products_dict["title"] = titles
#         products_dict["img_url"] = img_url
#         hemispheres_imgs_url.append(products_dict)



#     browser.quit()

#     # Results
#     mars_df = {
#         "news_title": news_title,
#         "summary": news_p,
#         "featured_image": feat_url,
#         "featured_image_title": feat_img_title,
#         "weather": mars_weather,
#         "fact_table": facts_html,
#         "hemispheres_images_urls": hemispheres_images_urls,
#         "news_url": url,
#         "jpl_url":jpl_url,
#         "weather_url": tweet_url,
#         "fact_url": facts_url,
#         "hemispheres_url": hemis_url,
#     }
#     collection.insert(mars_df)


#Site Navigation
executable_path = {"executable_path": "/Users/sharonsu/Downloads/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)


# Defining scrape & dictionary
def scrape():
    final_data = {}
    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_weather"] = marsWeather()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()

    return final_data

# # NASA Mars News

def marsNews():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    output = [news_title, news_p]
    return output

# # JPL Mars Space Images - Featured Image
def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url

# # Mars Weather
def marsWeather():
    
    import tweepy
    # Twitter API Keys
    def get_file_contents(filename):
        try:
            with open(filename, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print("'%s' file not found" % filename)

    consumer_key = get_file_contents('consumer_key')
    consumer_secret = get_file_contents('consumer_secret')
    access_token = get_file_contents('access_token')
    access_token_secret = get_file_contents('access_token_secret')

    # Setup Tweepy API Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    target_user = "MarsWxReport"
    tweet = api.user_timeline(target_user, count =1)
    mars_weather = ((tweet)[0]['text'])
    return mars_weather


# # Mars Facts
def marsFacts():
    import pandas as pd
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_data.columns = ["Description", "Value"]
    mars_data = mars_data.set_index("Description")
    mars_facts = mars_data.to_html(index = True, header =True)
    return mars_facts


# # Mars Hemispheres
def marsHem():
    import time 
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        dictionary = {"title": title, "img_url": image_url}
        mars_hemisphere.append(dictionary)
    return mars_hemisphere

                


 

