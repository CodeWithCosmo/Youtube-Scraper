import sys
from flask import Flask,render_template,request
from src.utils import scrape_records,write_mongo
from src.exception import CustomException
from waitress import serve

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
        
        return render_template('output.html', context=scrapes)

    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}", exc_info=True)
        return render_template('error.html', error_message=str(e)), 500
    
if __name__ == '__main__':
       serve(app, host='0.0.0.0', port=8080)