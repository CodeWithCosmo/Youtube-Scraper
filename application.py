import time
import sys
import pymongo
from bs4 import BeautifulSoup
from selenium import webdriver
from flask_cors import cross_origin
from flask import Flask,render_template,request
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from logger import logging
from exception import CustomException

application = Flask(__name__)  
app = application

@app.route('/', methods=['GET'])  
@cross_origin()
def home():
    return render_template("index.html")

@app.route('/scrape', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            
            handle = request.form['content']
            logging.info(f"Scraping for {handle}")
            url = f"https://www.youtube.com/@{handle}/videos"
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            driver = webdriver.Chrome(service=service,options=options)                        
            driver.get(url)
            driver.execute_script("window.scrollTo(0,500)", "")
            time.sleep(2.5)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            logging.info(f"Scraped for {handle}")
            scrape = []
            for i in range(5):
                try:
                    title = (soup.find_all("a", {"id": "video-title-link"}))[i].text
                    title.encode(encoding='utf-8')                             
                except Exception as e:
                    raise CustomException(e, sys)
                try:
                    view = (soup.find_all("div", {"id": "metadata"}))[i].find_all("span")[1].text
                except Exception as e:
                    raise CustomException(e, sys)
                try:
                    upload = (soup.find_all("div", {"id": "metadata"}))[i].find_all("span")[2].text
                except Exception as e:
                    raise CustomException(e, sys)                    
                try:
                    video_link = "https://www.youtube.com" + str((soup.find_all("a", {"id": "video-title-link"}))[i].get("href"))
                except Exception as e:
                    raise CustomException(e, sys)
                try:
                    thumbnail_link = (soup.find_all("img", {"class": "yt-core-image--fill-parent-height"}))[i].get("src")[0:48]
                except Exception as e:
                    raise CustomException(e, sys)

                mydict = {"Title": title, "Views": view, "Upload": upload,"Video Link": video_link, "Thumbnail Link": thumbnail_link}
                scrape.append(mydict)           
            logging.info(f'Storing data in MongoDB')
            client = pymongo.MongoClient("mongodb+srv://cwc:mongocloud@youtubescrapping.ryi6ibl.mongodb.net/?retryWrites=true&w=majority")            
            mydb= client.YoutubeScrape
            mycollection = mydb.LastFiveVideos
            mycollection.insert_many(scrape)
            logging.info(f'Data stored in MongoDB')
            return render_template('results.html', scrape=scrape)
        except Exception as e:
            raise CustomException(e, sys)
        finally:
            logging.info(f'Closing Browser')
            driver.quit()
    else:
        return render_template('index.html')    
if __name__ == "__main__":
    logging.info('Application Started')
    app.run()