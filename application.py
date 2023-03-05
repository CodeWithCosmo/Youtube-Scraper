import pymongo
from bs4 import BeautifulSoup
from selenium import webdriver
from flask_cors import cross_origin
from flask import Flask,render_template,request
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
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        try:
            url = request.form['content']
            driver.get(url)
            driver.execute_script("window.scrollTo(0,400)", "")
            soup = BeautifulSoup(driver.page_source, "html.parser")
            ###################!Stage 1######################
            scrape = []
            for i in range(5):
                try:
                    title = (soup.find_all("a", {"id": "video-title-link"}))[i].text
                    title.encode(encoding='utf-8')                             
                except Exception as e:
                    print(e)
                try:
                    view = (soup.find_all("div", {"id": "metadata"}))[i].find_all("span")[1].text
                except Exception as e:
                    print(e)
                try:
                    upload = (soup.find_all("div", {"id": "metadata"}))[i].find_all("span")[2].text
                except Exception as e:
                    print(e)                    
                try:
                    video_link = "https://www.youtube.com" + str((soup.find_all("a", {"id": "video-title-link"}))[i].get("href"))
                except Exception as e:
                    print(e)
                try:
                    thumbnail_link = (soup.find_all("img", {"class": "yt-core-image--fill-parent-height"}))[i].get("src")[0:48]
                except Exception as e:
                    print(e)

                mydict = {"Title": title, "Views": view, "Upload": upload,"Video Link": video_link, "Thumbnail Link": thumbnail_link}
                scrape.append(mydict)           
            ###################!Stage 2######################
            client = pymongo.MongoClient("mongodb+srv://lalit547:mongocloud@youtubescrape.shbwtmx.mongodb.net/?retryWrites=true&w=majority")
            mydb= client.YoutubeScrape
            mycollection = mydb.LastFiveVideos
            mycollection.insert_many(scrape)
            return render_template('results.html', scrape=scrape)
        except Exception as e:
            return 'Something Wrong !' +str(e)
        finally:
            driver.quit()
    else:
        return render_template('index.html')    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)