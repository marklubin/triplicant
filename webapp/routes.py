"""
routes.py
main entry point for web application
Mark Lubin
"""
DEBUG = True
from flask import Flask,url_for,render_template,request

app = Flask(__name__)#Flask app object

#routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trip',methods = ['POST'])
def trip():
    if request.method == 'POST':
        return render_template('trip.html',\
                               start = request.form['start'],\
                               end = request.form['end'])
    else:
        return "Error, something bad happened."


if __name__ == '__main__':
    app.run(debug = DEBUG)#start server
