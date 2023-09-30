import os
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from src.exception import CustomException
from src.logger import logging as lg


def scrape_records(handle):
    try:
        lg.info(f"Scraping for {handle}")
        url = f"https://www.youtube.com/@{handle}/videos"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        driver.execute_script("window.scrollTo(0,500)", "")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        scrapes = []
        for i in range(5):
            title = (soup.find_all("a", {"id": "video-title-link"}))[i].text
            view = (soup.find_all("div", {"id": "metadata"}))[i].find_all("span")[1].text
            upload = (soup.find_all("div", {"id": "metadata"}))[i].find_all("span")[2].text
            video_link = "https://www.youtube.com" + str((soup.find_all("a", {"id": "video-title-link"}))[i].get("href"))
            thumbnail_link = (soup.find_all("img", {"class": "yt-core-image--fill-parent-height"}))[i].get("src")[0:48]
            
            data = {              
                "Title": title,
                "Views": view,
                "Upload": upload,
                "Video Link": video_link,
                "Thumbnail Link": thumbnail_link
                }
            
            scrapes.append(data)

    except Exception as e:
        lg.info('Handle not found')
        raise CustomException(e, sys)
    
    finally:
        driver.close()   
        lg.info('Scraping Completed')
    
    return scrapes