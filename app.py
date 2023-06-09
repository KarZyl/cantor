import requests
import pandas as pd
from flask import Flask, render_template, request


app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

df = pd.json_normalize(data, record_path='rates', meta='table')
df = df[['currency', 'code', 'bid', 'ask']]

df.to_csv('exchange_rates.csv', sep=";", index=True)


@app.route('/')
def home():
    data = pd.read_csv('exchange_rates.csv',sep=";", names = ['number', 'currency', 'code','bid','ask'])
    return render_template('index.html', currencies=data['currency'])

@app.route('/', methods=['POST'])
def calculate():
    data = pd.read_csv('exchange_rates.csv', sep=";", names = ['number', 'currency', 'code','bid','ask'])
    currency = request.form.get('currency')
    found = data[data.eq(currency).any(axis=1)]
    ask = float(found["ask"].values[0])
    amount = float(request.form.get('amount'))
    result = round(amount * ask, 2)
    return render_template('index.html', currency=currency, amount=amount, result=result)

if __name__ == '__main__':
    app.run(debug=True)
    app.config['TESTING'] = True