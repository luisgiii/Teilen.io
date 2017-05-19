from flask import Flask, render_template, request
app = Flask(__name__)

#Global variables for very specific use. Not for production...
cryptoAmount = ""
convertedAmount = ""

@app.route("/")
def main_page():
    global cryptoAmount, convertedAmount
    cryptoValue = request.args.get('firstCrypto')
    buyButton = request.args.get('exchange')
    if cryptoValue != None:
        cryptoAmount = cryptoValue
        print "Stored cdc: " + cryptoAmount
        #API call to convert to the other crypto.
        convertedAmount = "0"

    if buyButton == "Get":
        print "Buy: " + cryptoAmount
    return render_template('mainView.html', value1 = cryptoAmount, value2 = convertedAmount)

if __name__ == "__main__":
    app.run()
