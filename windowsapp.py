# Note we imported request!
from flask import Flask, render_template, request
from ast import literal_eval
from CoinChangeFinder import simulatespending,globallog2
import sys,os
from CoinChangeFinder import buy

from waitress import serve



#To build
#pyinstaller --onefile --add-data "templates;templates"  windowsapp.py

#To test on local PC
#http://localhost:8080

#To test if the exe is running standalone on another PC
#http://192.168.0.17:8080/     where the IP is the other PCs IP address


base_dir = '.'
if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)


app = Flask(__name__,template_folder=os.path.join(base_dir, 'templates'))

@app.route('/')
def index():
    return render_template("index.html")


# This page will be the page after the form
@app.route('/report')
def report():
    denomination = request.args.get('denomination')
    wallet = request.args.get('wallet')
    price = request.args.get('price')
    #cumtotalcoins = simulatespending(denomination, 1, wallet, price)
    # buy(
    #     int(price),
    #     literal_eval(wallet),
    #     literal_eval(denomination)
    #     )
    cumtotalcoins = simulatespending(literal_eval(denomination), 1, literal_eval(wallet), int(price))
    #buy(, "[(1,2), (5,2), (10,2), (50,2), (100,2), (1000,2), (5000,2), (10000,2)]", "[1, 5, 10, 50, 100, 1000, 5000, 10000]")
   # buy(price,wallet,denomination)


    #rint("heh")
    return render_template('report.html',denomination=denomination,wallet=wallet,price=price,
                           cumtotalcoins=cumtotalcoins,globallog=globallog2)


if __name__ == '__main__':
    #app.run(debug=True)
    #app.run(host='0.0.0.0', debug=True, use_reloader=True)
    #import os, sys

    #waitress - serve - -call 'flaskr:create_app'
    #from waitress import serve
    #serve(wsgiapp)

    #sys.path.append(os.getcwd())

    #waitress server
    serve(app,host='0.0.0.0', port=8080)

    #flash default server
    #app.run(host='0.0.0.0', port=8080, debug=True)
