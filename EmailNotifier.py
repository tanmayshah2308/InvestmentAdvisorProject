import smtplib
import ssl
import yfinance as yf
import json

stocks_to_be_notified = {}

# JSON file holds all the stocks and whether or not we have already sent a
# notification or not. If a notification has already been sent (True), no need
# to resend.
with open("data.json") as json_file:
    data = json.load(json_file)

# Stocks Being Watched: Air Canada
# 1) Air Canada
ac = yf.Ticker("AC.TO")
ac_bid = ac.info['bid']
if ac_bid < 18 and data["Air Canada"] == "False":
    stocks_to_be_notified["Air Canada"] = ac_bid

