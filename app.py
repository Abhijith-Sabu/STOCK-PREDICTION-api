import os
import requests
import smtplib
import http.client
import json
import vonage
import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()
twilio_api = os.getenv('TWILIO_API')
twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
from_number = os.getenv('FROM_NUMBER')
to_number = os.getenv('TO_NUMBER')
stock = os.getenv('STOCK')
mypassword = os.getenv('MY_PASSWORD')
email = os.getenv('EMAIL')
STOCK = "TSLA"
# apikey_stock=os.environ.get("APIKEY")
stock_paramters={
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK,
    "apikey":os.getenv('API_KEY_STOCKS')
}
# Remove-Item Env:APIKEY
# $env:APIKEY= "WUDZF1GU9VEBTD5L"
# Get-ChildItem Env:

## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
#HINT 2: Work out the value of 5% of yerstday's closing stock price. 
STOCK_ENDPOINT = "https://www.alphavantage.co/query"

stock_request=requests.get(url=STOCK_ENDPOINT,params=stock_paramters)
stock_request.raise_for_status()
data=stock_request.json()["Time Series (Daily)"]
yesterday_data=[value for (key,value ) in data.items()]
# print(yesterday_data)
y_close=float(yesterday_data[0]["4. close"])

db_close=float(yesterday_data[1]["4. close"])



differnce=abs(y_close-db_close)

percentage=(differnce/db_close)*100
print(percentage)
if abs(percentage)>=0.124:
    NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
    COMPANY_NAME = "Tesla Inc"
    news_parameters={
        "q":COMPANY_NAME,
        "apiKey":os.getenv('API_KEY_TWI')
    }
    news_rsponse=requests.get(url=NEWS_ENDPOINT,params=news_parameters)
    article=news_rsponse.json()["articles"]
    news=article[:2]
    titles = [article["title"] for article in news]
    briefs=[_["description"] for _ in news]
    bodie=f"🔻\n\n\nTitle:{titles[0]}\n\n\n brief: {briefs[0]}\n\nTitle: {titles[1]}\n\nbrief: {briefs[1]}"
    print(bodie)
    # Download the helper library from https://www.twilio.com/docs/python/install
    import os
    from twilio.rest import Client


    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = twilio_account_sid
    auth_token = twilio_auth_token
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=f"{bodie}",
                        from_=from_number,
                        to=to_number
                    )

    print(message.sid)

        


        
