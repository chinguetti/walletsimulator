# Note we imported request!
from flask import Flask, render_template, request
from ast import literal_eval
from CoinChangeFinder import simulatespending
from CoinChangeFinder import buy

app = Flask(__name__)

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

    return render_template('report.html',denomination=denomination,wallet=wallet,price=price,
                           cumtotalcoins=cumtotalcoins)

if __name__ == '__main__':
    app.run(debug=True)
