from flask import Flask, render_template
app = Flask(__name__)

@app.route("/", methods=['POST'])
def main_page():
    getCrypto = request.form['exchange'] == 'Get ETH'
    firstValue = request.form['firstCrypto']
    secondValue = request.form['secondCrypto']
    
    return render_template('mainView.html')

if __name__ == "__main__":
    app.run()
