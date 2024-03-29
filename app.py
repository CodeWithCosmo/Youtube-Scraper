import sys
from flask import Flask,render_template,request
from src.utils import scrape_records,write_mongo
from src.exception import CustomException

app = Flask(__name__)  

@app.route('/', methods=['GET'])  
def home():
    return render_template("home.html")

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        handle = request.form['content']
        scrapes = scrape_records(handle)
        write_mongo(scrapes)
        return render_template('output.html',context=scrapes)

    except Exception as e:
        raise CustomException(e, sys)