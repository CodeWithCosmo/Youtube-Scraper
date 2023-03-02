import time
import pymongo
from bs4 import BeautifulSoup
from selenium import webdriver
from flask_cors import cross_origin
from flask import Flask, render_template, request
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

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
            driver = webdriver.Edge()
            options = webdriver.EdgeOptions()
            options.add_argument("--headless=new")
            url = request.form['content']
            driver.get(url)
            driver.execute_script("window.scrollTo(0,400)", "")
            soup = BeautifulSoup(driver.page_source, "html.parser")
            ###################!Stage 1######################
            scrape = []
            for i in range(5):
                title = (soup.find_all("a", {"id": "video-title-link"}))[i].text
                title.encode(encoding='utf-8')                             
                view = (soup.find_all("div", {"id": "metadata"}))[i].find_all("span")[1].text
                upload = (soup.find_all("div", {"id": "metadata"}))[i].find_all("span")[2].text
                video_link = "https://www.youtube.com" + str((soup.find_all("a", {"id": "video-title-link"}))[i].get("href"))
                thumbnail_link = (soup.find_all("img", {"class": "yt-core-image--fill-parent-height"}))[i].get("src")[0:50]
                mydict = {"Title": title, "Views": view, "Upload": upload,"Video Link": video_link, "Thumbnail Link": thumbnail_link}
                scrape.append(mydict)           
            ###################!Stage 2######################
            # client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")  # Local Server
            client = pymongo.MongoClient("mongodb+srv://lalit547:4W2lDPlTbwrbqkte@youtubescrape.shbwtmx.mongodb.net/?retryWrites=true&w=majority")
            mydb= client.YoutubeScrape
            mycollection = mydb.LastFiveVideos
            mycollection.insert_many(scrape)
            time.sleep(5)
            driver.quit()            
            return render_template('results.html', scrape=scrape[0:5])
        except Exception as e:
            print('The Exception message is: ', e)
            return 'Something Wrong !'
    else:
        return render_template('index.html')    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
